from django_dynamic_fixture import G, N
from django.core.files import File
from public_project.models import *


class ProjectFactory():
    
    @classmethod
    def create_base_project(cls):
        sc   = G(SiteConfig, header_image=None)
        p1   = G(Participant)
        p2   = G(Participant)
        pgg1 = G(ProjectGoalGroup)
        pg1  = G(ProjectGoal, project_goal_group=pgg1)
        pp1  = G(ProjectPart)
        q1   = G(Question)
        rr1  = G(ResearchRequest)
        rrr1 = G(ResearchRequestRelation, research_request=rr1)
        rrr1.content_object = q1
        rrr1.save()
        c1   = G(Comment, published=True)
        cr1  = G(CommentRelation, comment=c1)
        a1 = N(ActivityLog, type='NC')
        a1.content_object = c1
        a1.save()
        cr1.content_object = p1
        cr1.save()
        d1 = N(Document)
        pdf = File(open('fixtures/test_document.pdf', 'rw'))
        d1.document = pdf
        d1.save()
        
        