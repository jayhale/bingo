from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect

from cards.models import Card, Week, CardSquare
from ideas.models import CenterSquareIdea, SquareIdea

User = get_user_model()


@login_required
def index(request, template_name='cards/index.html'):
    try:
        cards = Card.objects.filter(user=request.user, week__published=True)
    except Card.DoesNotExist:
        return Http404('The cards you\'re looking for could not be found')

    center_square_ideas = CenterSquareIdea.objects.all()
    square_ideas = SquareIdea.objects.all()

    return render(request, template_name,
        {
            'cards': cards, 
            'center_square_ideas': center_square_ideas, 
            'square_ideas': square_ideas,
        }
    )


@login_required
def card(request, week_pk, template_name='cards/card.html'):
    week = get_object_or_404(Week, pk=week_pk, published=True)

    try:
        cards = Card.objects.filter(user=request.user)
    except Card.DoesNotExist:
        raise Http404('The cards you\'re looking for could not be found')

    # If a card doesn't exist for this user in this week yet, create it
    try:
        card = Card.objects.get(user=request.user, week=week)
    except Card.DoesNotExist:
        card = Card(user=user, week=week)
        card.save()

    toggle_square = request.GET.get('toggle_square', None)
    if toggle_square:
        card_square = get_object_or_404(CardSquare, pk=toggle_square)
        card_square.toggle()
        card_square.save()

    return render(request, template_name, {'card': card,
        'squares': card.get_ordered_squares() })


@login_required
def winner(request, week_pk, template_name='cards/winner.html'):
    week = get_object_or_404(Week, pk=week_pk, published=True)
    card = get_object_or_404(Card, week=week, user=week.winner)

    return render(request, template_name, {'card': card,
        'squares': card.get_ordered_squares(), 
        'square_progress_max': week.participating_count() })

