from django.shortcuts import render, redirect
from .models import User
from .forms import (UserRegisterForm,
                    UserUpdateForm,
                    ProfileUpdateForm, UserRegisterForm1)
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from users.tokens import account_activation_token
from django.http import HttpResponse


# Create your views here.

def user_dashboard(request):
    user = User.objects.filter(username=request.user).first()
    if not user.profile.has_full_profile:
        return redirect('users:register-complete')
    return render(request, 'users/user_dashboard.html', {'user': user})


def register_complete(request):
    form = UserRegisterForm1()
    if request.method == 'POST':
        form = UserRegisterForm1(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.has_full_profile = True
            user.save()
            messages.success(request, f'registration completed')
            redirect('user_dashboard')
        form = UserRegisterForm1(request.POST)

    return render(request, 'users/register_complete.html', {'form': form})


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Loan Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            user.email_user(subject, message)
            messages.info(request, f'account created for {username}')
            return redirect('users:user_account_activation_sent')

    form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        return redirect('/')

    else:
        return render(request, 'registration/account_activation_invalid.html')


def user_account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')


def profile(request):
    if request.method == 'POST':
        user = User.objects.filter(username=request.user).first()
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            user.profile.has_full_profile = True
            user.save()
            messages.success(request, f'Your account has been created completely')
            return redirect('user-dashboard')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/client_profile.html', context)
