from django.urls import path
from . import views

urlpatterns = [

    # HOME
    path("", views.home, name="home"),

    # AUTH
    path("login/", views.login_user, name="login"),
    path("register/", views.register_user, name="register"),
    path("logout/", views.logout_user, name="logout"),

    # VERIFICATION
    path("verify/", views.verify_email, name="verify"),
    path("resend-code/", views.resend_code, name="resend_code"),

    # EXAMS
    path("subjects/", views.subjects, name="subjects"),
    path("past/<int:subject_id>/", views.past_questions, name="past_questions"),

    path("mock-test/", views.mock_test, name="mock_test"),
    path("start-mock/", views.start_mock, name="start_mock"),
    path("submit-mock/", views.submit_mock, name="submit_mock"),

    # COUNSELLING
    path("counselling/", views.counseling, name="counseling"),

    # PAYMENT
    path("payment/", views.payment_page, name="payment_page"),

    # PAYSTACK VERIFY
    path("paystack/verify/", views.paystack_verify, name="paystack_verify"),
]