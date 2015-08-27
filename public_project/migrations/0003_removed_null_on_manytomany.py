# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public_project', '0002_boolean_default_values'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='events',
            field=models.ManyToManyField(related_name='related_documents', verbose_name='Events', to='public_project.Event', blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='participants',
            field=models.ManyToManyField(related_name='related_documents', verbose_name='Participants', to='public_project.Participant', blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='project_parts',
            field=models.ManyToManyField(related_name='related_documents', verbose_name='Topics', to='public_project.ProjectPart', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(related_name='related_events', verbose_name='Participants', to='public_project.Participant', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='project_parts',
            field=models.ManyToManyField(related_name='related_events', verbose_name='Topics', to='public_project.ProjectPart', blank=True),
        ),
        migrations.AlterField(
            model_name='projectpart',
            name='main_project_parts',
            field=models.ManyToManyField(help_text="If you select another project part here, you'll make this a sub project part.", to='public_project.ProjectPart', verbose_name='Main Topic', blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='documents',
            field=models.ManyToManyField(related_name='related_documents', verbose_name='Documents', to='public_project.Document', blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='events',
            field=models.ManyToManyField(related_name='related_questions', verbose_name='Events', to='public_project.Event', blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='participants',
            field=models.ManyToManyField(related_name='related_questions', verbose_name='Participants', to='public_project.Participant', blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='project_parts',
            field=models.ManyToManyField(related_name='related_questions', verbose_name='Topics', to='public_project.ProjectPart', blank=True),
        ),
        migrations.AlterField(
            model_name='sitecategory',
            name='documents',
            field=models.ManyToManyField(related_name='related_site_categories', verbose_name='Documents', to='public_project.Document', blank=True),
        ),
    ]
