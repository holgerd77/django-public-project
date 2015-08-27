# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('type', models.CharField(max_length=2, verbose_name='Type', choices=[(b'NA', 'New Subject Area'), (b'NQ', 'New Question'), (b'PA', 'New Participant'), (b'NE', 'Event'), (b'ND', 'New Document'), (b'RR', 'Research Request'), (b'NC', 'Comment')])),
                ('info', models.CharField(max_length=250, verbose_name='Info', blank=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'Activity Log Entry',
                'verbose_name_plural': 'Activity Log',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=250, verbose_name='Username')),
                ('email', models.EmailField(max_length=250, verbose_name='Email')),
                ('feedback_allowed', models.BooleanField(default=False, help_text='User has given permission to get in contact via email.', verbose_name='Feedback allowed')),
                ('comment', models.TextField(verbose_name='Comment text')),
                ('published', models.BooleanField(default=False, help_text='Comment is only shown on page if published is true.', verbose_name='Published')),
                ('published_by', models.CharField(max_length=250, verbose_name='Published by', blank=True)),
                ('activation_hash', models.CharField(max_length=250, verbose_name='Activation hash', blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date_added'],
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommentRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField(help_text='The id of the related object (you can find the id of an object in the url of the object change form in the admin).')),
                ('page', models.IntegerField(help_text='Page number in document', null=True, verbose_name='Page', blank=True)),
                ('comment', models.ForeignKey(to='public_project.Comment')),
                ('content_type', models.ForeignKey(help_text='Type of the related object (ProjectPart, Question, Participant, Event, Document).', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Relation with Project Element',
                'verbose_name_plural': 'Relations with Project Elements',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='Title of the document', max_length=250, verbose_name='Title')),
                ('document', models.FileField(help_text='Document in pdf format', upload_to=b'documents', verbose_name='Document')),
                ('date', models.DateField(help_text='Date of creation of the document', verbose_name='Date')),
                ('description', models.TextField(help_text='Short description.', verbose_name='Description')),
                ('comments', models.TextField(verbose_name='Comments (internal)', blank=True)),
                ('pdf_images_generated', models.BooleanField(default=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date_added'],
                'verbose_name': 'Document',
                'verbose_name_plural': 'Documents',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250, verbose_name='Title')),
                ('event_type', models.CharField(max_length=2, verbose_name='Type', choices=[(b'ME', 'Meeting / Gathering / Session'), (b'IN', 'New Information / Decision / Statement'), (b'MI', 'Project Progress / Execution / Milestone'), (b'CI', 'Action by Civil Society'), (b'UE', 'Unplanned Event'), (b'SE', 'Miscellaneous')])),
                ('important', models.BooleanField(help_text='Event being of central importance for the project.', verbose_name='Main Event')),
                ('description', models.TextField(verbose_name='Description')),
                ('date', models.DateField(verbose_name='Date')),
                ('not_exact', models.BooleanField(default=False, help_text='Date is not exact (e.g. if a source refers only to the month)', verbose_name='Date not exact')),
                ('comments', models.TextField(verbose_name='Comments (internal)', blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250, verbose_name='Title')),
                ('image', models.ImageField(help_text='400px max width, 200px for images used with floating texts', upload_to=b'images', verbose_name='Image')),
                ('attribution', models.CharField(help_text="Attribution to the original image source or alternatively something like 'Own image'.", max_length=250, verbose_name='Attribution')),
                ('attribution_url', models.URLField(help_text='Link to the original image source (if available)', null=True, verbose_name='Attribution URL', blank=True)),
                ('comments', models.TextField(verbose_name='Comments (internal)', blank=True)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('function', models.CharField(help_text='Type or function of the membership or task or position of the participant.', max_length=50, null=True, verbose_name='Function', blank=True)),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Membership',
                'verbose_name_plural': 'Memberships',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField()),
                ('content', models.TextField(blank=True)),
                ('document', models.ForeignKey(to='public_project.Document')),
            ],
            options={
                'ordering': ['number'],
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Person, group or institution acting in some way in the context of the project or being affected by the process or the result of the project execution.', unique=True, max_length=250, verbose_name='Name')),
                ('order', models.IntegerField(default=500, help_text="Use integer numbers for ordering (e.g. '100', '200', '300').", null=True, verbose_name='Order', blank=True)),
                ('description', models.TextField(help_text='Role/tasks as well as interests/goals of the participant regarding the project.', verbose_name='Description')),
                ('comments', models.TextField(verbose_name='Comments (internal)', blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('belongs_to', models.ManyToManyField(to='public_project.Participant', verbose_name='Belongs to', through='public_project.Membership')),
            ],
            options={
                'ordering': ['type', 'order', 'name'],
                'verbose_name': 'Participant',
                'verbose_name_plural': 'Participants',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ParticipantType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Type or category for sorting of participants', max_length=250, verbose_name='Title')),
                ('order', models.IntegerField(default=100, verbose_name='Order')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Type Participants',
                'verbose_name_plural': 'Types Participants',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectGoal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text="Name, e.g. 'Project budget', 'Target date', 'Noise level'", max_length=250, verbose_name='Name')),
                ('performance_figure', models.CharField(help_text="Single performance figure describing the project goal, e.g. '1.000.000 Euro', 'January 25th 2020', ...", max_length=250, verbose_name='Performance figure')),
                ('order', models.IntegerField(default=100, help_text="Use integer numbers for ordering (e.g. '100', '200', '300').", null=True, verbose_name='Order', blank=True)),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Goal Value',
                'verbose_name_plural': 'Goal Values',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectGoalGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='Group of project goals being determined at a certain point in time.', max_length=250, verbose_name='Title')),
                ('is_current', models.BooleanField(default=True, verbose_name='Is current')),
                ('description', models.TextField(help_text='Description of the group of project goals.', verbose_name='Description')),
                ('comments', models.TextField(verbose_name='Comments (internal)', blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(verbose_name='Associated event', to='public_project.Event')),
            ],
            options={
                'verbose_name': 'Goal',
                'verbose_name_plural': 'Goals',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectPart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Name of the topic', max_length=250, verbose_name='Name')),
                ('order', models.IntegerField(default=500, help_text="Use integer numbers for ordering (e.g. '100', '200', '300').", null=True, verbose_name='Order', blank=True)),
                ('description', models.TextField(help_text='Website (if existant).', verbose_name='Description')),
                ('comments', models.TextField(verbose_name='Comments (internal)', blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('main_project_parts', models.ManyToManyField(help_text="If you select another project part here, you'll make this a sub project part.", to='public_project.ProjectPart', null=True, verbose_name='Main Topic', blank=True)),
            ],
            options={
                'ordering': ['order', 'name'],
                'verbose_name': 'Project Part',
                'verbose_name_plural': 'Project Parts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='Title/short version of the question. Use prefix (e.g. 1,2,3 or A1,A2,A3) to sort questions', max_length=250, verbose_name='Title')),
                ('answered', models.BooleanField(verbose_name='Answered')),
                ('description', models.TextField(help_text='Description/long version of the question.', verbose_name='Description')),
                ('explanations', models.TextField(help_text='Optional explanations or remarks around the question', verbose_name='Explanations', blank=True)),
                ('answer', models.TextField(help_text='Optional answer (summary) of a question', verbose_name='Answer', blank=True)),
                ('comments', models.TextField(verbose_name='Comments (internal)', blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('documents', models.ManyToManyField(related_name='related_documents', null=True, verbose_name='Documents', to='public_project.Document', blank=True)),
                ('events', models.ManyToManyField(related_name='related_questions', null=True, verbose_name='Events', to='public_project.Event', blank=True)),
                ('participants', models.ManyToManyField(related_name='related_questions', null=True, verbose_name='Participants', to='public_project.Participant', blank=True)),
                ('project_parts', models.ManyToManyField(related_name='related_questions', null=True, verbose_name='Topics', to='public_project.ProjectPart', blank=True)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResearchRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nr', models.CharField(help_text='Give a unique number to your request so that people can reference it (e.g. "R1", "R2",...)', max_length=8, verbose_name='Nr')),
                ('title', models.CharField(max_length=250, verbose_name='Title')),
                ('open', models.BooleanField(default=True, verbose_name='Open')),
                ('description', models.TextField(verbose_name='Description')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date_added'],
                'verbose_name': 'Research Request',
                'verbose_name_plural': 'Research Requests',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResearchRequestRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField(help_text='The id of the related object (you can find the id of an object in the url of the object change form in the admin).')),
                ('page', models.IntegerField(help_text='Page number in document', null=True, verbose_name='Page', blank=True)),
                ('content_type', models.ForeignKey(help_text='Type of the related object (ProjectPart, Question, Participant, Event, Document).', to='contenttypes.ContentType')),
                ('research_request', models.ForeignKey(to='public_project.ResearchRequest')),
            ],
            options={
                'verbose_name': 'Relation with Project Element',
                'verbose_name_plural': 'Relations with Project Elements',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SearchTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Documents containing these search tags are shown on the detail page of this object.', max_length=250, verbose_name='Name')),
                ('object_id', models.PositiveIntegerField()),
                ('order', models.IntegerField(default=100, null=True, verbose_name='Order', blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Search Tag',
                'verbose_name_plural': 'Search Tags',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SearchTagCacheEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num_results', models.IntegerField()),
                ('document', models.ForeignKey(to='public_project.Document')),
                ('tag', models.ForeignKey(to='public_project.SearchTag')),
            ],
            options={
                'ordering': ['-num_results'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SiteCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(unique=True, max_length=50, verbose_name='Category', choices=[(b'home', b'Home'), (b'project_parts', 'Topics'), (b'goals', 'Goals'), (b'questions', 'Questions'), (b'participants', 'Participants'), (b'events', 'Events'), (b'documents', 'Documents')])),
                ('intro_text', models.TextField(null=True, verbose_name='Intro text', blank=True)),
                ('comments', models.TextField(verbose_name='Comments (internal)', blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('documents', models.ManyToManyField(related_name='related_site_categories', null=True, verbose_name='Documents', to='public_project.Document', blank=True)),
            ],
            options={
                'verbose_name': 'Website Category',
                'verbose_name_plural': 'Website Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SiteConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default='ProjectWatch', help_text='Main title, shown in the header navi.', max_length=250, verbose_name='Title')),
                ('short_title', models.CharField(default='ProjectWatch', help_text='Short version of the title, used e.g. in emails.', max_length=250, verbose_name='Short title')),
                ('title_color', models.CharField(default=b'#990000', help_text="Color for the page title (Format: '#990000').", max_length=7, verbose_name='Title color')),
                ('intro_text', models.TextField(default='This is a project watch website.', help_text='Short intro text to describe your page (HTML possible), not too long, use about text for detailed information.', verbose_name='Intro text')),
                ('about_text', models.TextField(default='About text', help_text='Short intro text about this site, what is the purpose, who is running it.', verbose_name='About text')),
                ('footer', models.TextField(default='This text will be shown in the footer of the site.', help_text='Some html text you want to use in the footer of the page, you can e.g. provide a link to your email adress or associated social media sites.', verbose_name='Footer')),
                ('contact_text', models.TextField(default='This text will be shown on the contact page.', help_text='Html to be displayed on the contact page, provide at least an adress there and some contact information.', verbose_name='Contact')),
                ('comments', models.TextField(verbose_name='Comments (internal)', blank=True)),
            ],
            options={
                'verbose_name': 'Website Configuration',
                'verbose_name_plural': 'Website Configuration',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('receive_new_comment_emails', models.BooleanField(default=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WebSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250, verbose_name='Title')),
                ('object_id', models.PositiveIntegerField()),
                ('order', models.IntegerField(default=100, help_text="Use integer numbers for ordering (e.g. '100', '200', '300').", null=True, verbose_name='Order', blank=True)),
                ('url', models.URLField(verbose_name='URL')),
                ('date', models.DateField(null=True, verbose_name='Date', blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Web-Source',
                'verbose_name_plural': 'Web-Sources',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='projectgoalgroup',
            name='project_part',
            field=models.ForeignKey(verbose_name='Topic', blank=True, to='public_project.ProjectPart', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectgoal',
            name='project_goal_group',
            field=models.ForeignKey(to='public_project.ProjectGoalGroup'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='participant',
            name='type',
            field=models.ForeignKey(blank=True, to='public_project.ParticipantType', help_text='Type for sorting, only for groups/institutions, necessary for participant to be visible on site', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='membership',
            name='from_participant',
            field=models.ForeignKey(related_name='from_memberships', verbose_name='From participant', to='public_project.Participant'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='membership',
            name='to_participant',
            field=models.ForeignKey(related_name='to_memberships', verbose_name='To participant', to='public_project.Participant', help_text='Association with a group or institution'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(related_name='related_events', null=True, verbose_name='Participants', to='public_project.Participant', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='project_parts',
            field=models.ManyToManyField(related_name='related_events', null=True, verbose_name='Topics', to='public_project.ProjectPart', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='events',
            field=models.ManyToManyField(related_name='related_documents', null=True, verbose_name='Events', to='public_project.Event', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='participants',
            field=models.ManyToManyField(related_name='related_documents', null=True, verbose_name='Participants', to='public_project.Participant', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='project_parts',
            field=models.ManyToManyField(related_name='related_documents', null=True, verbose_name='Topics', to='public_project.ProjectPart', blank=True),
            preserve_default=True,
        ),
    ]
