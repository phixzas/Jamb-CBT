from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import random
import requests
from .models import Subject, Question, Profile
from datetime import timedelta
from django.utils import timezone


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


# ================= AUTH =================

def register_user(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        full_name = request.POST.get("full_name")
        password = request.POST.get("password")
        referrer = request.POST.get("referrer")

        # CHECK USERNAME

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("register")

        # CHECK EMAIL

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        try:

            # CREATE USER

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=full_name,
                last_name=referrer if referrer else ""
            )

            user.is_active = False
            user.save()

            # CREATE PROFILE

            profile, created = Profile.objects.get_or_create(user=user)

            profile.full_name = full_name
            profile.email = email
            profile.referrer = referrer

            profile.save()

            # GENERATE VERIFICATION CODE

            code = str(random.randint(100000, 999999))

            request.session["verify_user"] = user.id
            request.session["verify_email"] = email
            request.session["verify_code"] = code

            # SEND EMAIL

            send_mail(
                "Your Verification Code",
                f"Your code is: {code}",
                "phixzas60@gmail.com",
                [email],
                fail_silently=False
            )

            messages.success(
                request,
                "Account created successfully! Check your email for verification code."
            )

            return redirect("verify")

        except Exception as e:

            print("REGISTRATION ERROR:", e)

            messages.error(request, f"Registration failed: {str(e)}")

            return redirect("register")

    return render(request, "auth/register.html")


# ================= LOGIN =================

def login_user(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            if not user.is_active:
                messages.error(request, "Please verify your email first")
                return redirect("login")

            login(request, user)

            profile = user.profile

            if profile.subscription_expiry and profile.subscription_expiry < timezone.now():
                profile.is_subscribed = False
                profile.save()

            messages.success(request, f"Welcome {user.username}")

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

        messages.error(request, "Session expired. Please register again.")

        return redirect("register")

    user = User.objects.filter(id=user_id).first()

    if not user:
        return redirect("register")

    if request.method == "POST":

        code = request.POST.get("code")

        if code == saved_code:

            user.is_active = True
            user.save()

            request.session.pop("verify_user", None)
            request.session.pop("verify_code", None)
            request.session.pop("verify_email", None)

            messages.success(
                request,
                "Email verified successfully! You can now login."
            )

            return redirect("login")

        messages.error(request, "Invalid code. Try again.")

    return render(request, "auth/verify.html")


# ================= RESEND CODE =================

def resend_code(request):

    user_id = request.session.get("verify_user")

    if not user_id:
        return redirect("login")

    user = User.objects.get(id=user_id)

    code = str(random.randint(100000, 999999))

    request.session["verify_code"] = code

    send_mail(
        "New Verification Code",
        f"Your new code is: {code}",
        "phixzas60@gmail.com",
        [user.email],
        fail_silently=False
    )

    messages.success(request, "New verification code sent to your email")

    return redirect("verify")


# ================= HOME =================

def home(request):

    return render(request, "exams/home.html")


# ================= SUBJECTS =================

def subjects(request):

    subjects = Subject.objects.exclude(name__iexact="use of english")

    return render(
        request,
        "exams/subjects.html",
        {"subjects": subjects}
    )


# ================= PAST QUESTIONS =================

def past_questions(request, subject_id):

    subject = get_object_or_404(Subject, id=subject_id)

    all_questions = Question.objects.filter(subject=subject).order_by('id')

    page_number = request.GET.get('page', 1)

    try:
        page_number = int(page_number)
    except:
        page_number = 1

    per_page = 15

    start = (page_number - 1) * per_page
    end = start + per_page

    questions = all_questions[start:end]

    total_questions = all_questions.count()

    total_pages = (total_questions + per_page - 1) // per_page

    context = {
        'subject': subject,
        'questions': questions,
        'current_page': page_number,
        'total_pages': total_pages,
        'has_next': page_number < total_pages,
        'has_previous': page_number > 1,
        'total_questions': total_questions,
    }

    return render(
        request,
        "exams/past_questions.html",
        context
    )


# ================= MOCK TEST =================

@subscription_required
def mock_test(request):

    subjects = Subject.objects.exclude(name__icontains="english")

    return render(
        request,
        "exams/mock_test.html",
        {"subjects": subjects}
    )


# ================= COUNSELING =================

@subscription_required
def counseling(request):

    return render(request, "exams/counseling.html")


# ================= START MOCK =================

@subscription_required
def start_mock(request):

    if request.method == "POST":

        selected_subject_ids = request.POST.getlist("subjects")

        subject_questions = {}

        exam_question_ids = []

        english = Subject.objects.filter(
            name__iexact="use of english"
        ).first()

        if english:

            english_questions = Question.objects.filter(
                subject=english
            ).order_by('?')[:60]

            subject_questions[english] = english_questions

            for q in english_questions:
                exam_question_ids.append(q.id)

        for sid in selected_subject_ids:

            try:

                subject = Subject.objects.get(id=sid)

                if english and subject.id == english.id:
                    continue

                questions = Question.objects.filter(
                    subject=subject
                ).order_by('?')[:40]

                subject_questions[subject] = questions

                for q in questions:
                    exam_question_ids.append(q.id)

            except Subject.DoesNotExist:
                continue

        request.session["exam_questions"] = exam_question_ids

        return render(
            request,
            "exams/mock_exam.html",
            {
                "subject_questions": subject_questions,
            }
        )

    return redirect("mock_test")


# ================= SUBMIT MOCK =================

@subscription_required
def submit_mock(request):

    if request.method == "POST":

        exam_question_ids = request.session.get("exam_questions", [])

        subject_scores = {}
        subject_totals = {}

        for qid in exam_question_ids:

            try:

                q = Question.objects.get(id=qid)

                subject_name = q.subject.name.strip()

                subject_scores.setdefault(subject_name, 0)
                subject_totals.setdefault(subject_name, 0)

                subject_totals[subject_name] += 1

                user_answer = request.POST.get(str(q.id))

                if user_answer == q.correct_option:
                    subject_scores[subject_name] += 1

            except Question.DoesNotExist:
                continue

        results = {}

        total_score = 0

        for subject in subject_scores:

            total = subject_totals.get(subject, 0)

            correct = subject_scores.get(subject, 0)

            score = round((correct / total) * 100) if total else 0

            results[subject] = score

            total_score += score

        request.session.pop("exam_questions", None)

        return render(
            request,
            "exams/result.html",
            {
                "results": results,
                "total_score": total_score
            }
        )

    return redirect("home")


# ================= PAYMENT =================

@login_required
def payment_page(request):

    plan = request.GET.get("plan")

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
        "callback_url": request.build_absolute_uri("/exams/paystack/verify/"),
        "metadata": {
            "plan": plan
        }
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

        messages.success(
            request,
            "Payment successful! Subscription activated"
        )

        return redirect("home")

    messages.error(request, "Payment verification failed")

    return redirect("payment_page")