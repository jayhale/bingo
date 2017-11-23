from django.conf.urls import url

from ideas.views import ( ajax_new_center_square_idea, ajax_new_square_idea, 
    ajax_new_center_square_vote, ajax_new_square_vote )


urlpatterns = [
    url(r'^centersquare/new/$', ajax_new_center_square_idea, 
        name='ajax_new_center_square_idea'),
    url(r'^sqauare/new/$', ajax_new_square_idea,
        name='ajax_new_square_idea'),
    url(r'^centersquare/vote/$', ajax_new_center_square_vote,
        name='ajax_new_center_square_vote'),
    url(r'^square/vote/$', ajax_new_square_vote,
        name='ajax_new_square_vote'),
]