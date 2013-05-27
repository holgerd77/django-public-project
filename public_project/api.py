from tastypie import fields
from tastypie.resources import ModelResource
from public_project.models import ProjectPart, Question, Participant, Event, Page, Document


class ProjectPartsResource(ModelResource):
    
    class Meta:
        queryset = ProjectPart.objects.all()
        resource_name = 'project_parts'
        excludes = ['comments',]
        allowed_methods = ['get',]


class QuestionsResource(ModelResource):
    
    class Meta:
        queryset = Question.objects.all()
        resource_name = 'questions'
        excludes = ['comments',]
        allowed_methods = ['get',]


class ParticipantsResource(ModelResource):
    
    class Meta:
        queryset = Participant.objects.all()
        resource_name = 'participants'
        excludes = ['comments',]
        allowed_methods = ['get',]


class EventsResource(ModelResource):
    
    class Meta:
        queryset = Event.objects.all()
        resource_name = 'events'
        excludes = ['comments',]
        allowed_methods = ['get',]


class PagesResource(ModelResource):
    
    class Meta:
        queryset = Page.objects.all()
        resource_name = 'pages'
        allowed_methods = ['get',]
        

class DocumentsResource(ModelResource):
    pages = fields.ToManyField(PagesResource, 'page_set', null=True, full=True)
    
    class Meta:
        queryset = Document.objects.all()
        limit = 5
        resource_name = 'documents'
        excludes = ['pdf_images_generated', 'document', 'comments',]
        allowed_methods = ['get',]
