from django.contrib import admin
from .models import Subject, Question, Profile


# ================= PROFILE ADMIN =================

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "full_name",
        "email",
        "is_subscribed",
        "subscription_type",
        "subscription_expiry",
    )

    list_filter = ("is_subscribed", "subscription_type")
    search_fields = ("user__username", "email", "full_name")

    ordering = ("-subscription_expiry",)

    readonly_fields = ("subscription_expiry",)


# ================= SUBJECT ADMIN =================
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# ================= QUESTION ADMIN =================
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "year")
    list_filter = ("subject", "year")
    search_fields = ("question_text",)