from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse

from sesame import utils

from accounts.forms import LoginForm

User = get_user_model()


def login(request, template_name='registration/login.html'):
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            subject = getattr(settings, 'NOPASSWORD_EMAIL_SUBJECT', 'Login')
            next_url = getattr(settings, 'NOPASSWORD_NEXT_URL', 'cards')
            from_email = settings.FROM_EMAIL
            to_email = request.POST.get('email')
            try:
                user = User.objects.get(email=to_email)
            except User.DoesNotExist:
                messages.error(request, 'There was a problem logging in')
                return render(request, template_name, {'form': form})

            login_url = request.build_absolute_uri(str(reverse(next_url)) + \
                utils.get_query_string(user))
            context = {'url': login_url}
            text_content = render_to_string(
                'registration/login_email.txt',
                context
            )
            html_content = render_to_string(
                'registration/login_email.html',
                context
            )

            msg = EmailMultiAlternatives(
                subject, text_content, from_email, (to_email,)
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()

            messages.success(
                request,
                'Please check your email for a login link'
            )

    return render(request, template_name, {'form': form})