from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from cards.models import Card, Week

User = get_user_model()


def index(request, user_pk, template_name='cards/index.html'):
    try:
        user = User.objects.get(pk=user_pk)
        users = User.objects.all()
        cards = Card.objects.filter(user=user)
    except (User.DoesNotExist, Card.DoesNotExist):
        raise Http404('The cards you\'re looking for could not be found')

    return render(request, template_name, {'user': user, 'users': users, 
        'cards': cards})


def card(request, user_pk, week_pk, template_name='cards/card.html'):
    try:
        user = User.objects.get(pk=user_pk)
        week = Week.objects.get(pk=week_pk)
        users = User.objects.all()
        cards = Card.objects.filter(user=user)
    except (User.DoesNotExist, Card.DoesNotExist, Week.DoesNotExist):
        raise Http404('The card you\'re looking for could not be found')

    # If a card doesn't exist for this user in this week yet, create it
    try:
        card = Card.objects.filter(user=user, week=week)
    except Card.DoesNotExist:
        card = Card(user=user, week=week)
        card.save()

    return render(request, template_name, {'card': card, 'user': user,
        'week': week, 'users': users, 'cards': cards})
