from django.test import RequestFactory, TestCase
from django.urls import resolve, reverse

from apps.politics.models import Choice, Question
from apps.politics.views import TakeView


class TakeViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # 3 questions, each with A/B choices (label is max_length=1)
        q1 = Question.objects.create(text="Q1?", order=1)
        q2 = Question.objects.create(text="Q2?", order=2)
        q3 = Question.objects.create(text="Q3?", order=3)

        for q in (q1, q2, q3):
            Choice.objects.create(question=q, label="A", text="A choice")
            Choice.objects.create(question=q, label="B", text="B choice")

    def test_url_and_resolves_to_takeview(self):
        url = reverse("politics:test")
        match = resolve(url)
        self.assertIs(match.func.view_class, TakeView)

    def test_get_returns_200_and_uses_template(self):
        url = reverse("politics:test")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "politics/take.html")

    def test_context_contains_all_questions(self):
        url = reverse("politics:test")
        response = self.client.get(url)
        questions = list(response.context["questions"])
        self.assertEqual(len(questions), Question.objects.count())
        for q in questions:
            # A and B exist
            self.assertEqual(q.choices.count(), 2)
            self.assertSetEqual(
                set(q.choices.values_list("label", flat=True)), {"A", "B"}
            )

    def test_prefetch_related_eliminates_n_plus_one(self):
        """
        With prefetch_related('choices'), iterating each question's choices
        should not issue additional queries.
        """
        url = reverse("politics:test")
        response = self.client.get(url)
        questions = list(response.context["questions"])

        with self.assertNumQueries(0):
            for q in questions:
                _ = list(q.choices.all())

    def test_requestfactory_direct_context(self):
        rf = RequestFactory()
        request = rf.get(reverse("politics:test"))
        response = TakeView.as_view()(request)
        ctx = response.context_data
        self.assertIn("questions", ctx)
        questions = list(ctx["questions"])
        self.assertEqual(len(questions), 3)
        with self.assertNumQueries(0):
            for q in questions:
                _ = list(q.choices.all())

    def test_empty_state(self):
        Question.objects.all().delete()
        url = reverse("politics:test")
        response = self.client.get(url)
        self.assertEqual(list(response.context["questions"]), [])
