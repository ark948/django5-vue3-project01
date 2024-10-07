from accounts.models import CustomUser, OneTimePassword
from django.conf import settings
from django.core.mail import EmailMessage
from accounts.utils.otp import generateOtp

def re_verify_email(id: int) -> None:
    user = CustomUser.objects.get(id=id)
    try:
        old_otp = OneTimePassword.objects.get(user=user)
    except Exception as e:
        old_otp = None
    if old_otp:
        OneTimePassword.objects.get(user=user).delete()
    send_code_to_user(user.email)

def send_code_to_user(email: str) -> None:
    Subject = "One Time passcode for email verification"
    otp_code = generateOtp()
    user = CustomUser.objects.get(email=email)
    current_site = "MyAuth.com"
    email_body = f'Hi {user.email}, thanks for signing up on {current_site}. \n plese verify your email with this one time password {otp_code}'
    from_email = settings.DEFAULT_FROM_EMAIL

    OneTimePassword.objects.create(user=user, code=otp_code)
    d_email = EmailMessage(
        subject=Subject,
        body=email_body,
        from_email=from_email,
        to=[email],
    )
    d_email.send(fail_silently=True)

def send_normal_email(data: set) -> None:
    email = EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=['admin@example.com'],
        to=[data['to_email']]
    )
    email.send()