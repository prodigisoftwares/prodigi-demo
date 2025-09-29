from django.test import TestCase, override_settings
from django.urls import reverse

from apps.politics.models import Politician, TestSubmission

# Provide an in-memory template so assertTemplateUsed works.
TEMPLATES_OVERRIDE = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": False,
        "OPTIONS": {
            "loaders": [
                (
                    "django.template.loaders.locmem.Loader",
                    {
                        # minimal template that references context keys
                        "politics/partials/result.html": (
                            "{% for p in nearest %}{{ p.name }}{% endfor %}"
                            "{{ x }}{{ y }}{{ submission.id }}"
                        )
                    },
                )
            ]
        },
    }
]


@override_settings(TEMPLATES=TEMPLATES_OVERRIDE)
class ScoreViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Politicians placed so we can verify nearest-3 ordering precisely.
        # Target point for "all A" answers is approximately (-1.0, 0.876923...)
        Politician.objects.create(name="Near-1", x=-1.00, y=0.90)  # closest
        Politician.objects.create(name="Near-2", x=-0.90, y=0.90)  # next
        Politician.objects.create(name="Near-3", x=-1.00, y=0.70)  # third
        Politician.objects.create(name="Far-1", x=1.00, y=-1.00)  # far away
        Politician.objects.create(name="Far-2", x=0.50, y=0.00)  # also far

    def test_get_is_bad_request(self):
        resp = self.client.get(reverse("politics:score"))
        self.assertEqual(resp.status_code, 400)
        self.assertIn(b"Use POST", resp.content)

    def test_post_creates_submission_and_renders_nearest(self):
        """
        Post all 'A' answers:
          - compute_coords should yield x == -1.0 and y ≈ 0.876923...
          - submission saved with exact answers
          - nearest should be the three 'Near-*' politicians in the correct order
        """
        post_data = {f"q{i}": "A" for i in range(1, 9)}
        url = reverse("politics:score")
        resp = self.client.post(url, data=post_data)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "politics/partials/result.html")

        # Context checks
        self.assertIn("submission", resp.context)
        self.assertIn("nearest", resp.context)
        self.assertIn("x", resp.context)
        self.assertIn("y", resp.context)

        sub = resp.context["submission"]
        nearest = resp.context["nearest"]
        x, y = resp.context["x"], resp.context["y"]

        # TestSubmission persisted
        self.assertEqual(TestSubmission.objects.count(), 1)
        sub_db = TestSubmission.objects.get(pk=sub.pk)
        # answers are stored as strings keyed by q1..q8
        self.assertEqual(sub_db.answers, post_data)
        self.assertAlmostEqual(sub_db.x, x)
        self.assertAlmostEqual(sub_db.y, y)

        # Expected coordinates for all 'A'
        self.assertAlmostEqual(x, -1.0)
        self.assertAlmostEqual(y, 2.28 / 2.6)  # ≈ 0.8769230769

        # Top 3 nearest must be these three, in this exact order
        self.assertEqual([p.name for p in nearest], ["Near-1", "Near-2", "Near-3"])
        self.assertEqual(len(nearest), 3)

    def test_post_with_no_answers_defaults_to_origin_and_picks_nearest(self):
        """
        When POST has no 'q*' fields, compute_coords returns (0.0, 0.0).
        Verify that a submission is still created and nearest-3 are returned
        based on distance from the origin.
        """
        url = reverse("politics:score")
        resp = self.client.post(url, data={})
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "politics/partials/result.html")

        sub = resp.context["submission"]
        x, y = resp.context["x"], resp.context["y"]
        nearest = resp.context["nearest"]

        self.assertAlmostEqual(x, 0.0)
        self.assertAlmostEqual(y, 0.0)
        self.assertTrue(TestSubmission.objects.filter(pk=sub.pk).exists())

        # Compute expected nearest by hand for (0,0)
        # Distances:
        #  Near-1: sqrt(1^2 + 0.9^2)  ≈ 1.345
        #  Near-2: sqrt(0.9^2 + 0.9^2)≈ 1.273  <-- closest
        #  Near-3: sqrt(1^2 + 0.7^2)  ≈ 1.220  <-- actually this is closest
        #  Far-1:  sqrt(1^2 + 1^2)    ≈ 1.414
        #  Far-2:  sqrt(0.5^2 + 0^2)  = 0.5    <-- closest overall
        # Therefore nearest 3 should be: Far-2, Near-3, Near-2
        self.assertEqual([p.name for p in nearest], ["Far-2", "Near-3", "Near-2"])
        self.assertEqual(len(nearest), 3)

    def test_post_returns_only_three_nearest_even_with_many_politicians(self):
        # Add a bunch more far-away politicians
        for i in range(10):
            Politician.objects.create(name=f"Very-Far-{i}", x=10 + i, y=10 + i)

        url = reverse("politics:score")
        resp = self.client.post(url, data={})  # origin (0,0)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context["nearest"]), 3)
