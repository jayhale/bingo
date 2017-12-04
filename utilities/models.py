from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models


class Announcement(models.Model):
    """Stores a site-wide announcement"""
    
    title = models.CharField(max_length=254)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    expires_on = models.DateTimeField()
    submitted_by = models.ForeignKey(get_user_model(),
        on_delete=models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return self.content


    @classmethod
    def get_current_announcements(cls):
        return cls.objects.filter(expires_on__gt=datetime.now())
