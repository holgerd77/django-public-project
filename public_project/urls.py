from django.conf import settings
from django.conf.urls import include, patterns, url
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView
from tastypie.api import Api
from public_project.api import *
from public_project.feeds import *

handler404 = 'public_project.views.custom_404_view'

urlpatterns = patterns('',
)

if getattr(settings, 'DPP_PUBLIC_API', False):
    v01_api = Api(api_name='v0.1')
    v01_api.register(ProjectPartsResource())
    v01_api.register(QuestionsResource())
    v01_api.register(ParticipantsResource())
    v01_api.register(EventsResource())
    v01_api.register(PagesResource())
    v01_api.register(DocumentsResource())
    
    urlpatterns = patterns('',
        url(r'^api/$', 'public_project.views.api'),
        (r'^api/', include(v01_api.urls)),
        url(r'^dev/logo/$', TemplateView.as_view(template_name="dev/logo.html")),
    )

urlpatterns += patterns('',
    url(r'^xhr/universal_search/', 'public_project.views.xhr_universal_search', name='xhr_universal_search'),
    url(r'^xhr/document_tags/', 'public_project.views.xhr_document_tags', name='xhr_document_tags'),
    url(r'^$', 'public_project.views.index'),
    url(r'^rss/$', ActivityFeed(None, '')),
    url(r'^%s$' % _('comments_url'), 'public_project.views.comments', {'object_id': None, 'content_type': None}),
    url(r'^%srss/$' % _('comments_url'), ActivityFeed('NC', _('comments_url'))),
    url(r'^404test/$', 'public_project.views.custom_404_view'),
    #ProjectParts
    url(r'^%s$' % _('project_parts_url'), 'public_project.views.project_parts'),
    url(r'^%srss/$' % _('project_parts_url'), ActivityFeed('NA', _('project_parts_url'))),
    url(r'^%s[a-z\d\-]+-(?P<project_part_id>\d+)/$' % _('project_parts_url'), 'public_project.views.project_part'),
    url(r'^%s(?P<object_id>\d+)/%s$' % (_('project_parts_url'), _('comments_url')), 'public_project.views.comments', {'content_type': 'project_part'}),
    url(r'^%s(?P<object_id>\d+)/%srss/$' % (_('project_parts_url'), _('comments_url')), ProjectPartCommentsFeed()),
    url(r'^%s$' % _('goals_url'), 'public_project.views.goals'),
    #Questions
    url(r'^%s$' % _('questions_url'), 'public_project.views.questions'),
    url(r'^%s%s$' % (_('questions_url'), _('research_requests_url')), 'public_project.views.research_requests', {'object_id': None, 'content_type': None}),
    url(r'^%s%srss/$' % (_('questions_url'), _('research_requests_url')), ActivityFeed('RR', _('research_requests_url'))),
    url(r'^%s[a-z\d\-]+-(?P<question_id>\d+)/$' % _('questions_url'), 'public_project.views.question'),
    url(r'^%s(?P<object_id>\d+)/%s$' % (_('questions_url'), _('research_requests_url')), 'public_project.views.research_requests', {'content_type': 'question'}),
    url(r'^%s(?P<object_id>\d+)/%srss/$' % (_('questions_url'), _('research_requests_url')), QuestionResearchRequestsFeed()),
    url(r'^%srss/$' % _('questions_url'), ActivityFeed('NQ', _('questions_url'))),
    url(r'^%s(?P<object_id>\d+)/%s$' % (_('questions_url'), _('comments_url')), 'public_project.views.comments', {'content_type': 'question'}),
    url(r'^%s(?P<object_id>\d+)/%srss/$' % (_('questions_url'), _('comments_url')), QuestionCommentsFeed()),
    #Events
    url(r'^%s$' % _('events_url'), 'public_project.views.events'),
    url(r'^%srss/$' % _('events_url'), ActivityFeed('NE', _('events_url'))),
    url(r'^%s[a-z\d\-]+-(?P<event_id>\d+)/$' % _('events_url'), 'public_project.views.event'),
    url(r'^%s(?P<object_id>\d+)/%s$' % (_('events_url'), _('comments_url')), 'public_project.views.comments', {'content_type': 'event'}),
    url(r'^%s(?P<object_id>\d+)/%srss/$' % (_('events_url'), _('comments_url')), EventCommentsFeed()),
    #Participants
    url(r'^%s$' % _('participants_url'), 'public_project.views.participants'),
    url(r'^%srss/$' % _('participants_url'), ActivityFeed('PA', _('participants_url'))),
    url(r'^%s[a-z\d\-]+-(?P<participant_id>\d+)/$' % _('participants_url'), 'public_project.views.participant'),
    url(r'^%s(?P<object_id>\d+)/%s$' % (_('participants_url'), _('comments_url')), 'public_project.views.comments', {'content_type': 'participant'}),
    url(r'^%s(?P<object_id>\d+)/%srss/$' % (_('participants_url'), _('comments_url')), ParticipantCommentsFeed()),
    
    url(r'^%s(?P<web_source_id>\d+)/$' % _('web_sources_url'), 'public_project.views.web_source'),
    
    #Documents
    url(r'^%s$' % _('documents_url'), 'public_project.views.documents'),
    url(r'^%srss/$' % _('documents_url'), ActivityFeed('ND', _('documents_url'))),
    url(r'^%s[a-z\d\-]+-(?P<document_id>\d+)/$' % _('documents_url'), 'public_project.views.document'),
    url(r'^%s(?P<object_id>\d+)/%s$' % (_('documents_url'), _('comments_url')), 'public_project.views.comments', {'content_type': 'document'}),
    url(r'^%s(?P<object_id>\d+)/%srss/$' % (_('documents_url'), _('comments_url')), DocumentCommentsFeed()),
    url(r'^%s$' %  _('search_url'), 'public_project.views.search'),
    url(r'^%s$' % _('contact_url'), 'public_project.views.contact'),
    url(r'^%s$' % _('activate_comment_url'), 'public_project.views.activate_comment'),
)
                       
