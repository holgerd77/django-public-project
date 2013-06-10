import datetime
from django.core.files import File
from public_project.models import *



class ExampleData:

    def create(self):
        
        sc = SiteConfig(
            title          = 'Tower of Babel',
            short_title    = 'Tower of Babel',
            sub_title      = "We will finish. Someday.",
            intro_text     = "This project is taking a litte longer than expected. Having some language problems " + \
                             " as well. But we will finish. We promise.",
            desc_about     = "This project website is run by Tower of Babel International, London, " + \
                             "but is not at all associated with the Babel Tower Coorporation, Antalya or the " + \
                             "Babel Tower Group, Jamaica.",
            footer_html    = "For questions ask Jim, John, Miranda or Turtle-Joey.",
            contact_html   = "Contact: no-reply@towerofbabelinternationalassociation.com",
        )
        sc.save()

        p1 = Participant(
            name             = 'Tower of Babel International',
            description      = 'We are the makers. We are the doers. The sky is the limit.',
        )
        p1.save()

        p2 = Participant(
            name             = 'Babel Tower Coorporation',
            description      = 'Former project responsibles. Hmm. Never met. Strange people.',
        )
        p2.save()
        
        
        #p = Project(
        #    name           = 'Tower of Babel',
        #    desc_project   = '"whose top may reach unto heaven" - that is the tower we want to build. ' + \
        #                     'Some may call us crazy. Some may call us naive. But we are determined and ' + \
        #                     'beside from having some language problems between some of our workers ' + \
        #                     'we are very much in our plan and will succeed!',
        #    desc_project_parts = 'We want to make everything as transparent as possible. Our trust ' + \
        #                         'in us is our trust in you.',
        #    desc_questions     = 'We try to work with you on common questions around the tower building here.',
        #    desc_participants  = 'Such an ambitious project has various actors involved. You can find them here.',
        #    desc_goal_groups   = 'We have adopted our goals over the centuries. See them here.',
        #    desc_process       = 'This is the building timeline of our amazing construction project.',
        #    desc_documents     = 'We want that you are able to take part. So we publish all construction documents here.',
        #)
        #p.save()
        #p.responsible_participants = [p1,]
        #p.former_responsible_participants = [p2,]
        #p.save()

        e1 = Event(
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
        e1.save()
        e1.participants = [p2,]
        e1.save()

        pgg1 = ProjectGoalGroup(
            title       = 'Initial Goals',
            event       = e1,
            description = 'We want to build a really high tower, the sky is the limit, at lease 5000 floors tall',
        )
        pgg1.save()

        pgg1_pg1 = ProjectGoal(
            project_goal_group = pgg1,
            name  = 'Floors',
            performance_figure = '5000+',
            order = 100,
        )
        pgg1_pg1.save()
        
        pgg1_pg2 = ProjectGoal(
            project_goal_group = pgg1,
            name = 'Beautiness',
            performance_figure = 'very beautiful',
            order = 200,
        )
        pgg1_pg2.save()

        p3 = Participant(
            name = 'Department of Stone Measurement (DOFSTON)',
            description = 'Responsible for all stone measurement certificates at building site',
        )
        p3.save()
        
        p4 = Participant(
            name = 'Mrs. Smith',
            description = 'Very geeky lady from the DOFSTON, but kind of nice.',
        )
        p4.save()
        p4.belongs_to = [p3,]
        p4.save()

        pp1 = ProjectPart(
            name = 'Stone Management',
            description = 'Management of stone acquistion, quality management and deposition.',
        )
        pp1.save()
        
        pp2 = ProjectPart(
            name = 'Certification',
            main_project_part = pp1,
            description = 'Certificates for stone measures, stone hole size compliance and stone authenticity.'
        )
        pp2.save()

        e2 = Event(
            title = 'No DOFSTON certificate, rebuilding of 500 first floors',
            event_type = 'IN',
            description = "The Department of Stone Measurements doesn't give us the certificate for the first " + \
                          "500 floors due to irregularities in stone dimensions, we are forced to rebuild.",
            date = '2005-07-15',
        )
        e2.save()
        e2.participants = [p2, p3,]
        e2.project_parts = [pp2,]
        e2.save()

        d1 = Document(
            title =       'DOFSTON Certificate Refusal',
            date =        '2005-06-23',
            description = 'Writing from Department of Stone Measurements about stone block certificate refusal.', 
        )
        pdf = File(open('ep_setup_app/docs/dofston_cert_refusal.pdf', 'rw'))
        d1.document = pdf
        d1.save()
        d1.project_parts = [pp2,]
        d1.participants = [p3,]
        d1.save()

        q1 = Question(
            title = 'Available stone deposits in the area',
            description = 'Due to the necessary rebuilding of the first 500 floors we are in need of stone ' + \
                          'deposition sites for temporarily shelving stones with wrong dimensions.',
        )
        q1.save()
        q1.project_parts = [pp1,]
        q1.participants = [p2, p3,]
        q1.save()
        
        q2 = Question(
            title = 'What is the role of Mrs. Smith?',
            description = 'Mrs. Smith plays a really dubious role in all this. ' + \
                          'We want to figure out what her role really is and why she did what she did.',
        )
        q2.save()
        q2.project_parts = [pp2,]
        q2.participants = [p4,]
        q2.save()
        
        e3 = Event(
            title = 'Mrs. Smith made a telephone call',
            event_type = 'IN',
            description = "On this day Mrs. Smith made a telephone call. Normally this woman never answers " + \
                          "the phone so this is obviously quite dubious.",
            date = '2005-03-22',
        )
        e3.save()
        e3.participants = [p4,]
        e3.project_parts = [pp1,]
        e3.save()
        
        d2 = Document(
            title =       'Transcript of telephone call Mrs. Smith',
            date =        '2005-03-25',
            description = 'Mrs. Smith made a phone call. Transcript was sent by anonymous caller.', 
        )
        pdf = File(open('ep_setup_app/docs/phonecall_mrs_smith.pdf', 'rw'))
        d2.document = pdf
        d2.save()
        d2.project_parts = [pp1,]
        d2.events = [e3,]
        d2.participants = [p4,]
        d2.save()























