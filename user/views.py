from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse

from .forms import CustomRegistrationForm
from .models import CustomUser
from .utils import send_email


def index(request):
    return render(request, 'index.html')


def user_sign_up(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)

            email_subject = 'Activate Your Account'
            message = render_to_string('activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uuid': user.id,
            })
            to_email = form.cleaned_data.get('email')

            send_email(email_subject, message, [to_email])
            group = Group.objects.get(name='Users')
            user.groups.add(group)

            messages.success(request,
                             'We have sent you an email, please confirm your '
                             'email address to complete the registration.')
            return redirect(reverse('home-page'))
    else:
        form = CustomRegistrationForm()
    return render(request, 'django_registration/registration_form.html', {'form': form})


def activate_account(request, uuid):
    try:
        user = CustomUser.objects.filter(id=uuid).first()
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None:
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Your account has been activate successfully. You are sign in automatically')
        return redirect(reverse('home-page'))
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect(reverse('home-page'))
