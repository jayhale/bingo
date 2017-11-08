# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-08 21:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.CharField(blank=True, max_length=128)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CardSquare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checked', models.BooleanField(default=False)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.Card')),
            ],
        ),
        migrations.CreateModel(
            name='Square',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=254)),
                ('order', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('start', models.DateField()),
                ('end', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='square',
            name='week',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.Week'),
        ),
        migrations.AddField(
            model_name='cardsquare',
            name='square',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.Square'),
        ),
        migrations.AddField(
            model_name='card',
            name='week',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.Week'),
        ),
        migrations.AlterUniqueTogether(
            name='square',
            unique_together=set([('week', 'order')]),
        ),
        migrations.AlterUniqueTogether(
            name='card',
            unique_together=set([('user', 'week')]),
        ),
    ]
