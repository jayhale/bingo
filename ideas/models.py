from django.contrib.auth import get_user_model
from django.db import models


class Idea(models.Model):
    content = models.CharField(max_length=254)
    submitted_by = models.ForeignKey(get_user_model(),
        on_delete=models.SET_NULL, blank=True, null=True)
    submitted_on = models.DateTimeField(auto_now_add=True)


    class Meta:
        abstract = True


    def __str__(self):
        return self.content


    def negative_vote_count(self):
        return self.votes.filter(positive=False).count()


    def positive_vote_count(self):
        return self.votes.filter(positive=True).count()


    def save(self, *args, **kwargs):
        super(SquareIdea, self).save(*args, **kwargs)
        self.votes.create(user=self.submitted_by)


class Vote(models.Model):
    """Stores a vote for a center square idea"""
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    positive = models.BooleanField(default=True)
    submitted_on = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True


    def is_negative(self):
        return not self.positive


    def is_positive(self):
        return self.positive


class CenterSquareIdea(Idea):
    """Stores an idea for the center square"""
    pass


class CenterSquareVote(Vote):
    """Stores a vote for a center square idea"""
    idea = models.ForeignKey(CenterSquareIdea, on_delete=models.CASCADE,
        related_name='votes')


    class Meta:
        unique_together = (('user', 'idea'),)


class SquareIdea(Idea):
    """Stores an idea for a non-center square"""
    pass


class SquareVote(Vote):
    """Sotres a vote for a non-center square"""
    idea = models.ForeignKey(SquareIdea, on_delete=models.CASCADE,
        related_name='votes')


    class Meta:
        unique_together = (('user', 'idea'),)
