from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import render

from ideas.models import ( CenterSquareIdea, SquareIdea, CenterSquareVote,
    SquareVote )


@login_required
def ajax_new_center_square_idea(request):
    if not request.method == 'POST':
        return Http404('')

    if not request.POST.get('content', None):
        return JsonResponse({
            'errors': True,
            'error_message': 'Unable to create a blank center square idea'
        })

    idea = CenterSquareIdea(
        content=request.POST['content'],
        submitted_by=request.user
    )
    idea.save()

    return JsonResponse({
        'success': True,
        'content': idea.content,
        'submitted_by': idea.submitted_by.get_full_name(),
        'submitted_on': 'Just now',
        'upvotes': 1,
        'downvotes': 0
    })


@login_required
def ajax_new_square_idea(request):
    if not request.method == 'POST':
        return Http404('')

    if not request.POST.get('content', None):
        return JsonResponse({
            'errors': True,
            'error_message': 'Unable to create a blank center square idea'
        })

    idea = SquareIdea(
        content=request.POST['content'],
        submitted_by=request.user
    )
    idea.save()

    return JsonResponse({
        'success': True,
        'content': idea.content,
        'submitted_by': idea.submitted_by.get_full_name(),
        'submitted_on': 'Just now',
        'upvotes': 1,
        'downvotes': 0
    })


@login_required
def ajax_new_center_square_vote(request):
    if not request.method == 'POST':
        return Http404('')

    try:
        idea = CenterSquareIdea.objects.get(pk=request.POST.get('idea', None))
    except CenterSquareIdea.DoesNotExist:
        return JsonResponse({
            'errors': True,
            'error_message': 'Unable to find idea'
        })

    # If the user has already voted on this idea, toggle the vote
    if idea.votes.filter(user=request.user).exists():
        vote = idea.votes.get(user=request.user)
        if ( request.POST.get('vote_type', None) == 'positive' and \
            vote.is_positive() ) or \
            ( request.POST.get('vote_type', None) == 'negative' and \
            vote.is_negative() ):
            return JsonResponse({
                'errors': True,
                'error_message': 'Your vote has already been cast'
            })
        elif request.POST.get('vote_type', None) in ('positive', 'negative'):
            vote.positive = not vote.is_positive()
            vote.save()
            return JsonResponse({
                'success': True,
                'idea': idea.pk,
                'vote_type': 'positive' if vote.is_positive() else 'negative',
                'positive_vote_count': idea.positive_vote_count(),
                'negative_vote_count': idea.negative_vote_count()
            })

    # If the user has yet to vote on the idea, create a vote
    if request.POST.get('vote_type', None) == 'positive':
        idea.votes.create(user=request.user, positive=True)
        return JsonResponse({
            'success': True,
            'idea': idea.pk,
            'vote_type': 'positive',
            'positive_vote_count': idea.positive_vote_count(),
            'negative_vote_count': idea.negative_vote_count()
        })

    elif request.POST.get('vote_type', None) == 'negative':
        idea.votes.create(user=request.user, positive=False)
        return JsonResponse({
            'success': True,
            'idea': idea.pk,
            'vote_type': 'negative',
            'positive_vote_count': idea.positive_vote_count(),
            'negative_vote_count': idea.negative_vote_count()
        })

    return JsonResponse({
        'errors': True,
        'error_message': 'Bad request'
    })


@login_required
def ajax_new_square_vote(request):
    if not request.method == 'POST':
        return Http404('')

    try:
        idea = SquareIdea.objects.get(pk=request.POST.get('idea', None))
    except CenterSquareIdea.DoesNotExist:
        return JsonResponse({
            'errors': True,
            'error_message': 'Unable to find idea'
        })

    # If the user has already voted on this idea, toggle the vote
    if idea.votes.filter(user=request.user).exists():
        vote = idea.votes.get(user=request.user)
        if ( request.POST.get('vote_type', None) == 'positive' and \
            vote.is_positive() ) or \
            ( request.POST.get('vote_type', None) == 'negative' and \
            vote.is_negative() ):
            return JsonResponse({
                'errors': True,
                'error_message': 'Your vote has already been cast'
            })
        elif request.POST.get('vote_type', None) in ('positive', 'negative'):
            vote.positive = not vote.is_positive()
            vote.save()
            return JsonResponse({
                'success': True,
                'idea': idea.pk,
                'vote_type': 'positive' if vote.is_positive() else 'negative',
                'positive_vote_count': idea.positive_vote_count(),
                'nevative_vote_count': idea.negative_vote_count()
            })

    # If the user has yet to vote on the idea, create a vote
    if request.POST.get('vote_type', None) == 'positive':
        idea.votes.create(user=request.user, positive=True)
        return JsonResponse({
            'success': True,
            'idea': idea.pk,
            'vote_type': 'positive',
            'positive_vote_count': idea.positive_vote_count(),
            'negative_vote_count': idea.negative_vote_count()
        })

    elif request.POST.get('vote_type', None) == 'negative':
        idea.votes.create(user=request.user, positive=False)
        return JsonResponse({
            'success': True,
            'idea': idea.pk,
            'vote_type': 'negative',
            'positive_vote_count': idea.positive_vote_count(),
            'negative_vote_count': idea.negative_vote_count()
        })

    return JsonResponse({
        'errors': True,
        'error_message': 'Bad request'
    })
