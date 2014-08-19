import datetime
from django.core.files import File
from django.contrib.sites.models import Site
from public_project.models import *



class ExampleData:

    def create_site_config(self):
        self.site = Site.objects.all()[0]
        self.site.domain = '127.0.0.1:8075'
        self.site.name = '127.0.0.1:8075'
        self.site.save()
        
        self.sc = SiteConfig(
            title          = 'Tower of Babel',
            short_title    = 'Tower of Babel',
            intro_text     = "<p><b>We will finish. Someday.</b></p>This project is taking a litte longer than expected. Having some language problems " + \
                             " as well. But we will finish. We promise.",
            about_text     = "This project website is run by Tower of Babel International, London, " + \
                             "but is not at all associated with the Babel Tower Coorporation, Antalya or the " + \
                             "Babel Tower Group, Jamaica.",
            footer         = "For questions ask Jim, John, Miranda or Turtle-Joey.",
            contact_text   = "Contact: no-reply@towerofbabelinternationalassociation.com",
        )
        self.sc.save()
    
    
    def create_site_categories(self):
        self.scat1 = SiteCategory(
            category = 'home',
            intro_text = '"whose top may reach unto heaven" - that is the tower we want to build. ' + \
                         'Some may call us crazy. Some may call us naive. But we are determined and ' + \
                         'beside from having some language problems between some of our workers ' + \
                         'we are very much in our plan and will succeed!',    
        )
        self.scat1.save()
        
        self.scat2 = SiteCategory(
            category = 'project_parts',
            intro_text = 'We want to make everything as transparent as possible. Our trust ' + \
                         'in us is our trust in you.',    
        )
        self.scat2.save()
        
        self.scat3 = SiteCategory(
            category = 'questions',
            intro_text = 'We try to work with you on common questions around the tower building here.',    
        )
        self.scat3.save()
        
        self.scat4 = SiteCategory(
            category = 'participants',
            intro_text = 'Such an ambitious project has various actors involved. You can find them here.',    
        )
        self.scat4.save()
        
        self.scat5 = SiteCategory(
            category = 'goals',
            intro_text = 'We have adopted our goals over the centuries. See them here.',    
        )
        self.scat5.save()
        
        self.scat6 = SiteCategory(
            category = 'events',
            intro_text = 'This is the building timeline of our amazing construction project.',    
        )
        self.scat6.save()
        
        self.scat7 = SiteCategory(
            category = 'documents',
            intro_text = 'We want that you are able to take part. So we publish all construction documents here.',    
        )
        self.scat7.save()
    
    
    def create_project_parts(self):
        self.pp1 = ProjectPart(
            name = 'Stone Management',
            description = 'Management of stone acquistion, quality management and deposition.',
        )
        self.pp1.save()
        
        self.pp2 = ProjectPart(
            name = 'Certification',
            description = 'Certificates for stone measures, stone hole size compliance and stone authenticity.'
        )
        self.pp2.save()
        #pp2.main_project_parts = [pp1,],
        #pp2.save()
    
    
    def create_participants(self):
        
        self.pt1 = ParticipantType(
            name = 'Building Companies',
            order = 100,
        )
        self.pt1.save()
        
        self.pt2 = ParticipantType(
            name = 'Administration',
            order = 200,
        )
        self.pt2.save()
        
        self.p1 = Participant(
            name             = 'Tower of Babel International',
            description      = 'We are the makers. We are the doers. The sky is the limit.',
            type = self.pt1,
        )
        self.p1.save()

        self.p2 = Participant(
            name             = 'Babel Tower Coorporation',
            description      = 'Former project responsibles. Hmm. Never met. Strange people.',
            type = self.pt1,
        )
        self.p2.save()
        
        self.p3 = Participant(
            name = 'Department of Stone Measurement (DOFSTON)',
            description = 'Responsible for all stone measurement certificates at building site',
            type = self.pt2,
        )
        self.p3.save()
        
        self.p4 = Participant(
            name = 'Mrs. Smith',
            description = 'Very geeky lady from the DOFSTON, but kind of nice.',
        )
        self.p4.save()
        
        self.ws1 = WebSource(
            title = 'Official Website',
            url = 'http://www.spiegel.de',
            content_object = self.p4,
        )
        self.ws1.save()
        
        self.st1 = SearchTag(
            name = 'Smith',
            content_object = self.p4,
        )
        self.st1.save()
        
        self.m1 = Membership(
            from_participant = self.p4,
            to_participant = self.p3,
            function = 'Department Manager',
        )
        self.m1.save()
        
        self.c1 = Comment(
            username = 'Robert Gutherfeather',
            email = 'robgus@smirdenbroeth.co.uk',
            comment = 'Is Mrs. Smith THE Mrs. Smith I encountered in Durbanport in 1957?? How exciting!',
            published = True,
        )
        self.c1.save()
        
        self.cr1 = CommentRelation(
            comment = self.c1,
            content_object = self.p4,
        )
        self.cr1.save()
        
    
    
    def create_events(self):
        self.e1 = Event(
            title       = 'Begin of the construction work',
            event_type  = 'MI',
            important   = True,
            description = 'Start of the construction of the tower, great atmosphere, everybody was there ' + \
                          'and there was this spirit in the air, you could feel it, you know? ' + \
                          'Lots of tears, our Meta-CEO said a few words ("They are one people and have one ' + \
                          'language, and nothing will be withheld from them which they purpose to do.", whew), ' + \
                          'very emotional.',
            date        = '2002-05-12',
        )
        self.e1.save()
        self.e1.participants = [self.p2,]
        self.e1.save()
        
        self.e2 = Event(
            title = 'No DOFSTON certificate, rebuilding of 500 first floors',
            event_type = 'IN',
            description = "The Department of Stone Measurements doesn't give us the certificate for the first " + \
                          "500 floors due to irregularities in stone dimensions, we are forced to rebuild.",
            date = '2005-07-15',
        )
        self.e2.save()
        self.e2.participants = [self.p2, self.p3,]
        self.e2.project_parts = [self.pp2,]
        self.e2.save()
    
    
    def create_project_goals(self):
        self.pgg1 = ProjectGoalGroup(
            title       = 'Initial Goals',
            event       = self.e1,
            description = 'We want to build a really high tower, the sky is the limit, at lease 5000 floors tall',
        )
        self.pgg1.save()

        self.pgg1_pg1 = ProjectGoal(
            project_goal_group = self.pgg1,
            name  = 'Floors',
            performance_figure = '5000+',
            order = 100,
        )
        self.pgg1_pg1.save()
        
        self.pgg1_pg2 = ProjectGoal(
            project_goal_group = self.pgg1,
            name = 'Beautiness',
            performance_figure = 'very beautiful',
            order = 200,
        )
        self.pgg1_pg2.save()
    
    
    def create_documents(self):
        self.d1 = Document(
            title =       'DOFSTON Certificate Refusal',
            date =        '2005-06-23',
            description = 'Writing from Department of Stone Measurements about stone block certificate refusal.', 
        )
        pdf = File(open('ep_setup_app/docs/dofston_cert_refusal.pdf', 'rw'))
        self.d1.document = pdf
        self.d1.save()
        self.d1.project_parts = [self.pp2,]
        self.d1.participants = [self.p3,]
        self.d1.save()

        self.q1 = Question(
            title = 'Available stone deposits in the area',
            description = 'Due to the necessary rebuilding of the first 500 floors we are in need of stone ' + \
                          'deposition sites for temporarily shelving stones with wrong dimensions.',
        )
        self.q1.save()
        self.q1.project_parts = [self.pp1,]
        self.q1.participants = [self.p2, self.p3,]
        self.q1.save()
        
        self.q2 = Question(
            title = 'What is the role of Mrs. Smith?',
            description = 'Mrs. Smith plays a really dubious role in all this. ' + \
                          'We want to figure out what her role really is and why she did what she did.',
        )
        self.q2.save()
        self.q2.project_parts = [self.pp2,]
        self.q2.participants = [self.p4,]
        self.q2.save()
        
        self.e3 = Event(
            title = 'Mrs. Smith made a telephone call',
            event_type = 'IN',
            description = "On this day Mrs. Smith made a telephone call. Normally this woman never answers " + \
                          "the phone so this is obviously quite dubious.",
            date = '2005-03-22',
        )
        self.e3.save()
        self.e3.participants = [self.p4,]
        self.e3.project_parts = [self.pp1,]
        self.e3.save()
        
        self.d2 = Document(
            title =       'Transcript of telephone call Mrs. Smith',
            date =        '2005-03-25',
            description = 'Mrs. Smith made a phone call. Transcript was sent by anonymous caller.', 
        )
        pdf = File(open('ep_setup_app/docs/phonecall_mrs_smith.pdf', 'rw'))
        self.d2.document = pdf
        self.d2.save()
        self.d2.project_parts = [self.pp1,]
        self.d2.events = [self.e3,]
        self.d2.participants = [self.p4,]
        self.d2.save()
    
    
    def create(self):
        self.create_site_config()
        self.create_site_categories()
        self.create_project_parts()
        self.create_participants()
        self.create_events()
        self.create_project_goals()
        self.create_documents()
