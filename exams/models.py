from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


# ================= SUBJECT =================
class Subject(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# ================= PROFILE =================
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    referrer = models.CharField(max_length=200, blank=True, null=True)

    verification_code = models.CharField(max_length=10, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    # ✅ PAYMENT FEATURE
    is_subscribed = models.BooleanField(default=False)

    # 🆕 SUBSCRIPTION PLAN SYSTEM
    subscription_type = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )  # "monthly" or "yearly"

    subscription_expiry = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username


# ================= QUESTION =================
class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)

    correct_option = models.CharField(max_length=1, choices=[
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D')
    ])

    year = models.IntegerField(null=True, blank=True)
    explanation = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.subject.name} - Q{self.id}"


# ================= RESULT =================
class Result(models.Model):
    user = models.CharField(max_length=100)
    score = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.score}"


# ================= AUTO CREATE PROFILE =================
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(
            user=instance,
            defaults={
                "full_name": instance.first_name,
                "email": instance.email
            }
        )