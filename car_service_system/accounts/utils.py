
from functools import wraps
from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import random
from datetime import timedelta
from .models import UserProfile


def role_required(allowed_roles):
    if isinstance(allowed_roles, str):
        allowed = {allowed_roles}
    else:
        allowed = set(allowed_roles)

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:user_login')
            try:
                role = request.user.role
            except Exception:
                return redirect('accounts:user_login')
            if role not in allowed:
                return render(request, 'accounts/forbidden.html', status=403)
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


def generate_otp(length: int = 6) -> str:
    return ''.join(str(random.randint(0, 9)) for _ in range(length))


def set_user_otp(user: UserProfile, ttl_minutes: int = 10) -> str:
    code = generate_otp(6)
    user.otp_code = code
    user.otp_expires_at = timezone.now() + timedelta(minutes=ttl_minutes)
    user.save(update_fields=["otp_code", "otp_expires_at"])
    return code


def send_otp_email(user: UserProfile, code: str) -> None:
    if not user.email:
        return
    subject = "Your verification code"
    message = f"Hello {user.username},\n\nYour OTP code is: {code}. It expires in 10 minutes."
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or getattr(settings, "EMAIL_HOST_USER", None)
    try:
        send_mail(subject, message, from_email, [user.email], fail_silently=True)
    except Exception:
        # Fail silently in dev
        pass


def verify_otp_code(user: UserProfile, code: str) -> bool:
    if not user.otp_code or not user.otp_expires_at:
        return False
    if timezone.now() > user.otp_expires_at:
        return False
    return str(code).strip() == str(user.otp_code).strip()
