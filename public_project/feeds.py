from django.contrib.contenttypes.models import ContentType
from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from public_project.models import SiteConfig, ProjectPart, Question, Participant, Event, Document, ResearchRequest, Comment, ActivityLog


class ActivityFeed(Feed):
    item_guid_is_permalink = False
    
    def __init__(self, type, link):
        self.type = type
        self.link = '/' + link
        if SiteConfig.objects.count() == 0:
            return None
        site_config = SiteConfig.objects.get_site_config(None)
        if type == 'NA':
            self.title = site_config.short_title + ": " + _("Subject Areas")
            self.description = _("Feed with new subject areas from %s.") % site_config.short_title
        if type == 'NQ':
            self.title = site_config.short_title + ": " + _("Questions")
            self.description = _("Feed with new questions from %s.") % site_config.short_title
        if type == 'PA':
            self.title = site_config.short_title + ": " + _("Participants")
            self.description = _("Feed with new participants from %s.") % site_config.short_title
        if type == 'NE':
            self.title = site_config.short_title + ": " + _("Events")
            self.description = _("Feed with new events from %s.") % site_config.short_title
        if type == 'ND':
            self.title = site_config.short_title + ": " + _("Documents")
            self.description = _("Feed with new documents from %s.") % site_config.short_title
        if type  == None:
            self.title = site_config.short_title + ": " + _("Activities")
            self.description = _("General feed with all activities from %s.") % site_config.short_title
        super(ActivityFeed, self).__init__()
    
    def items(self):
        if self.type == None:
            return ActivityLog.objects.all()[:8]
        else:
            return ActivityLog.objects.filter(type=self.type)[:8]
    
    def item_title(self, item):
        title  = ''
        if self.type == None:
            title += item.get_type_display() + ": "
        title += unicode(item.content_object) 
        return title
    
    def item_description(self, item):
        if item.content_object:
            return item.content_object.get_feed_description()
        else:
            return ''
    
    def item_link(self, item):
        if item.content_object:
            return item.content_object.get_absolute_url()
        else:
            return ''
    
    def item_guid(self, item):
        if item.content_object:
            return item.content_object.get_absolute_url()
        else:
            return ''
    
    def item_pubdate(self, item):
        return item.date


class QuestionResearchRequestsFeed(Feed):
    item_guid_is_permalink = False
    
    def get_object(self, request, object_id):
        obj = get_object_or_404(Question, pk=object_id)
        self.set_config(obj)
        return obj
    
    def items(self, obj):
        content_type = ContentType.objects.get(app_label="public_project", model="question")
        research_request_list = ResearchRequest.objects.filter(researchrequestrelation__content_type=content_type).filter(researchrequestrelation__object_id=obj.id).distinct()
        return research_request_list[:8]
    
    def set_config(self, obj):
        site_config = SiteConfig.objects.get_site_config(None)
        self.link = obj.get_absolute_url() + _('research_requests_url')
        self.title = site_config.short_title + ": " + _("Research Requests on") + " " + unicode(obj)
        self.description = _("Feed with new research requests on {object} on {title}.").format(
            object = unicode(obj),
            title = site_config.short_title,
        )
    
    def item_title(self, item):
        return unicode(item)
    
    def item_description(self, item):
        return item.get_feed_description()
    
    def item_link(self, item):
        return item.get_absolute_url()
    
    def item_guid(self, item):
        return item.get_absolute_url()
    
    def item_pubdate(self, item):
        return item.date_added


class ObjectCommentsFeed(Feed):
    item_guid_is_permalink = False
    
    def set_config(self, obj):
        site_config = SiteConfig.objects.get_site_config(None)
        self.link = obj.get_absolute_url() + _('comments_url')
        self.title = site_config.short_title + ": " + _("Comments on") + " " + unicode(obj)
        self.description = _("Feed with new comments on {object} on {title}.").format(
            object = unicode(obj),
            title = site_config.short_title,
        )
    
    def item_title(self, item):
        return unicode(item)
    
    def item_description(self, item):
        return item.get_feed_description()
    
    def item_link(self, item):
        return item.get_absolute_url()
    
    def item_guid(self, item):
        return item.get_absolute_url()
    
    def item_pubdate(self, item):
        return item.date_added


class ProjectPartCommentsFeed(ObjectCommentsFeed):
    
    def get_object(self, request, object_id):
        obj = get_object_or_404(ProjectPart, pk=object_id)
        self.set_config(obj)
        return obj
    
    def items(self, obj):
        content_type = ContentType.objects.get(app_label="public_project", model="projectpart")
        comment_list = Comment.objects.filter(commentrelation__content_type=content_type).filter(commentrelation__object_id=obj.id).filter(published=True).distinct()
        return comment_list[:8]


class QuestionCommentsFeed(ObjectCommentsFeed):
    
    def get_object(self, request, object_id):
        obj = get_object_or_404(Question, pk=object_id)
        self.set_config(obj)
        return obj
    
    def items(self, obj):
        content_type = ContentType.objects.get(app_label="public_project", model="question")
        comment_list = Comment.objects.filter(commentrelation__content_type=content_type).filter(commentrelation__object_id=obj.id).filter(published=True).distinct()
        return comment_list[:8]


class ParticipantCommentsFeed(ObjectCommentsFeed):
    
    def get_object(self, request, object_id):
        obj = get_object_or_404(Participant, pk=object_id)
        self.set_config(obj)
        return obj
    
    def items(self, obj):
        content_type = ContentType.objects.get(app_label="public_project", model="participant")
        comment_list = Comment.objects.filter(commentrelation__content_type=content_type).filter(commentrelation__object_id=obj.id).filter(published=True).distinct()
        return comment_list[:8]


class EventCommentsFeed(ObjectCommentsFeed):
    
    def get_object(self, request, object_id):
        obj = get_object_or_404(Event, pk=object_id)
        self.set_config(obj)
        return obj
    
    def items(self, obj):
        content_type = ContentType.objects.get(app_label="public_project", model="event")
        comment_list = Comment.objects.filter(commentrelation__content_type=content_type).filter(commentrelation__object_id=obj.id).filter(published=True).distinct()
        return comment_list[:8]
    

class DocumentCommentsFeed(ObjectCommentsFeed):
    
    def get_object(self, request, object_id):
        obj = get_object_or_404(Document, pk=object_id)
        self.set_config(obj)
        return obj
    
    def items(self, obj):
        content_type = ContentType.objects.get(app_label="public_project", model="document")
        comment_list = Comment.objects.filter(commentrelation__content_type=content_type).filter(commentrelation__object_id=obj.id).filter(published=True).distinct()
        return comment_list[:8]