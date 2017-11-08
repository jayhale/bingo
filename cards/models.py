from random import shuffle

from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

MAX_SQUARES = 24

ORDER_CHOICES = tuple(range(0, MAX_SQUARES))

ORDER_LIST_SEPARATOR = ','


class CardSquare(models.Model):
    """Stores the status of a Square for each Card"""
    card = models.ForeignKey('Card', on_delete=models.CASCADE)
    square = models.ForeignKey('Square', on_delete=models.CASCADE)
    checked = models.BooleanField(default=False)


class Week(models.Model):
    """Stores a Week, into which Squares are grouped"""
    name = models.CharField(max_length=128)
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Week, self).save(*args, **kwargs)

        # Ensure everyone has a card
        for user in get_user_model().objects.all():
            if not Card.objects.filter(user=user, week=self).exists():
                Card.objects.create(user=user, week=self)

        return self


class Card(models.Model):
    """
    Stores the order in which Squares should be populated into a Card for each
    User
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    order = models.CharField(max_length=128, blank=True)


    class Meta:
        unique_together = (('user', 'week'),)


    def __str__(self):
        return str(self.week.start)


    def clean(self, *args, **kwargs):
        if self.order:
            keys = self.order.split(ORDER_LIST_SEPARATOR)

            # Check that the right number of keys are present
            if not len(keys) == len(ORDER_CHOICES):
                raise ValidationError({'order': ('Card order does contains '
                    'incorrect number of keys: {}').format(len(keys))})

            # Check that each key appears once and only once
            for key in ORDER_CHOICES:
                if not keys.count(str(key)) == 1:
                    raise ValidationError({'order': ('Card order does not '
                        'contain key {} exactly 1 time: present {} times'
                        ).format(key, keys.count(str(key)))})

        return super(Card, self).clean(self, *args, **kwargs)
            

    def save(self, *args, **kwargs):
        # Set the order
        if not self.order:
            choices = [str(c) for c in ORDER_CHOICES]
            shuffle(choices)
            self.order = ORDER_LIST_SEPARATOR.join(choices)

        super(Card, self).save(*args, **kwargs)

        # Ensure every square is associated
        for square in self.week.square_set.all():
            if not CardSquare.objects.filter(card=self, square=square).exists():
                CardSquare.objects.create(card=self, square=square)

        return self


class Square(models.Model):
    """Stores a Square for a given Week"""
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    content = models.CharField(max_length=254)
    order = models.PositiveSmallIntegerField()


    class Meta:
        unique_together = (('week', 'order'),)


    def __str__(self):
        return self.content


    def clean(self, *args, **kwargs):
        if not self.pk:
            # Check to make sure we're not adding too many squares to the week
            if Square.objects.filter(week=self.week).count() >= MAX_SQUARES:
                raise ValidationError(('Unable to save another square for '
                    'week starting {:%Y-%m-%d}, there are already {} '
                    'squares').format(self.week.start, MAX_SQUARES))

        return super(Card, self).clean(*args, **kwargs)


    def save(self, *args, **kwargs):
        if not self.order:
            # Increment self.order within week
            self.order = 0
            prev_squares = Square.objects.filter(week=self.week)
            if prev_squares:
                self.order = prev_squares.aggregate(models.Max('order')) + 1
        
        super(Square, self).save(*args, **kwargs)

        # Ensure every card has the square
        for card in self.week.card_set.all():
            if not CardSquare.objects.filter(card=card, week=self.week):
                CardSquare.objects.create(card=card, week=self.week)

        return self
