from django_dynamic_fixture import G, N
from django.core.files import File
from public_project.models import *


class ProjectFactory():
    
    @classmethod
    def create_base_project(cls):
        sc   = G(SiteConfig, header_image=None)
        pp1 = G(ProjectPart)
        pp2 = G(ProjectPart)
        p1   = G(Participant)
        p1.name = "Test Corporation"
        p1.save()
        p2   = G(Participant)
        
        m = G(Membership)
        m.from_participant = p2
        m.to_participant = p1
        m.save()
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
        e1 = G(Event)
        e1.project_parts = [pp1,]
        e1.save()
        e2 = G(Event)
        e2.project_parts = [pp2,]
        e2.save()
        d1 = N(Document)
        pdf = File(open('fixtures/test_document.pdf', 'rw'))
        d1.document = pdf
        d1.save()
        
        