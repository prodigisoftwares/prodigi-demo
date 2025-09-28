from django.contrib import admin
from .models import Politician, Question, Choice


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("order", "text")
    ordering = ("order",)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("question", "label", "text")
    list_filter = ("question",)


@admin.register(Politician)
class PoliticianAdmin(admin.ModelAdmin):
    list_display = ("name", "x", "y")
    search_fields = ("name",)
