# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_column(u'public_project_image', 'attribution_html', 'attribution')


    def backwards(self, orm):
        db.rename_column(u'public_project_image', 'attribution', 'attribution_html')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'public_project.activitylog': {
            'Meta': {'ordering': "['-date']", 'object_name': 'ActivityLog'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'public_project.comment': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Comment'},
            'activation_hash': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '250'}),
            'feedback_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_by': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'public_project.commentrelation': {
            'Meta': {'object_name': 'CommentRelation'},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['public_project.Comment']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'page': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'public_project.document': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Document'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'document': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_documents'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['public_project.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_documents'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['public_project.Participant']"}),
            'pdf_images_generated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'project_parts': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_documents'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['public_project.ProjectPart']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'public_project.event': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Event'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'important': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_events'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['public_project.Participant']"}),
            'project_parts': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_events'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['public_project.ProjectPart']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'public_project.image': {
            'Meta': {'ordering': "['title']", 'object_name': 'Image'},
            'attribution': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'public_project.membership': {
            'Meta': {'object_name': 'Membership'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'from_participant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_memberships'", 'to': u"orm['public_project.Participant']"}),
            'function': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_participant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_memberships'", 'to': u"orm['public_project.Participant']"})
        },
        u'public_project.page': {
            'Meta': {'ordering': "['number']", 'object_name': 'Page'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['public_project.Document']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {})
        },
        u'public_project.participant': {
            'Meta': {'ordering': "['order', 'name']", 'object_name': 'Participant'},
            'belongs_to': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['public_project.Participant']", 'through': u"orm['public_project.Membership']", 'symmetrical': 'False'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '500', 'null': 'True', 'blank': 'True'})
        },
        u'public_project.projectgoal': {
            'Meta': {'ordering': "['order']", 'object_name': 'ProjectGoal'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '100', 'null': 'True', 'blank': 'True'}),
            'performance_figure': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'project_goal_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['public_project.ProjectGoalGroup']"})
        },
        u'public_project.projectgoalgroup': {
            'Meta': {'object_name': 'ProjectGoalGroup'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['public_project.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_current': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'project_part': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['public_project.ProjectPart']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'public_project.projectpart': {
            'Meta': {'ordering': "['order', 'name']", 'object_name': 'ProjectPart'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_project_parts': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['public_project.ProjectPart']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '500', 'null': 'True', 'blank': 'True'})
        },
        u'public_project.question': {
            'Meta': {'ordering': "['title']", 'object_name': 'Question'},
            'answer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'answered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'documents': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_documents'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['public_project.Document']"}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_questions'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['public_project.Event']"}),
            'explanations': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_questions'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['public_project.Participant']"}),
            'project_parts': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_questions'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['public_project.ProjectPart']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'public_project.researchrequest': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'ResearchRequest'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nr': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'open': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'public_project.researchrequestrelation': {
            'Meta': {'object_name': 'ResearchRequestRelation'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'page': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'research_request': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['public_project.ResearchRequest']"})
        },
        u'public_project.searchtag': {
            'Meta': {'ordering': "['order']", 'object_name': 'SearchTag'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '100', 'null': 'True', 'blank': 'True'})
        },
        u'public_project.searchtagcacheentry': {
            'Meta': {'ordering': "['-num_results']", 'object_name': 'SearchTagCacheEntry'},
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['public_project.Document']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_results': ('django.db.models.fields.IntegerField', [], {}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['public_project.SearchTag']"})
        },
        u'public_project.sitecategory': {
            'Meta': {'object_name': 'SiteCategory'},
            'category': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'documents': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_site_categories'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['public_project.Document']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'public_project.siteconfig': {
            'Meta': {'object_name': 'SiteConfig'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'contact_html': ('django.db.models.fields.TextField', [], {'default': "u'This text will be shown on the contact page.'"}),
            'desc_about': ('django.db.models.fields.TextField', [], {'default': "u'About text'"}),
            'footer_html': ('django.db.models.fields.TextField', [], {'default': "u'This text will be shown in the footer of the site.'"}),
            'header_image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['public_project.Image']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro_text': ('django.db.models.fields.TextField', [], {'default': "u'This is a project watch website.'"}),
            'navi_link_color': ('django.db.models.fields.CharField', [], {'default': "'#FFFFFF'", 'max_length': '7'}),
            'short_title': ('django.db.models.fields.CharField', [], {'default': "u'ProjectWatch'", 'max_length': '250'}),
            'sub_title': ('django.db.models.fields.CharField', [], {'default': "u'Project Website Subtitle'", 'max_length': '250'}),
            'sub_title_color': ('django.db.models.fields.CharField', [], {'default': "'#444444'", 'max_length': '7'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u'ProjectWatch'", 'max_length': '250'}),
            'title_color': ('django.db.models.fields.CharField', [], {'default': "'#990000'", 'max_length': '7'})
        },
        u'public_project.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'receive_new_comment_emails': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'public_project.websource': {
            'Meta': {'ordering': "['order']", 'object_name': 'WebSource'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['public_project']
