from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .forms import EmailAccountForm
from .models import EmailAccount, Message
from .utils import fetch_emails


def get_email_account(request):
    if request.method == 'POST':
        form = EmailAccountForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            hashed_password = make_password(password)

            email_account, created = EmailAccount.objects.get_or_create(
                email=email,
                defaults={'password': hashed_password, 'provider': form.cleaned_data.get('provider')}
            )

            channel_name = request.session.session_key
            if not channel_name:
                print("Session key is None. Setting default channel name.")
                channel_name = "default_channel"

            fetch_emails(email, password, channel_name)

            return redirect('message_list')
    else:
        form = EmailAccountForm()

    return render(request, 'emails/email_account_form.html', {'form': form})


def message_list(request):
    messages = Message.objects.all()
    return render(request, 'emails/message_list.html', {'messages': messages})
