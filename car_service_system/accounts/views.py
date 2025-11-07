from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from functools import wraps
from .models import UserProfile
from accounts.forms import SignupForm,UserProfileForm,SelectRoleForm
from .utils import set_user_otp, send_otp_email, verify_otp_code

# Create your views here.

def home(request):
    return render(request, 'accounts/home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password = password)
        if user is not None:
            if not getattr(user, 'is_email_verified', False):
                code = set_user_otp(user)
                send_otp_email(user, code)
                request.session['pending_verify_username'] = user.username
                messages.info(request, 'Please verify your account with the OTP sent to your email.')
                return redirect('accounts:verify_otp')
            login(request,user)
            return redirect('accounts:redirect_after_login')
        else:
            messages.error(request, 'Invalid username or password. ')
    
     # Create a simple form for error handling
    from django.contrib.auth.forms import AuthenticationForm
    form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})
    

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data['email']
            user.is_active = True
            user.is_email_verified = False
            user.save(update_fields=['email', 'is_active', 'is_email_verified'])
            user.role = form.cleaned_data['role']
            user.save(update_fields=['role'])
            code = set_user_otp(user)
            send_otp_email(user, code)
            request.session['pending_verify_username'] = user.username
            messages.success(request, 'Account created. Enter the OTP sent to your email to verify.')
            return redirect('accounts:verify_otp')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignupForm()

    # ✅ Always return response for both GET and invalid POST
    return render(request, 'accounts/signup.html', {'form': form})

    

@login_required
def redirect_after_login(request):    # If user picked a role on login, honor it and persist
    selected = request.GET.get('selected_role')
    if selected in dict(UserProfile.ROLE_CHOICES):
        request.user.role = selected
        request.user.save(update_fields = ['role'])
        role = selected
    else:
        try:
            role = request.user.role
        except Exception:
            return redirect('accounts:select_role')
    
    if role == UserProfile.ROLE_CUSTOMER:
        return redirect('customer_portal')
    if role == UserProfile.ROLE_GARAGE:
        return redirect('garage_dashboard')
    return redirect('/')


def custom_logout(request):
    logout(request)
    messages.success(request, 'Nikkall jaldii yhasee.')
    return redirect('/')

@login_required
def select_role(request):
    try:
        profile = request.user
    except Exception:
        profile = request.user
    if request.method == 'POST':
        form = SelectRoleForm(request.POST)
        if form.is_valid():
            profile.role = form.cleaned_data['role']
            profile.save(update_fields =['role'])
            return redirect('accounts:redirect_after_login')
    else:
        form = SelectRoleForm(initial={'role': getattr(profile, 'role', UserProfile.ROLE_CUSTOMER)})
    return render(request, 'accounts/select_role.html', {'form': form})


def verify_otp(request):
    # Try session first, then accept ?u=username as fallback to avoid accidental redirects
    username = request.session.get('pending_verify_username') or request.GET.get('u')
    if not username:
        messages.info(request, 'Start verification from signup or login.')
        return redirect('accounts:user_login')
    try:
        user = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('accounts:user_login')

    if request.method == 'POST':
        code = request.POST.get('otp')
        if verify_otp_code(user, code):
            user.is_email_verified = True
            user.otp_code = None
            user.otp_expires_at = None
            user.save(update_fields=['is_email_verified', 'otp_code', 'otp_expires_at'])
            request.session.pop('pending_verify_username', None)
            messages.success(request, 'Your account is verified.')
            login(request, user)
            return redirect('accounts:redirect_after_login')
        else:
            messages.error(request, 'Invalid or expired code. Please try again.')

    return render(request, 'accounts/verify_otp.html', {'username': username})


def resend_otp(request):
    username = request.session.get('pending_verify_username')
    if not username:
        return redirect('accounts:user_login')
    try:
        user = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        return redirect('accounts:user_login')
    code = set_user_otp(user)
    send_otp_email(user, code)
    messages.info(request, 'A new OTP has been sent to your email.')
    return redirect('accounts:verify_otp')


def forgot_password(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier', '').strip()
        user = None
        if identifier:
            try:
                user = UserProfile.objects.get(username=identifier)
            except UserProfile.DoesNotExist:
                try:
                    user = UserProfile.objects.get(email=identifier)
                except UserProfile.DoesNotExist:
                    user = None
        if user is None:
            messages.error(request, 'User not found. Enter valid username or email.')
        else:
            code = set_user_otp(user)
            send_otp_email(user, code)
            request.session['pwd_reset_user'] = user.username
            messages.info(request, 'OTP sent to your registered email.')
            return redirect('accounts:forgot_password_verify')
    return render(request, 'accounts/forgot_password_request.html')


def forgot_password_verify(request):
    username = request.session.get('pwd_reset_user')
    if not username:
        return redirect('accounts:forgot_password')
    try:
        user = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        return redirect('accounts:forgot_password')

    if request.method == 'POST':
        code = request.POST.get('otp')
        if verify_otp_code(user, code):
            request.session['pwd_reset_verified'] = True
            messages.success(request, 'OTP verified. Set your new password.')
            return redirect('accounts:forgot_password_reset')
        else:
            messages.error(request, 'Invalid or expired code.')

    return render(request, 'accounts/forgot_password_verify.html', { 'username': username })


def resend_reset_otp(request):
    username = request.session.get('pwd_reset_user')
    if not username:
        return redirect('accounts:forgot_password')
    try:
        user = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        return redirect('accounts:forgot_password')
    code = set_user_otp(user)
    send_otp_email(user, code)
    messages.info(request, 'A new OTP has been sent to your email.')
    return redirect('accounts:forgot_password_verify')


def forgot_password_reset(request):
    username = request.session.get('pwd_reset_user')
    verified = request.session.get('pwd_reset_verified')
    if not username or not verified:
        return redirect('accounts:forgot_password')
    try:
        user = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        return redirect('accounts:forgot_password')

    if request.method == 'POST':
        p1 = request.POST.get('password1')
        p2 = request.POST.get('password2')
        if not p1 or p1 != p2:
            messages.error(request, 'Passwords do not match.')
        else:
            user.set_password(p1)
            user.otp_code = None
            user.otp_expires_at = None
            user.save(update_fields=['password', 'otp_code', 'otp_expires_at'])
            # clear session flags
            for k in ['pwd_reset_user', 'pwd_reset_verified']:
                request.session.pop(k, None)
            messages.success(request, 'Password updated. Please log in.')
            return redirect('accounts:user_login')

    return render(request, 'accounts/forgot_password_reset.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Keep the user logged in after password change
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been updated.')
            return redirect('accounts:redirect_after_login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'accounts/change_password.html', {'form': form})
