# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public_project', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='important',
            field=models.BooleanField(default=False, help_text='Event being of central importance for the project.', verbose_name='Main Event'),
        ),
        migrations.AlterField(
            model_name='question',
            name='answered',
            field=models.BooleanField(default=False, verbose_name='Answered'),
        ),
        migrations.AlterField(
            model_name='siteconfig',
            name='contact_text',
            field=models.TextField(default='Contact HTML Default', help_text='Html to be displayed on the contact page, provide at least an adress there and some contact information.', verbose_name='Contact'),
        ),
        migrations.AlterField(
            model_name='siteconfig',
            name='footer',
            field=models.TextField(default='Footer HTML Default', help_text='Some html text you want to use in the footer of the page, you can e.g. provide a link to your email adress or associated social media sites.', verbose_name='Footer'),
        ),
        migrations.AlterField(
            model_name='siteconfig',
            name='short_title',
            field=models.CharField(default='Project Website Short Title', help_text='Short version of the title, used e.g. in emails.', max_length=250, verbose_name='Short title'),
        ),
        migrations.AlterField(
            model_name='siteconfig',
            name='title',
            field=models.CharField(default='Project Website Title', help_text='Main title, shown in the header navi.', max_length=250, verbose_name='Title'),
        ),
    ]
