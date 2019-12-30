from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from eventex.subscriptions.form import SubscriptionForm
from eventex.subscriptions.models import Subscription

def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)


def create(request):
    form = SubscriptionForm(request.POST)
    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html', {'form': form})

    # send email
    _send_mail('Confirmação de inscrição', settings.DEFAULT_FROM_EMAIL, form.cleaned_data['email'], form.cleaned_data,
               'subscriptions/subscription_email.txt')

    Subscription.objects.create(**form.cleaned_data)
    # success email
    messages.success(request, 'Inscrição realizada com sucesso')
    return HttpResponseRedirect('/inscricao/')


def new(request):
    return render(request, 'subscriptions/subscription_form.html', {'form': SubscriptionForm()})


def _send_mail(subject, from_, to, context, template_name):
    msg_email = render_to_string(template_name, context)
    mail.send_mail(subject, msg_email, from_, [from_, to])
