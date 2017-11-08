from django.shortcuts import render
from django.contrib.auth import get_user_model

def index(request, template_name='utilities/index.html'):
    users = get_user_model().objects.all()
    return render(request, template_name, {'users': users})