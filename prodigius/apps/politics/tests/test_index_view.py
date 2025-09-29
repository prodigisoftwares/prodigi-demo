from django.test import RequestFactory, TestCase, override_settings
from django.urls import resolve, reverse

from apps.politics.models import Question
from apps.politics.views import IndexView

# In-memory template so assertTemplateUsed works without touching disk.
TEMPLATES_OVERRIDE = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": False,
        "OPTIONS": {
            "loaders": [
                (
                    "django.template.loaders.locmem.Loader",
                    {
                        "politics/index.html": (
                            "{% for q in questions %}{{ q.order }}{% endfor %}"
                        )
                    },
                )
            ]
        },
    }
]


@override_settings(TEMPLATES=TEMPLATES_OVERRIDE)
class IndexViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create questions with explicit order to verify Meta.ordering = ["order"]
        Question.objects.create(text="Q3?", order=3)
        Question.objects.create(text="Q1?", order=1)
        Question.objects.create(text="Q2?", order=2)

    def test_url_resolves_to_indexview(self):
        url = reverse("politics:index")
        match = resolve(url)
        self.assertIs(match.func.view_class, IndexView)

    def test_get_returns_200_and_uses_template(self):
        url = reverse("politics:index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "politics/index.html")

    def test_context_contains_questions_in_order(self):
        url = reverse("politics:index")
        resp = self.client.get(url)
        self.assertIn("questions", resp.context)
        questions = list(resp.context["questions"])
        # Expect order: 1, 2, 3 due to Meta.ordering
        self.assertEqual([q.order for q in questions], [1, 2, 3])
        self.assertEqual(len(questions), Question.objects.count())

    def test_requestfactory_direct_context(self):
        """Call the CBV directly and verify context keys without template rendering."""
        rf = RequestFactory()
        request = rf.get(reverse("politics:index"))
        response = IndexView.as_view()(request)
        ctx = response.context_data
        self.assertIn("questions", ctx)
        self.assertEqual([q.order for q in ctx["questions"]], [1, 2, 3])

    def test_empty_state(self):
        Question.objects.all().delete()
        url = reverse("politics:index")
        resp = self.client.get(url)
        self.assertEqual(list(resp.context["questions"]), [])
