from django.db import models
from django.utils import timezone


class Question(models.Model):
    text = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Q{self.order}: {self.text[:50]}"


class Choice(models.Model):
    QUESTION_CHOICES = [
        ("A", "A"),
        ("B", "B"),
        ("Both", "Both"),
        ("Neither", "Neither"),
    ]
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices"
    )
    label = models.CharField(max_length=10, choices=QUESTION_CHOICES)
    text = models.CharField(max_length=255)

    class Meta:
        unique_together = ("question", "label")

    def __str__(self):
        return f"Q{self.question.order} {self.label}: {self.text[:40]}"


class Politician(models.Model):
    name = models.CharField(max_length=100)
    x = models.FloatField(help_text="-1.0 left, +1.0 right")
    y = models.FloatField(help_text="-1.0 authoritarian, +1.0 libertarian")
    blurb = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TestSubmission(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    answers = models.JSONField(default=dict)
    x = models.FloatField(default=0.0)
    y = models.FloatField(default=0.0)

    def __str__(self):
        return f"Submission {self.pk} @ {self.created_at:%Y-%m-%d %H:%M}"
