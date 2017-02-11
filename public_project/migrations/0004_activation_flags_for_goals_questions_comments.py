# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public_project', '0003_removed_null_on_manytomany'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfig',
            name='activate_comments',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='siteconfig',
            name='show_goals_category',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='siteconfig',
            name='show_questions_category',
            field=models.BooleanField(default=True),
        ),
    ]
