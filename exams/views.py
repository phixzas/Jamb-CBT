from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from datetime import timedelta

from .models import Subject, Question, Profile

import random
import requests
import traceback


# ================= CUSTOM DECORATOR =================

def subscription_required(view_func):
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            messages.error(request, "Please login first")
            return redirect("login")

        profile = getattr(request.user, "profile", None)

        if not profile or not profile.is_subscribed:
            messages.error(request, "Please subscribe to continue")
            return redirect("payment_page")

        if profile.subscription_expiry and profile.subscription_expiry < timezone.now():
            profile.is_subscribed = False
            profile.save()
            messages.error(request, "Your subscription has expired")
            return redirect("payment_page")

        return view_func(request, *args, **kwargs)

    return wrapper


# ================= REGISTER =================

def register_user(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        full_name = request.POST.get("full_name")
        password = request.POST.get("password")
        referrer = request.POST.get("referrer")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=full_name,
                last_name=referrer if referrer else ""
            )

            user.is_active = False
            user.save()

            profile, _ = Profile.objects.get_or_create(user=user)
            profile.full_name = full_name
            profile.email = email
            profile.referrer = referrer
            profile.save()

            # OTP
            code = str(random.randint(100000, 999999))

            request.session["verify_user"] = user.id
            request.session["verify_email"] = email
            request.session["verify_code"] = code

            try:
                send_mail(
                    "Your Verification Code",
                    f"Your code is: {code}",
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=True
                )
            except Exception as e:
                print("EMAIL ERROR:", e)

            messages.success(request, "Account created! Check your email for code.")
            return redirect("verify")

        except Exception as e:
            print(str(e))
            traceback.print_exc()
            messages.error(request, f"Registration failed: {str(e)}")
            return redirect("register")

    return render(request, "auth/register.html")


# ================= LOGIN =================

def login_user(request):

    if request.method == "POST":

        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        if user:

            if not user.is_active:
                messages.error(request, "Verify your email first")
                return redirect("login")

            login(request, user)

            profile = user.profile

            if profile.subscription_expiry and profile.subscription_expiry < timezone.now():
                profile.is_subscribed = False
                profile.save()

            return redirect("home")

        messages.error(request, "Invalid login details")
        return redirect("login")

    return render(request, "auth/login.html")


# ================= LOGOUT =================

def logout_user(request):
    logout(request)
    return redirect("login")


# ================= VERIFY EMAIL =================

def verify_email(request):

    user_id = request.session.get("verify_user")
    saved_code = request.session.get("verify_code")

    if not user_id or not saved_code:
        messages.error(request, "Session expired")
        return redirect("register")

    user = User.objects.filter(id=user_id).first()

    if request.method == "POST":

        code = request.POST.get("code")

        if code == saved_code:

            user.is_active = True
            user.save()

            request.session.pop("verify_user", None)
            request.session.pop("verify_email", None)
            request.session.pop("verify_code", None)

            return redirect("login")

        messages.error(request, "Invalid code")

    return render(request, "auth/verify.html")


# ================= RESEND CODE =================

def resend_code(request):

    user_id = request.session.get("verify_user")

    if not user_id:
        return redirect("register")

    user = User.objects.get(id=user_id)

    code = str(random.randint(100000, 999999))
    request.session["verify_code"] = code

    send_mail(
        "New Verification Code",
        f"Your new code is: {code}",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=True
    )

    return redirect("verify")


# ================= HOME =================

def home(request):
    return render(request, "exams/home.html")


# ================= SUBJECTS =================

def subjects(request):
    subjects = Subject.objects.exclude(name__iexact="use of english")
    return render(request, "exams/subjects.html", {"subjects": subjects})


# ================= PAYMENT =================

@login_required
def payment_page(request):

    # ✅ FIXED SESSION PLAN HANDLING
    plan = request.GET.get("plan")

    if plan:
        request.session["plan"] = plan
    else:
        plan = request.session.get("plan")

    if not plan:
        return render(request, "exams/payment.html")

    if plan not in ["monthly", "yearly"]:
        messages.error(request, "Invalid plan selected")
        return redirect("payment_page")

    amount = 1000 * 100 if plan == "monthly" else 5000 * 100

    url = "https://api.paystack.co/transaction/initialize"

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "email": request.user.email,
        "amount": amount,
        "callback_url": request.build_absolute_uri(reverse("paystack_verify")),
        "metadata": {"plan": plan}
    }

    response = requests.post(url, json=data, headers=headers)
    res = response.json()

    if res.get("status"):
        return redirect(res["data"]["authorization_url"])

    messages.error(request, "Payment initialization failed")
    return redirect("home")


# ================= VERIFY PAYMENT =================

@login_required
def paystack_verify(request):

    reference = request.GET.get("reference")

    if not reference:
        messages.error(request, "Missing payment reference")
        return redirect("payment_page")

    url = f"https://api.paystack.co/transaction/verify/{reference}"

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }

    response = requests.get(url, headers=headers)
    res = response.json()

    print(res)  # DEBUG

    if res.get("status") and res["data"]["status"] == "success":

        profile = request.user.profile
        plan = res["data"].get("metadata", {}).get("plan", "monthly")

        profile.is_subscribed = True
        profile.subscription_type = plan

        if plan == "monthly":
            profile.subscription_expiry = timezone.now() + timedelta(days=30)
        else:
            profile.subscription_expiry = timezone.now() + timedelta(days=365)

        profile.save()

        messages.success(request, "Payment successful!")
        return redirect("home")

    messages.error(request, "Payment verification failed")
    return redirect("payment_page")