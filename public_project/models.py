# coding=UTF-8
import os
import shutil
import subprocess
from datetime import datetime
from itertools import chain

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils.text import slugify
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
    title = models.CharField(_("Title"), max_length=250)
    help_text = _("400px max width, 200px for images used with floating texts")
    image = models.ImageField(_("Image"), upload_to='images', help_text=help_text)
    help_text = _("Attribution to the original image source or alternatively something like 'Own image'.")
    attribution = models.CharField(_("Attribution"), max_length=250, help_text=help_text)
    help_text = _("Link to the original image source (if available)")
    attribution_url = models.URLField(_("Attribution URL"), help_text=help_text, blank=True, null=True)
    comments = models.TextField(_("Comments (internal)"), blank=True)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ['title',]
        verbose_name = _('Image')
        verbose_name_plural = _('Images')


class SiteConfigManager(models.Manager):
    
    def get_site_config(self, request):
        if super(SiteConfigManager, self).count() == 0:
            site_config = SiteConfig()
            site_config.save()
        else:
            site_config = super(SiteConfigManager, self).all()[0]
        
        site_config.pdf_viewer = 'STANDARD'
        site_config.browser = 'Unknown'
        if request and 'HTTP_USER_AGENT' in request.META:
            if 'Mozilla'.lower() in request.META['HTTP_USER_AGENT'].lower():
                site_config.pdf_viewer = 'STANDARD'
                site_config.browser = 'Mozilla'
            if 'Safari'.lower() in request.META['HTTP_USER_AGENT'].lower():
                site_config.pdf_viewer = 'STANDARD'
                site_config.browser = 'Safari'
            if 'Chrome'.lower() in request.META['HTTP_USER_AGENT'].lower():
                site_config.pdf_viewer = 'STANDARD'
                site_config.browser = 'Chrome'
            if 'Opera'.lower() in request.META['HTTP_USER_AGENT'].lower():
                site_config.pdf_viewer = 'STANDARD'
                site_config.browser = 'Opera'
            if 'MSIE'.lower() in request.META['HTTP_USER_AGENT'].lower():
                if getattr(settings, 'DPP_IE_COMPATIBLE_PDF_VIEWER', False):
                    site_config.pdf_viewer = 'LEGACY'
                else:
                    site_config.pdf_viewer = False
                site_config.browser = 'MSIE'
        
        if getattr(settings, 'DPP_PUBLIC_API', False):
            site_config.public_api = True
        else:
            site_config.public_api = False
        
        if getattr(settings, 'DPP_CUSTOM_JS', False):
            site_config.custom_js = settings.DPP_CUSTOM_JS
        else:
            site_config.custom_js = ''    
        
        if getattr(settings, 'DPP_CUSTOM_CSS', False):
            site_config.custom_css = settings.DPP_CUSTOM_CSS
        else:
            site_config.custom_css = ''
        
        return site_config
    

class SiteConfig(models.Model):
    help_text = _("Main title, shown in the header navi.")
    default = _("Project Website Title")
    title = models.CharField(_("Title"), max_length=250, help_text=help_text, default=default)
    help_text = _("Short version of the title, used e.g. in emails.")
    default = _("Project Website Short Title")
    short_title = models.CharField(_("Short title"), max_length=250, help_text=help_text, default=default)
    help_text = _("Color for the page title (Format: '#990000').")
    title_color = models.CharField(_("Title color"), max_length=7, help_text=help_text, default='#990000')
    help_text = _("Show/use the Goals category in the project.")
    show_goals_category = models.BooleanField(default=True)
    help_text = _("Show/use the Questions category in the project.")
    show_questions_category = models.BooleanField(default=True)
    help_text = _("Activate user comments.")
    activate_comments = models.BooleanField(default=True)
    help_text = _("Short intro text to describe your page (HTML possible), not too long, use about text for detailed information.")
    default = _("This is a project watch website.")
    intro_text = models.TextField(_("Intro text"), help_text=help_text, default=default)
    help_text = _("Short intro text about this site, what is the purpose, who is running it.")
    default = _("About text")
    about_text = models.TextField(_("About text"), help_text=help_text, default=default)
    help_text = _("Some html text you want to use in the footer of the page, you can e.g. \
provide a link to your email adress or associated social media sites.")
    footer = models.TextField(_("Footer"), help_text=help_text, default=_("Footer HTML Default"))
    help_text = _("Html to be displayed on the contact page, provide at least an adress there \
and some contact information.")
    contact_text = models.TextField(_("Contact"), help_text=help_text, default=_("Contact HTML Default"))
    comments = models.TextField(_("Comments (internal)"), blank=True)
    
    objects = SiteConfigManager()
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = _('Website Configuration')
        verbose_name_plural = _('Website Configuration')


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
    category = models.CharField(_("Category"), max_length=50, choices=NAME_CHOICES, unique=True)
    intro_text = models.TextField(_("Intro text"), blank=True, null=True)
    documents = models.ManyToManyField('Document', related_name="related_site_categories", blank=True, verbose_name=_("Documents"))
    web_sources = GenericRelation('WebSource', verbose_name=_("Web Sources"))
    comments = models.TextField(_("Comments (internal)"), blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.get_category_display()
    
    class Meta:
        verbose_name = _('Website Category')
        verbose_name_plural = _('Website Categories')


class ParticipantType(models.Model):
    help_text = _("Type or category for sorting of participants")
    name = models.CharField(_("Title"), max_length=250, help_text=help_text)
    help_text = _("Use integer numbers for ordering (e.g. '100', '200', '300').")
    order = models.IntegerField(_("Order"), default=100)
    date_added = models.DateTimeField(auto_now_add=True)    
    
    def get_participants(self):
        return self.participant_set.filter(belongs_to=None)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['order']
        verbose_name = _('Type Participants')
        verbose_name_plural = _('Types Participants')


class WebSource(models.Model):
    title = models.CharField(_("Title"), max_length=250)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    help_text = _("Use integer numbers for ordering (e.g. '100', '200', '300').")
    order = models.IntegerField(_("Order"), help_text=help_text, default=100, blank=True, null=True)
    url = models.URLField(_("URL"))
    date = models.DateField(_("Date"), blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return "/" + ugettext("web_sources_url") + unicode(self.id) + "/"
    
    @classmethod
    def get_icon_class(cls):
        return 'icon-globe'
    
    class Meta:
        ordering = ['order']
        verbose_name = _('Web-Source')
        verbose_name_plural = _('Web-Sources')


class Membership(models.Model):
    from_participant = models.ForeignKey('Participant', related_name='from_memberships', verbose_name=_("From participant"))
    help_text = _('Association with a group or institution')
    to_participant = models.ForeignKey('Participant', help_text=help_text, related_name='to_memberships', verbose_name=_("To participant"))
    help_text = _("Type or function of the membership or task or position of the participant.")
    function = models.CharField(_("Function"), max_length=50, help_text=help_text, blank=True, null=True)
    active = models.BooleanField(_("Active"), default=True)
    
    class Meta:
        verbose_name = _('Membership')
        verbose_name_plural = _('Memberships')


class Participant(models.Model):
    help_text  = _("Person, group or institution acting in some way in the context of the project or being affected by the process or the result of the project execution.")
    name = models.CharField(_("Name"), max_length=250, help_text=help_text, unique=True)
    help_text = _("Type for sorting, only for groups/institutions, necessary for participant to be visible on site")
    type = models.ForeignKey(ParticipantType, blank=True, null=True, help_text=help_text)
    help_text = _("Use integer numbers for ordering (e.g. '100', '200', '300').")
    order = models.IntegerField(_("Order"), help_text=help_text, default=500, blank=True, null=True)
    help_text = _("The participant belongs to another participant (often an institution or group), leave blank if participant itself is institution/group.")
    belongs_to = models.ManyToManyField('self', symmetrical=False, through='Membership', verbose_name=_("Belongs to"))
    search_tags = GenericRelation('SearchTag')
    help_text = _("Role/tasks as well as interests/goals of the participant regarding the project.")
    description = models.TextField(_("Description"), help_text=help_text)
    web_sources = GenericRelation(WebSource)
    comment_relations = GenericRelation('CommentRelation')
    comments = models.TextField(_("Comments (internal)"), blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    activities = GenericRelation('ActivityLog')
    
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
        return "/" + ugettext("participants_url") + slugify(self.name) + '-' + unicode(self.id) + "/"
    
    def get_comments_url(self):
        return "/" + ugettext("participants_url") + unicode(self.id) + "/" + ugettext("comments_url")
    
    def get_active_user_comments(self):
        return self.comment_relations.filter(comment__published=True)
    
    def get_num_active_user_comments(self):
        return self.comment_relations.filter(comment__published=True).count()
    
    @classmethod
    def get_color(cls):
        return '#3e3ec7';
    
    def get_icon_class(self):
        if self.belongs_to.count() > 0:
            return 'icon-user'
        else:
            return 'icon-group'
    
    def get_simple_entry(self):
        html  = '<i class="' + self.get_icon_class() + '"></i> '
        html += '<a href="' + self.get_absolute_url() +'">' + self.name + '</a>'
        return html 
    
    class Meta:
        ordering = ['type', 'order', 'name',]
        verbose_name = _('Participant')
        verbose_name_plural = _('Participants')


class ProjectPart(models.Model):
    help_text = _("Name of the topic")
    name = models.CharField(_("Name"), max_length=250, help_text=help_text)
    help_text = _("Use integer numbers for ordering (e.g. '100', '200', '300').")
    order = models.IntegerField(_("Order"), help_text=help_text, default=500, blank=True, null=True)
    help_text = _("If you select another project part here, you'll make this a sub project part.")
    main_project_parts = models.ManyToManyField('self', symmetrical=False, help_text=help_text, blank=True, verbose_name=_("Main Topic"))
    search_tags = GenericRelation('SearchTag')
    help_text = _("Website (if existant).")
    description = models.TextField(_("Description"), help_text=help_text)
    web_sources = GenericRelation(WebSource)
    comment_relations = GenericRelation('CommentRelation')
    comments = models.TextField(_("Comments (internal)"), blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    activities = GenericRelation('ActivityLog')

    def __unicode__(self):
        return self.name
    
    def get_questions(self):
        return Question.objects.filter(project_parts__in=list(chain([self,], self.projectpart_set.all()))).distinct()
    
    def get_num_questions(self):
        return Question.objects.filter(project_parts__in=list(chain([self,], self.projectpart_set.all()))).distinct().count()
    
    def get_events(self):
        return Event.objects.filter(project_parts__in=list(chain([self,], self.projectpart_set.all()))).distinct()
    
    def get_num_events(self):
        return Event.objects.filter(project_parts__in=list(chain([self,], self.projectpart_set.all()))).distinct().count()
    
    def get_documents(self):
        return Document.objects.filter(project_parts__in=list(chain([self,], self.projectpart_set.all()))).distinct()
    
    def get_num_documents(self):
        return Document.objects.filter(project_parts__in=list(chain([self,], self.projectpart_set.all()))).distinct().count()
    
    def get_feed_description(self):
        html  = self.description
        return  html
    
    def get_absolute_url(self):
        return "/" + ugettext("project_parts_url") + slugify(self.name) + '-' + unicode(self.id) + "/"
    
    @classmethod
    def get_color(cls):
        return '#0d9434';
    
    def get_icon_class(self):
        if self.main_project_parts.count() > 0:
            return 'icon-cog'
        else:
            return 'icon-cogs'
    
    def get_simple_entry(self):
        html  = '<i class="' + self.get_icon_class() + '"></i> '
        html += '<a href="' + self.get_absolute_url() +'">' + self.name + '</a>'
        return html
    
    class Meta:
        ordering = ['order', 'name',]
        verbose_name = _('Project Part')
        verbose_name_plural = _('Project Parts')


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
    title = models.CharField(_("Title"), max_length=250)
    event_type = models.CharField(_("Type"), max_length=2, choices=EVENT_TYPE_CHOICES)
    help_text = _("Event being of central importance for the project.")
    important = models.BooleanField(_("Main Event"), default=False, help_text=help_text)
    search_tags = GenericRelation('SearchTag')
    description = models.TextField(_("Description"))
    date = models.DateField(_("Date"))
    help_text = _("Date is not exact (e.g. if a source refers only to the month)")
    not_exact = models.BooleanField(_("Date not exact"), default=False, help_text=help_text)
    participants = models.ManyToManyField(Participant, related_name="related_events", blank=True, verbose_name=_("Participants"))
    project_parts = models.ManyToManyField(ProjectPart, related_name="related_events", blank=True, verbose_name=_("Topics"))
    web_sources = GenericRelation(WebSource)
    comment_relations = GenericRelation('CommentRelation')
    comments = models.TextField(_("Comments (internal)"), blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    activities = GenericRelation('ActivityLog')
    
    def __unicode__(self):
        str  = self.title + ", "
        if self.not_exact:
            str += '('
        str += datetime.strftime(self.date, '%d.%m.%Y')
        if self.not_exact:
            str += ')'
        return str 
    
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
        return "/" + ugettext("events_url") + slugify(self.date.strftime('%Y-%m-%d') + '-' + self.title) + '-' + unicode(self.id) + "/"
    
    def get_event_type_icon(self):
        return self.EVENT_TYPE_CHOICES_ICONS[self.event_type]
    
    def get_comments_url(self):
        return "/" + ugettext("events_url") + unicode(self.id) + "/" + ugettext("comments_url")
    
    def get_active_user_comments(self):
        return self.comment_relations.filter(comment__published=True)
    
    def get_num_active_user_comments(self):
        return self.comment_relations.filter(comment__published=True).count()
    
    @classmethod
    def get_color(cls):
        return '#c91a1a'
    
    @classmethod
    def get_icon_class(cls):
        return 'icon-time'
    
    def get_simple_entry(self):
        html  = '<i class="' + self.get_icon_class() + '"></i> '
        html += '<a href="' + self.get_absolute_url() +'">' + self.title + '</a>'
        return html
    
    def as_list(self):
        return [self,]
    
    class Meta:
        ordering = ['-date']
        verbose_name = _('Event')
        verbose_name_plural = _('Events')


class Question(models.Model):
    help_text = _("Title/short version of the question. Use prefix (e.g. 1,2,3 or A1,A2,A3) to sort questions")
    title = models.CharField(_("Title"), max_length=250, help_text=help_text)
    answered = models.BooleanField(_("Answered"), default=False)
    help_text = _("Description/long version of the question.")
    description = models.TextField(_("Description"), help_text=help_text)
    project_parts = models.ManyToManyField(ProjectPart, related_name="related_questions", blank=True, verbose_name=_("Topics"))
    participants = models.ManyToManyField(Participant, related_name="related_questions", blank=True, verbose_name=_("Participants"))
    events = models.ManyToManyField(Event, related_name="related_questions", blank=True, verbose_name=_("Events"))
    help_text = _("Optional explanations or remarks around the question")
    explanations = models.TextField(_("Explanations"), blank=True, help_text=help_text)
    help_text = _("Optional answer (summary) of a question")
    answer = models.TextField(_("Answer"), blank=True, help_text=help_text)
    documents = models.ManyToManyField('Document', related_name="related_documents", blank=True, verbose_name=_("Documents"))
    web_sources = GenericRelation(WebSource)
    comment_relations = GenericRelation('CommentRelation')
    comments = models.TextField(_("Comments (internal)"), blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    activities = GenericRelation('ActivityLog')
    
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
        return "/" + ugettext("questions_url") + slugify(self.title) + '-' + unicode(self.id) + "/"
    
    def get_comments_url(self):
        return "/" + ugettext("questions_url") + unicode(self.id) + "/" + ugettext("comments_url")
    
    def get_active_user_comments(self):
        return self.comment_relations.filter(comment__published=True)
    
    def get_num_active_user_comments(self):
        return self.comment_relations.filter(comment__published=True).count()
    
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
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')


class ProjectGoalGroupManager(models.Manager):
    
    def get_current(self):
        if self.count() > 0:
            return self.all().order_by('event')[0]
        else:
            return None
        

class ProjectGoalGroup(models.Model):
    help_text = _("Group of project goals being determined at a certain point in time.")
    title = models.CharField(_("Title"), max_length=250, help_text=help_text)
    help_text = _("The topic the group of goals belong to. Will be shown as common goal group if none selected.")
    project_part = models.ForeignKey(ProjectPart, blank=True, null=True, verbose_name=_("Topic"))
    event = models.ForeignKey(Event, verbose_name=_("Associated event"))
    is_current = models.BooleanField(default=True, verbose_name=_("Is current"))
    help_text = _("Description of the group of project goals.")
    description = models.TextField(_("Description"), help_text=help_text)
    comments = models.TextField(_("Comments (internal)"), blank=True)
    objects = ProjectGoalGroupManager()
    date_added = models.DateTimeField(auto_now_add=True)
    activities = GenericRelation('ActivityLog')
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = _('Goal')
        verbose_name_plural = _('Goals')


class ProjectGoal(models.Model):
    help_text = _("Name, e.g. 'Project budget', 'Target date', 'Noise level'")
    name = models.CharField(_("Name"), max_length=250, help_text=help_text)
    project_goal_group = models.ForeignKey(ProjectGoalGroup)
    help_text = _("Single performance figure describing the project goal, e.g. '1.000.000 Euro', 'January 25th 2020', ...")
    performance_figure = models.CharField(_("Performance figure"), max_length=250, help_text=help_text)
    help_text = _("Use integer numbers for ordering (e.g. '100', '200', '300').")
    order = models.IntegerField(_("Order"), help_text=help_text, default=100, blank=True, null=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['order',]
        verbose_name = _('Goal Value')
        verbose_name_plural = _('Goal Values')


class Document(models.Model):
    help_text = _("Title of the document")
    title = models.CharField(_("Title"), max_length=250, help_text=help_text)
    help_text = _('Document in pdf format')
    document = models.FileField(_("Document"), upload_to='documents', help_text=help_text)
    help_text = _('Date of creation of the document')
    date = models.DateField(_("Date"), help_text=help_text)
    help_text = _("Short description.")
    description = models.TextField(_("Description"), help_text=help_text)
    participants = models.ManyToManyField(Participant, related_name="related_documents", blank=True, verbose_name=_("Participants"))
    project_parts = models.ManyToManyField(ProjectPart, related_name="related_documents", blank=True, verbose_name=_("Topics"))
    events = models.ManyToManyField(Event, related_name="related_documents", blank=True, verbose_name=_("Events"))
    comment_relations = GenericRelation('CommentRelation')
    comments = models.TextField(_("Comments (internal)"), blank=True)
    pdf_images_generated = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    activities = GenericRelation('ActivityLog')
    
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
        return "/" + ugettext("documents_url") + slugify(self.title) + '-' + unicode(self.id) + "/"
    
    def get_comments_url(self):
        return "/" + ugettext("documents_url") + unicode(self.id) + "/" + ugettext("comments_url")
    
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
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')
    
    def __init__(self, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)
        self.old_document = self.document

    def save(self, force_insert=False, force_update=False):
        if getattr(settings, 'DPP_IE_COMPATIBLE_PDF_VIEWER', True) and self.old_document != self.document:
            self.pdf_images_generated = False
        else:
            self.pdf_images_generated = True
        super(Document, self).save(force_insert, force_update)
        #print "pdf_images_generated set to: " + str(self.pdf_images_generated)

        # Delete old document
        if self.old_document and self.old_document != self.document:
            if os.path.exists(self.old_document.path):
                os.remove(self.old_document.path)
                #print "Old document deleted from path: " + self.old_document.path
        
        if self.old_document != self.document:
            cmd = u"python manage.py createpages " + str(self.id) + " --settings=" + settings.SETTINGS_MODULE
            subprocess.Popen(cmd, shell=True)
            #print "New page creation process started..."
        
        # Creating images when DPP_IE_COMPATIBLE_PDF_VIEWER=True in settings.py    
        if getattr(settings, 'DPP_IE_COMPATIBLE_PDF_VIEWER', True) and self.old_document != self.document:
            cmd = u"python manage.py generatepdfimages " + str(self.id) + " --settings=" + settings.SETTINGS_MODULE
            subprocess.Popen(cmd, shell=True)
            #print "Image generation process started..."
        
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
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')


def delete_page_image(sender, **kwargs):
    instance = kwargs['instance']
    if os.path.exists(instance.get_filepath()):
        os.remove(instance.get_filepath())

pre_delete.connect(delete_page_image, sender=Page)


class SearchTag(models.Model):
    help_text = _("Documents containing these search tags are shown on the detail page of this object.")
    name = models.CharField(_("Name"), max_length=250, help_text=help_text)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    order = models.IntegerField(_("Order"), default=100, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['order']
        verbose_name = _('Search Tag')
        verbose_name_plural = _('Search Tags')


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
    content_object = GenericForeignKey('content_type', 'object_id')
    help_text = _("Page number in document")
    page = models.IntegerField(_("Page"), blank=True, null=True, help_text=help_text)
    
    def __unicode__(self):
        return unicode(self.research_request) + ', ' + unicode(self.content_object)
    
    class Meta:
        verbose_name = _('Relation with Project Element')
        verbose_name_plural = _('Relations with Project Elements')
    

class ResearchRequest(models.Model):
    help_text = _('Give a unique number to your request so that people can reference it (e.g. "R1", "R2",...)')
    nr = models.CharField(_("Nr"), max_length=8, help_text=help_text)
    title = models.CharField(_("Title"), max_length=250)
    open = models.BooleanField(_("Open"), default=True)
    description = models.TextField(_("Description"))
    date_added = models.DateTimeField(auto_now_add=True)
    activities = GenericRelation('ActivityLog')
    
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
        verbose_name = _('Research Request')
        verbose_name_plural = _('Research Requests')



class CommentRelation(models.Model):
    comment = models.ForeignKey('Comment')
    help_text = _('Type of the related object (ProjectPart, Question, Participant, Event, Document).')
    limit = RELATION_LIMIT
    content_type = models.ForeignKey(ContentType, help_text=help_text, limit_choices_to=limit)
    help_text = _('The id of the related object (you can find the id of an object in the url \
of the object change form in the admin).')
    object_id = models.PositiveIntegerField(help_text=help_text)
    content_object = GenericForeignKey('content_type', 'object_id')
    help_text = _("Page number in document")
    page = models.IntegerField(_("Page"), blank=True, null=True, help_text=help_text)
    
    def __unicode__(self):
        return unicode(self.comment) + ', ' + unicode(self.content_object)
    
    class Meta:
        verbose_name = _('Relation with Project Element')
        verbose_name_plural = _('Relations with Project Elements')

class Comment(models.Model):
    username = models.CharField(_("Username"), max_length=250)
    email = models.EmailField(_("Email"), max_length=250)
    help_text = _('User has given permission to get in contact via email.')
    feedback_allowed = models.BooleanField(_("Feedback allowed"), default=False, help_text=help_text)
    comment = models.TextField(_("Comment text"))
    help_text = _('Comment is only shown on page if published is true.')
    published = models.BooleanField(_("Published"), default=False, help_text=help_text)
    published_by = models.CharField(_("Published by"), max_length=250, blank=True)
    activation_hash = models.CharField(_("Activation hash"), max_length=250, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    activities = GenericRelation('ActivityLog')
    
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
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
    

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
    content_object = GenericForeignKey('content_type', 'object_id')
    type = models.CharField(_("Type"), max_length=2, choices=TYPE_CHOICES)
    info = models.CharField(_("Info"), max_length=250, blank=True)
    date = models.DateTimeField(_("Date"), auto_now_add=True)
    
    def __unicode__(self):
        return u'Activity: ' + unicode(self.content_object)
    
    class Meta:
        ordering = ['-date']
        verbose_name = _('Activity Log Entry')
        verbose_name_plural = _('Activity Log')


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
