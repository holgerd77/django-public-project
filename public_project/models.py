# coding=UTF-8
import os
import shutil
import subprocess
from datetime import datetime
from itertools import chain

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.http import urlquote
from public_project.doc_scanner import DocScanner



class UserProfile(models.Model):
    user = models.OneToOneField(User)
    receive_new_comment_emails = models.BooleanField(default=True)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class Image(models.Model):
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='images')
    help_text = _("Short linked html attribution snippet to the original image source or \
alternatively something like 'Own image'.")
    attribution_html = models.CharField(max_length=250, help_text=help_text)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ['title',]


class SiteConfig(models.Model):
    help_text = _("Main title, shown in the header navi.")
    default = _("Project Website Title")
    title = models.CharField(max_length=250, help_text=help_text, default=default)
    help_text = _("Short version of the title, used e.g. in emails.")
    default = _("Project Website Short Title")
    short_title = models.CharField(max_length=250, help_text=help_text, default=default)
    help_text = _("Color for the page title (Format: '#990000').")
    title_color = models.CharField(max_length=7, help_text=help_text, default='#990000')
    help_text = _("Subtitle of the page.")
    default = _("Project Website Subtitle")
    sub_title = models.CharField(max_length=250, help_text=help_text, default=default)
    help_text = _("Color for the page subtitle (Format: '#990000').")
    sub_title_color = models.CharField(max_length=7, help_text=help_text, default='#444444')
    help_text = _("Short intro text to describe your page (HTML possible), not too long, use about text for detailed information.")
    default = _("This is a project watch website.")
    intro_text = models.TextField(help_text=help_text, default=default)
    help_text = _("Optional header image shown at the end of intro box on first page (Width: 450px \
Height: your choice, something around 175px is a good fit).")
    header_image = models.ForeignKey(Image, help_text=help_text, blank=True, null=True)
    help_text = _("Background color for the header (Format: '#990000').")
    header_bg_color = models.CharField(max_length=7, help_text=help_text, default='#EEEEEE')
    help_text = _("Color of the navi links (Format: '#990000').")
    navi_link_color = models.CharField(max_length=7, help_text=help_text, default='#FFFFFF')
    help_text = _("Background color for the navigation (Format: '#990000').")
    navi_bg_color = models.CharField(max_length=7, help_text=help_text, default='#333333')
    help_text = _("Background color to mark important elements on various parts of the site, \
font color will be white, so use something slightly darker.")
    important_bg_color = models.CharField(max_length=7, help_text=help_text, default='#990000')
    help_text = _("Short intro text about this site, what is the purpose, who is running it.")
    desc_about = models.TextField(help_text=help_text)
    help_text = _("Some html text you want to use in the footer of the page, you can e.g. \
provide a link to your email adress or associated social media sites.")
    footer_html = models.TextField(help_text=help_text, default=_("Footer HTML Default"))
    help_text = _("Html to be displayed on the contact page, provide at least an adress there \
and some contact information.")
    contact_html = models.TextField(help_text=help_text, default=_("Contact HTML Default"))
    comments = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.title


class SiteCategoryManager(models.Manager):
    def get_category(self, category):
        cnt = super(SiteCategoryManager, self).filter(category=category).count()
        if cnt == 1:
            return super(SiteCategoryManager, self).get(category=category)
        else:
            sc = self.model(category='home')
            print sc
            return sc


class SiteCategory(models.Model):
    NAME_CHOICES = (
        ('home', "Home"),
        ('project_parts', _('Topics')),
        ('goals', _('Goals')),
        ('questions', _('Questions')),
        ('participants', _('Participants')),
        ('events', _('Events')),
        ('documents', _('Documents')),
    )
    category = models.CharField(max_length=50, choices=NAME_CHOICES, unique=True)
    intro_text = models.TextField(blank=True, null=True)
    documents = models.ManyToManyField('Document', related_name="related_site_categories", blank=True, null=True)
    web_sources = generic.GenericRelation('WebSource')
    comments = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    objects = SiteCategoryManager()


class WebSource(models.Model):
    title = models.CharField(max_length=250)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey("content_type", "object_id")
    order = models.IntegerField(blank=True, null=True)
    url = models.URLField()
    date = models.DateField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.title
    
    @classmethod
    def get_icon_class(cls):
        return 'icon-globe'
    
    class Meta:
        ordering = ['order']


class Participant(models.Model):
    help_text  = _("Person, group or institution acting in some way in the context of the project or being affected by the process or the result of the project execution.")
    name = models.CharField(max_length=250, help_text=help_text)
    help_text = _("The participant belongs to another participant (often an institution or group), leave blank if participant itself is institution/group.")
    belongs_to = models.ManyToManyField('self', symmetrical=False)
    search_tags = generic.GenericRelation('SearchTag')
    help_text = _("Role/tasks as well as interests/goals of the participant regarding the project.")
    description = models.TextField(help_text=help_text)
    web_sources = generic.GenericRelation(WebSource)
    comment_relations = generic.GenericRelation('CommentRelation')
    comments = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.name
    
    def get_questions(self):
        return Question.objects.filter(participants__in=list(chain([self,], self.participant_set.all()))).distinct()
    
    def get_events(self):
        return Event.objects.filter(participants__in=list(chain([self,], self.participant_set.all()))).distinct()
    
    def get_documents(self):
        return Document.objects.filter(participants__in=list(chain([self,], self.participant_set.all()))).distinct()
    
    def get_feed_description(self):
        html  = self.description
        return  html
    
    def get_absolute_url(self):
        return "/" + ugettext("participants_url") + unicode(self.id) + "/"
    
    @classmethod
    def get_color(cls):
        return '#3e3ec7';
    
    def get_icon_class(self):
        if self.belongs_to.count() > 0:
            return 'icon-user'
        else:
            return 'icon-group'
    
    class Meta:
        ordering = ['name',]


class ProjectPart(models.Model):
    help_text = _("Structural parts of the project being stable over time.")
    name = models.CharField(max_length=250, help_text=help_text)
    help_text = _("Use integer numbers for ordering (e.g. '100', '200', '300').")
    order = models.IntegerField(help_text=help_text, blank=True, null=True)
    help_text = _("If you select another project part here, you'll make this a sub project part.")
    main_project_part = models.ForeignKey('self', blank=True, null=True, help_text=help_text)
    search_tags = generic.GenericRelation('SearchTag')
    help_text = _("Website (if existant).")
    description = models.TextField(help_text=help_text)
    web_sources = generic.GenericRelation(WebSource)
    comment_relations = generic.GenericRelation('CommentRelation')
    comments = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        if self.main_project_part:
            return self.name + " (" + self.main_project_part.name + ")"
        else:
            return self.name
    
    def get_questions(self):
        return Question.objects.filter(project_parts__in=list(chain([self,], self.projectpart_set.all()))).distinct()
    
    def get_events(self):
        return Event.objects.filter(project_parts__in=list(chain([self,], self.projectpart_set.all()))).distinct()
    
    def get_documents(self):
        return Document.objects.filter(project_parts__in=list(chain([self,], self.projectpart_set.all()))).distinct()
    
    def get_feed_description(self):
        html  = self.description
        return  html
    
    def get_absolute_url(self):
        return "/" + ugettext("project_parts_url") + unicode(self.id) + "/"
    
    @classmethod
    def get_color(cls):
        return '#0d9434';
    
    def get_icon_class(self):
        if self.main_project_part:
            return 'icon-cog'
        else:
            return 'icon-cogs'
    
    class Meta:
        ordering = ['order',]


class Event(models.Model):
    EVENT_TYPE_CHOICES = (
        ('ME', _('Meeting / Gathering / Session')),
        ('IN', _('New Information / Decision / Statement')),
        ('MI', _('Project Progress / Execution / Milestone')),
        ('CI', _('Action by Civil Society')),
        ('UE', _('Unplanned Event')),
        ('SE', _('Miscellaneous')),
    )
    EVENT_TYPE_CHOICES_ICONS = {
        'ME': 'icon-calendar',
        'IN': 'icon-info-sign',
        'MI': 'icon-wrench',
        'CI': 'icon-bullhorn',
        'UE': 'icon-bolt',
        'SE': 'icon-asterisk',
    }
    title = models.CharField(max_length=250)
    event_type = models.CharField(max_length=2, choices=EVENT_TYPE_CHOICES)
    help_text = _("Event being of central importance for the project.")
    important = models.BooleanField(help_text=help_text)
    search_tags = generic.GenericRelation('SearchTag')
    description = models.TextField()
    date = models.DateField()
    participants = models.ManyToManyField(Participant, related_name="related_events", blank=True, null=True)
    project_parts = models.ManyToManyField(ProjectPart, related_name="related_events", blank=True, null=True)
    web_sources = generic.GenericRelation(WebSource)
    comment_relations = generic.GenericRelation('CommentRelation')
    comments = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.title + ", " + datetime.strftime(self.date, '%d.%m.%Y') 
    
    def get_feed_description(self):
        html  = self.description
        
        if len(self.participants.all()) > 0:
            html += '<br><br>'
            html += _("Participants") + ':'
            for p in self.participants.all():
                html += '<br><a href="' + p.get_absolute_url() + '">' + unicode(p) + '</a>'
        
        if len(self.project_parts.all()) > 0:
            html += '<br><br>'
            html += _("Subject Areas") + ':'
            for pp in self.project_parts.all():
                html += '<br><a href="' + pp.get_absolute_url() + '">' + unicode(pp) + '</a>'
        
        return  html
    
    def get_absolute_url(self):
        return "/" + ugettext("events_url") + unicode(self.id) + "/"
    
    def get_event_type_icon(self):
        return self.EVENT_TYPE_CHOICES_ICONS[self.event_type]
    
    @classmethod
    def get_color(cls):
        return '#c91a1a'
    
    @classmethod
    def get_icon_class(cls):
        return 'icon-time'
    
    def as_list(self):
        return [self,]
    
    class Meta:
        ordering = ['-date']


class Question(models.Model):
    help_text = _("Title/short version of the question. Use prefix (e.g. 1,2,3 or A1,A2,A3) to sort questions")
    title = models.CharField(max_length=250, help_text=help_text)
    answered = models.BooleanField()
    help_text = _("Description/long version of the question.")
    description = models.TextField(help_text=help_text)
    project_parts = models.ManyToManyField(ProjectPart, related_name="related_questions", blank=True, null=True)
    participants = models.ManyToManyField(Participant, related_name="related_questions", blank=True, null=True)
    events = models.ManyToManyField(Event, related_name="related_questions", blank=True, null=True)
    help_text = _("Optional explanations or remarks around the question")
    explanations = models.TextField(blank=True, help_text=help_text)
    help_text = _("Optional answer (summary) of a question")
    answer = models.TextField(blank=True, help_text=help_text)
    documents = models.ManyToManyField('Document', related_name="related_documents", blank=True, null=True)
    web_sources = generic.GenericRelation(WebSource)
    comment_relations = generic.GenericRelation('CommentRelation')
    comments = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def get_feed_description(self):
        html  = self.description
        
        if len(self.project_parts.all()) > 0:
            html += '<br><br>'
            html += _("Subject Areas") + ':'
            for pp in self.project_parts.all():
                html += '<br><a href="' + pp.get_absolute_url() + '">' + unicode(pp) + '</a>'
        
        if len(self.participants.all()) > 0:
            html += '<br><br>'
            html += _("Participants") + ':'
            for p in self.participants.all():
                html += '<br><a href="' + p.get_absolute_url() + '">' + unicode(p) + '</a>'
        
        if len(self.events.all()) > 0:
            html += '<br><br>'
            html += _("Events") + ':'
            for e in self.events.all():
                html += '<br><a href="' + e.get_absolute_url() + '">' + unicode(e) + '</a>'
        
        return  html
    
    def get_absolute_url(self):
        return "/" + ugettext("questions_url") + unicode(self.id) + "/"
    
    @classmethod
    def get_color(cls):
        return '#941bbf';
    
    @classmethod
    def get_icon_class(cls):
        return 'icon-question-sign';
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ['title']


class ProjectGoalGroupManager(models.Manager):
    
    def get_current(self):
        return self.all().order_by('event')[0]
        

class ProjectGoalGroup(models.Model):
    help_text = _("Group of project goals being determined at a certain point in time.")
    title = models.CharField(max_length=250, help_text=help_text)
    event = models.ForeignKey(Event)
    help_text = _("Description of the group of project goals.")
    description = models.TextField(help_text=help_text)
    comments = models.TextField(blank=True)
    objects = ProjectGoalGroupManager()
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.title

    def is_current(self):
        return self == ProjectGoalGroup.objects.get_current()


class ProjectGoal(models.Model):
    help_text = _("Name, e.g. 'Project budget', 'Target date', 'Noise level'")
    name = models.CharField(max_length=250, help_text=help_text)
    project_goal_group = models.ForeignKey(ProjectGoalGroup)
    help_text = _("Single performance figure describing the project goal, e.g. '1.000.000 Euro', 'January 25th 2020', ...")
    performance_figure = models.CharField(max_length=250, help_text=help_text)
    help_text = _("Use integer numbers for ordering (e.g. '100', '200', '300').")
    order = models.IntegerField(help_text=help_text, blank=True, null=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['order',]


class Document(models.Model):
    help_text = _("Unique and descriptive title (if PublicDocs is used: PDF live view is shown, if document title is the same)")
    title = models.CharField(max_length=250, help_text=help_text)
    document = models.FileField(upload_to='documents')
    date = models.DateField()
    help_text = _("Short description.")
    description = models.TextField(help_text=help_text)
    participants = models.ManyToManyField(Participant, related_name="related_documents", blank=True, null=True)
    project_parts = models.ManyToManyField(ProjectPart, related_name="related_documents", blank=True, null=True)
    events = models.ManyToManyField(Event, related_name="related_documents", blank=True, null=True)
    comment_relations = generic.GenericRelation('CommentRelation')
    comments = models.TextField(blank=True)
    pdf_images_generated = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.title + " (" + datetime.strftime(self.date, '%d.%m.%Y') + ")"
    
    def get_feed_description(self):
        html  = self.description
        
        if len(self.participants.all()) > 0:
            html += '<br><br>'
            html += _("Participants") + ':'
            for p in self.participants.all():
                html += '<br><a href="' + p.get_absolute_url() + '">' + unicode(p) + '</a>'
        
        if len(self.project_parts.all()) > 0:
            html += '<br><br>'
            html += _("Subject Areas") + ':'
            for pp in self.project_parts.all():
                html += '<br><a href="' + pp.get_absolute_url() + '">' + unicode(pp) + '</a>'
        
        if len(self.events.all()) > 0:
            html += '<br><br>'
            html += _("Events") + ':'
            for e in self.events.all():
                html += '<br><a href="' + e.get_absolute_url() + '">' + unicode(e) + '</a>'
        
        return  html
    
    def get_absolute_url(self):
        return "/" + ugettext("documents_url") + unicode(self.id) + "/"
    
    @classmethod
    def get_color(cls):
        return '#b88f00';
    
    @classmethod
    def get_icon_class(cls):
        return 'icon-inbox';
    
    def get_document_name(self):
        return os.path.basename(self.document.name)
    
    def get_pages_path(self):
        return os.path.join(settings.MEDIA_ROOT, 'documents/document_' + unicode(self.id) + '/')
    
    def get_active_user_comments(self):
        return self.comment_relations.filter(comment__published=True)
    
    def get_num_active_user_comments(self):
        return self.comment_relations.filter(comment__published=True).count()
    
    class Meta:
        ordering = ['-date_added']
    
    def __init__(self, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)
        self.old_document = self.document

    def save(self, force_insert=False, force_update=False):
        if getattr(settings, 'DPP_IE_COMPATIBLE_PDF_VIEWER', False) and self.old_document != self.document:
            self.pdf_images_generated = False
        super(Document, self).save(force_insert, force_update)

        # Delete old document
        if self.old_document and self.old_document != self.document:
            if os.path.exists(self.old_document.path):
                os.remove(self.old_document.path)
        
        # Saving pages when DPP_IE_COMPATIBLE_PDF_VIEWER=True in settings.py
        if getattr(settings, 'DPP_IE_COMPATIBLE_PDF_VIEWER', False) and self.old_document != self.document:
            self.page_set.all().delete()
            cmd = u"python manage.py createpages " + str(self.id) + " --settings=" + settings.SETTINGS_MODULE
            subprocess.Popen(cmd, shell=True)
            
            cmd = u"python manage.py generatepdfimages " + str(self.id) + " --settings=" + settings.SETTINGS_MODULE
            subprocess.Popen(cmd, shell=True)
        
        from public_project.tag_cache_creator import rebuild_cache_for_document
        rebuild_cache_for_document(self)
        
        self.old_document = self.document

def delete_pages_folder(sender, **kwargs):
    instance = kwargs['instance']
    if os.path.exists(instance.get_pages_path()):
        shutil.rmtree(instance.get_pages_path())

def delete_document_file(sender, **kwargs):
    instance = kwargs['instance']
    if instance.document and os.path.exists(instance.document.path):
                os.remove(instance.document.path)

pre_delete.connect(delete_pages_folder, sender=Document)
pre_delete.connect(delete_document_file, sender=Document)


class Page(models.Model):
    document = models.ForeignKey(Document)
    number = models.IntegerField()
    content = models.TextField(blank=True)
    
    def get_filename(self):
        return u'page-' + unicode(self.number) + u'.jpg'
    
    def get_filepath(self):
        return self.document.get_pages_path() + self.get_filename()
    
    def __unicode__(self):
        return unicode(self.document) + ", Page " + unicode(self.number)
    
    class Meta:
        ordering = ['number']


def delete_page_image(sender, **kwargs):
    instance = kwargs['instance']
    if os.path.exists(instance.get_filepath()):
        os.remove(instance.get_filepath())

pre_delete.connect(delete_page_image, sender=Page)


class SearchTag(models.Model):
    help_text = _("Documents containing these search tags are shown on the detail page of this object.")
    name = models.CharField(max_length=250, help_text=help_text)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey("content_type", "object_id")
    order = models.IntegerField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['order']


@receiver(post_save, sender=SearchTag)
def rebuild_tag_cache(sender, instance, **kwargs):
    from public_project.tag_cache_creator import rebuild_cache_for_tag
    rebuild_cache_for_tag(instance)


class SearchTagCacheEntry(models.Model):
    tag = models.ForeignKey(SearchTag)
    document = models.ForeignKey(Document)
    num_results = models.IntegerField()
    
    def __unicode__(self):
        return "Tag:" + unicode(self.tag) + ", Document:" + unicode(self.document)
    
    class Meta:
        ordering = ['-num_results']


RELATION_LIMIT = models.Q(app_label = 'public_project', model = 'projectpart') | \
            models.Q(app_label = 'public_project', model = 'question') | \
            models.Q(app_label = 'public_project', model = 'participant') | \
            models.Q(app_label = 'public_project', model = 'event') | \
            models.Q(app_label = 'public_project', model = 'document')


class ResearchRequestRelation(models.Model):
    research_request = models.ForeignKey('ResearchRequest')
    help_text = _('Type of the related object (ProjectPart, Question, Participant, Event, Document).')
    limit = RELATION_LIMIT
    content_type = models.ForeignKey(ContentType, help_text=help_text, limit_choices_to=limit)
    help_text = _('The id of the related object (you can find the id of an object in the url \
of the object change form in the admin).')
    object_id = models.PositiveIntegerField(help_text=help_text)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    help_text = _("Page number in document")
    page = models.IntegerField(blank=True, null=True, help_text=help_text)
    
    def __unicode__(self):
        return unicode(self.research_request) + ', ' + unicode(self.content_object)
    

class ResearchRequest(models.Model):
    help_text = _('Give a unique number to your request so that people can reference it (e.g. "R1", "R2",...)')
    nr = models.CharField(max_length=8, help_text=help_text)
    title = models.CharField(max_length=250)
    open = models.BooleanField(default=True)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return unicode(self.nr) + ': ' + self.title
    
    def get_feed_description(self):
        html  = self.description
        
        html += '<br><br>'
        html += _("Request on the following contents") + ':'
        for rr_rel in self.researchrequestrelation_set.all():
            html += '<br><a href="' + rr_rel.content_object.get_absolute_url() + '">' + unicode(rr_rel.content_object) + '</a>'
        
        return  html
    
    def get_related_question(self):
        question = None
        content_type = ContentType.objects.get(app_label="public_project", model="question")
        cos =  self.researchrequestrelation_set.all()
        for co in cos:
            if co.content_type == content_type:
                question = co.content_object
        return question
    
    def get_absolute_url(self):
        return self.get_related_question().get_absolute_url() + '?research_request_id=' + unicode(self.id)
    
    @classmethod
    def get_color(cls):
        return '#555';
    
    @classmethod
    def get_icon_class(cls):
        return 'icon-eye-open';
    
    def get_share_text(self):
        short_title = 'ProjectWatch'
        if SiteConfig.objects.count() > 0:
            site_config = SiteConfig.objects.all()[0]
            short_title = site_config.short_title
        
        share_text = short_title + " " + unicode(_("Research Request")) + " " + self.nr + ": " + self.title
        return share_text
    
    def get_share_url(self):
        share_url = 'http://%s%s' % (Site.objects.get_current().domain, self.get_absolute_url())
        return share_url
    
    def get_twitter_url(self):
        url  = 'https://twitter.com/intent/tweet'
        url += '?&text=' + urlquote(self.get_share_text()) + '&url=' + urlquote(self.get_share_url())
        return url
    
    def get_facebook_url(self):
        url  = 'https://www.facebook.com/sharer.php'
        url += '?&t=' + urlquote(self.get_share_text()) + '&u=' + urlquote(self.get_share_url())
        return url
    
    def get_google_plus_url(self):
        url  = 'https://plus.google.com/share'
        url += '?url=' + urlquote(self.get_share_url())
        return url
    
    def get_app_net_url(self):
        url  = 'https://alpha.app.net/intent/post?text='
        url += urlquote(self.get_share_text() + " " + self.get_share_url())
        return url
    
    class Meta:
        ordering = ['-date_added']



class CommentRelation(models.Model):
    comment = models.ForeignKey('Comment')
    help_text = _('Type of the related object (ProjectPart, Question, Participant, Event, Document).')
    limit = RELATION_LIMIT
    content_type = models.ForeignKey(ContentType, help_text=help_text, limit_choices_to=limit)
    help_text = _('The id of the related object (you can find the id of an object in the url \
of the object change form in the admin).')
    object_id = models.PositiveIntegerField(help_text=help_text)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    help_text = _("Page number in document")
    page = models.IntegerField(blank=True, null=True, help_text=help_text)
    
    def __unicode__(self):
        return unicode(self.comment) + ', ' + unicode(self.content_object)
    

class Comment(models.Model):
    username = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    help_text = _('User has given permission to get in contact vi.')
    feedback_allowed = models.BooleanField(default=False, help_text=help_text)
    comment = models.TextField()
    help_text = _('Comment is only shown on page if published is true.')
    published = models.BooleanField(default=False, help_text=help_text)
    published_by = models.CharField(max_length=250, blank=True)
    activation_hash = models.CharField(max_length=250, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.username + ", " + datetime.strftime(self.date_added, '%d.%m.%Y')
    
    def get_feed_description(self):
        html  = self.comment
        
        html += '<br><br>'
        html += _("Commented contents") + ':'
        for cr in self.commentrelation_set.all():
            html += '<br><a href="' + cr.content_object.get_absolute_url() + '">' + unicode(cr.content_object) + '</a>'
        
        return  html
    
    def get_absolute_url(self):
        first_co = self.commentrelation_set.all()[0].content_object
        return first_co.get_absolute_url() + '?comment_id=' + unicode(self.id)
    
    @classmethod
    def get_color(cls):
        return '#555';
    
    @classmethod
    def get_icon_class(cls):
        return 'icon-comment';
    
    def get_share_text(self):
        co1 = list(self.commentrelation_set.all())[0].content_object
        
        short_title = 'ProjectWatch'
        if SiteConfig.objects.count() > 0:
            site_config = SiteConfig.objects.all()[0]
            short_title = site_config.short_title
        
        share_text = _('Comment on %s on') % short_title
        share_text += ' "' + unicode(co1) + '"'
        share_text += ":"
        return share_text
    
    def get_share_url(self):
        share_url = 'http://%s%s' % (Site.objects.get_current().domain, self.get_absolute_url())
        return share_url
    
    def get_twitter_url(self):
        url  = 'https://twitter.com/intent/tweet'
        url += '?&text=' + urlquote(self.get_share_text()) + '&url=' + urlquote(self.get_share_url())
        return url
    
    def get_facebook_url(self):
        url  = 'https://www.facebook.com/sharer.php'
        url += '?&t=' + urlquote(self.get_share_text()) + '&u=' + urlquote(self.get_share_url())
        return url
    
    def get_google_plus_url(self):
        url  = 'https://plus.google.com/share'
        url += '?url=' + urlquote(self.get_share_url())
        return url
    
    def get_app_net_url(self):
        url  = 'https://alpha.app.net/intent/post?text='
        url += urlquote(self.get_share_text() + " " + self.get_share_url())
        return url
    
    class Meta:
        ordering = ['-date_added']
    

class ActivityLog(models.Model):
    TYPE_CHOICES = (
        ('NA', _('New Subject Area')),
        ('NQ', _('New Question')),
        ('PA', _('New Participant')),
        ('NE', _('Event')),
        ('ND', _('New Document')),
        ('RR', _('Research Request')),
        ('NC', _('Comment')),
    )
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    info = models.CharField(max_length=250, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return u'Activity: ' + unicode(self.content_object)
    
    class Meta:
        ordering = ['-date']


@receiver(post_save, sender=ProjectPart)
def add_na_activity(sender, instance, created, **kwargs):
    if created:
        al = ActivityLog(content_object=instance, type='NA')
        al.save()


@receiver(post_save, sender=Question)
def add_nq_activity(sender, instance, created, **kwargs):
    if created:
        al = ActivityLog(content_object=instance, type='NQ')
        al.save()


@receiver(post_save, sender=Participant)
def add_pa_activity(sender, instance, created, **kwargs):
    if created:
        al = ActivityLog(content_object=instance, type='PA')
        al.save()


@receiver(post_save, sender=Event)
def add_ne_activity(sender, instance, created, **kwargs):
    if created:
        al = ActivityLog(content_object=instance, type='NE')
        al.save()


@receiver(post_save, sender=Document)
def add_nd_activity(sender, instance, created, **kwargs):
    if created:
        al = ActivityLog(content_object=instance, type='ND')
        al.save()


@receiver(post_save, sender=ResearchRequest)
def add_rr_activity(sender, instance, created, **kwargs):
    if created:
        al = ActivityLog(content_object=instance, type='RR')
        al.save()
