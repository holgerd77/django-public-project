# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'public_project_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('receive_new_comment_emails', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'public_project', ['UserProfile'])

        # Adding model 'Image'
        db.create_table(u'public_project_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('attribution_html', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal(u'public_project', ['Image'])

        # Adding model 'SiteConfig'
        db.create_table(u'public_project_siteconfig', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default=u'ProjectWatch', max_length=250)),
            ('short_title', self.gf('django.db.models.fields.CharField')(default=u'ProjectWatch', max_length=250)),
            ('title_color', self.gf('django.db.models.fields.CharField')(default='#990000', max_length=7)),
            ('sub_title', self.gf('django.db.models.fields.CharField')(default=u'Project Website Subtitle', max_length=250)),
            ('sub_title_color', self.gf('django.db.models.fields.CharField')(default='#444444', max_length=7)),
            ('intro_text', self.gf('django.db.models.fields.TextField')(default=u'This is a project watch website.')),
            ('header_image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['public_project.Image'], null=True, blank=True)),
            ('header_bg_color', self.gf('django.db.models.fields.CharField')(default='#EEEEEE', max_length=7)),
            ('navi_link_color', self.gf('django.db.models.fields.CharField')(default='#FFFFFF', max_length=7)),
            ('navi_bg_color', self.gf('django.db.models.fields.CharField')(default='#333333', max_length=7)),
            ('important_bg_color', self.gf('django.db.models.fields.CharField')(default='#990000', max_length=7)),
            ('desc_about', self.gf('django.db.models.fields.TextField')()),
            ('footer_html', self.gf('django.db.models.fields.TextField')(default=u'This text will be shown in the footer of the site.')),
            ('contact_html', self.gf('django.db.models.fields.TextField')(default=u'This text will be shown on the contact page.')),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'public_project', ['SiteConfig'])

        # Adding model 'WebSource'
        db.create_table(u'public_project_websource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'public_project', ['WebSource'])

        # Adding model 'Participant'
        db.create_table(u'public_project_participant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('participant_type', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'public_project', ['Participant'])

        # Adding model 'Project'
        db.create_table(u'public_project_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('desc_project', self.gf('django.db.models.fields.TextField')()),
            ('desc_project_parts', self.gf('django.db.models.fields.TextField')()),
            ('desc_questions', self.gf('django.db.models.fields.TextField')()),
            ('desc_participants', self.gf('django.db.models.fields.TextField')()),
            ('desc_goal_groups', self.gf('django.db.models.fields.TextField')()),
            ('desc_process', self.gf('django.db.models.fields.TextField')()),
            ('desc_documents', self.gf('django.db.models.fields.TextField')()),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'public_project', ['Project'])

        # Adding M2M table for field responsible_participants on 'Project'
        db.create_table(u'public_project_project_responsible_participants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'public_project.project'], null=False)),
            ('participant', models.ForeignKey(orm[u'public_project.participant'], null=False))
        ))
        db.create_unique(u'public_project_project_responsible_participants', ['project_id', 'participant_id'])

        # Adding M2M table for field former_responsible_participants on 'Project'
        db.create_table(u'public_project_project_former_responsible_participants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'public_project.project'], null=False)),
            ('participant', models.ForeignKey(orm[u'public_project.participant'], null=False))
        ))
        db.create_unique(u'public_project_project_former_responsible_participants', ['project_id', 'participant_id'])

        # Adding model 'ProjectPart'
        db.create_table(u'public_project_projectpart', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'public_project', ['ProjectPart'])

        # Adding model 'Event'
        db.create_table(u'public_project_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('event_type', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('important', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'public_project', ['Event'])

        # Adding M2M table for field participants on 'Event'
        db.create_table(u'public_project_event_participants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'public_project.event'], null=False)),
            ('participant', models.ForeignKey(orm[u'public_project.participant'], null=False))
        ))
        db.create_unique(u'public_project_event_participants', ['event_id', 'participant_id'])

        # Adding M2M table for field project_parts on 'Event'
        db.create_table(u'public_project_event_project_parts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'public_project.event'], null=False)),
            ('projectpart', models.ForeignKey(orm[u'public_project.projectpart'], null=False))
        ))
        db.create_unique(u'public_project_event_project_parts', ['event_id', 'projectpart_id'])

        # Adding model 'Question'
        db.create_table(u'public_project_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('answered', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('explanations', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('answer', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'public_project', ['Question'])

        # Adding M2M table for field project_parts on 'Question'
        db.create_table(u'public_project_question_project_parts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm[u'public_project.question'], null=False)),
            ('projectpart', models.ForeignKey(orm[u'public_project.projectpart'], null=False))
        ))
        db.create_unique(u'public_project_question_project_parts', ['question_id', 'projectpart_id'])

        # Adding M2M table for field participants on 'Question'
        db.create_table(u'public_project_question_participants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm[u'public_project.question'], null=False)),
            ('participant', models.ForeignKey(orm[u'public_project.participant'], null=False))
        ))
        db.create_unique(u'public_project_question_participants', ['question_id', 'participant_id'])

        # Adding M2M table for field events on 'Question'
        db.create_table(u'public_project_question_events', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm[u'public_project.question'], null=False)),
            ('event', models.ForeignKey(orm[u'public_project.event'], null=False))
        ))
        db.create_unique(u'public_project_question_events', ['question_id', 'event_id'])

        # Adding M2M table for field documents on 'Question'
        db.create_table(u'public_project_question_documents', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm[u'public_project.question'], null=False)),
            ('document', models.ForeignKey(orm[u'public_project.document'], null=False))
        ))
        db.create_unique(u'public_project_question_documents', ['question_id', 'document_id'])

        # Adding model 'ProjectGoalGroup'
        db.create_table(u'public_project_projectgoalgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['public_project.Event'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'public_project', ['ProjectGoalGroup'])

        # Adding model 'ProjectGoal'
        db.create_table(u'public_project_projectgoal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('project_goal_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['public_project.ProjectGoalGroup'])),
            ('performance_figure', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'public_project', ['ProjectGoal'])

        # Adding model 'Document'
        db.create_table(u'public_project_document', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('document', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('pdf_images_generated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'public_project', ['Document'])

        # Adding M2M table for field participants on 'Document'
        db.create_table(u'public_project_document_participants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('document', models.ForeignKey(orm[u'public_project.document'], null=False)),
            ('participant', models.ForeignKey(orm[u'public_project.participant'], null=False))
        ))
        db.create_unique(u'public_project_document_participants', ['document_id', 'participant_id'])

        # Adding M2M table for field project_parts on 'Document'
        db.create_table(u'public_project_document_project_parts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('document', models.ForeignKey(orm[u'public_project.document'], null=False)),
            ('projectpart', models.ForeignKey(orm[u'public_project.projectpart'], null=False))
        ))
        db.create_unique(u'public_project_document_project_parts', ['document_id', 'projectpart_id'])

        # Adding M2M table for field events on 'Document'
        db.create_table(u'public_project_document_events', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('document', models.ForeignKey(orm[u'public_project.document'], null=False)),
            ('event', models.ForeignKey(orm[u'public_project.event'], null=False))
        ))
        db.create_unique(u'public_project_document_events', ['document_id', 'event_id'])

        # Adding model 'Page'
        db.create_table(u'public_project_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['public_project.Document'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'public_project', ['Page'])

        # Adding model 'SearchTag'
        db.create_table(u'public_project_searchtag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'public_project', ['SearchTag'])

        # Adding model 'SearchTagCacheEntry'
        db.create_table(u'public_project_searchtagcacheentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['public_project.SearchTag'])),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['public_project.Document'])),
            ('num_results', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'public_project', ['SearchTagCacheEntry'])

        # Adding model 'ResearchRequestRelation'
        db.create_table(u'public_project_researchrequestrelation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('research_request', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['public_project.ResearchRequest'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('page', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'public_project', ['ResearchRequestRelation'])

        # Adding model 'ResearchRequest'
        db.create_table(u'public_project_researchrequest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nr', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('open', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'public_project', ['ResearchRequest'])

        # Adding model 'CommentRelation'
        db.create_table(u'public_project_commentrelation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['public_project.Comment'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('page', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'public_project', ['CommentRelation'])

        # Adding model 'Comment'
        db.create_table(u'public_project_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=250)),
            ('feedback_allowed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('published_by', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('activation_hash', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'public_project', ['Comment'])

        # Adding model 'ActivityLog'
        db.create_table(u'public_project_activitylog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'public_project', ['ActivityLog'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table(u'public_project_userprofile')

        # Deleting model 'Image'
        db.delete_table(u'public_project_image')

        # Deleting model 'SiteConfig'
        db.delete_table(u'public_project_siteconfig')

        # Deleting model 'WebSource'
        db.delete_table(u'public_project_websource')

        # Deleting model 'Participant'
        db.delete_table(u'public_project_participant')

        # Deleting model 'Project'
        db.delete_table(u'public_project_project')

        # Removing M2M table for field responsible_participants on 'Project'
        db.delete_table('public_project_project_responsible_participants')

        # Removing M2M table for field former_responsible_participants on 'Project'
        db.delete_table('public_project_project_former_responsible_participants')

        # Deleting model 'ProjectPart'
        db.delete_table(u'public_project_projectpart')

        # Deleting model 'Event'
        db.delete_table(u'public_project_event')

        # Removing M2M table for field participants on 'Event'
        db.delete_table('public_project_event_participants')

        # Removing M2M table for field project_parts on 'Event'
        db.delete_table('public_project_event_project_parts')

        # Deleting model 'Question'
        db.delete_table(u'public_project_question')

        # Removing M2M table for field project_parts on 'Question'
        db.delete_table('public_project_question_project_parts')

        # Removing M2M table for field participants on 'Question'
        db.delete_table('public_project_question_participants')

        # Removing M2M table for field events on 'Question'
        db.delete_table('public_project_question_events')

        # Removing M2M table for field documents on 'Question'
        db.delete_table('public_project_question_documents')

        # Deleting model 'ProjectGoalGroup'
        db.delete_table(u'public_project_projectgoalgroup')

        # Deleting model 'ProjectGoal'
        db.delete_table(u'public_project_projectgoal')

        # Deleting model 'Document'
        db.delete_table(u'public_project_document')

        # Removing M2M table for field participants on 'Document'
        db.delete_table('public_project_document_participants')

        # Removing M2M table for field project_parts on 'Document'
        db.delete_table('public_project_document_project_parts')

        # Removing M2M table for field events on 'Document'
        db.delete_table('public_project_document_events')

        # Deleting model 'Page'
        db.delete_table(u'public_project_page')

        # Deleting model 'SearchTag'
        db.delete_table(u'public_project_searchtag')

        # Deleting model 'SearchTagCacheEntry'
        db.delete_table(u'public_project_searchtagcacheentry')

        # Deleting model 'ResearchRequestRelation'
        db.delete_table(u'public_project_researchrequestrelation')

        # Deleting model 'ResearchRequest'
        db.delete_table(u'public_project_researchrequest')

        # Deleting model 'CommentRelation'
        db.delete_table(u'public_project_commentrelation')

        # Deleting model 'Comment'
        db.delete_table(u'public_project_comment')

        # Deleting model 'ActivityLog'
        db.delete_table(u'public_project_activitylog')


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
            'attribution_html': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'public_project.page': {
            'Meta': {'ordering': "['number']", 'object_name': 'Page'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['public_project.Document']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {})
        },
        u'public_project.participant': {
            'Meta': {'ordering': "['name']", 'object_name': 'Participant'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'participant_type': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'public_project.project': {
            'Meta': {'object_name': 'Project'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desc_documents': ('django.db.models.fields.TextField', [], {}),
            'desc_goal_groups': ('django.db.models.fields.TextField', [], {}),
            'desc_participants': ('django.db.models.fields.TextField', [], {}),
            'desc_process': ('django.db.models.fields.TextField', [], {}),
            'desc_project': ('django.db.models.fields.TextField', [], {}),
            'desc_project_parts': ('django.db.models.fields.TextField', [], {}),
            'desc_questions': ('django.db.models.fields.TextField', [], {}),
            'former_responsible_participants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'formerly_responsible_for_project'", 'symmetrical': 'False', 'to': u"orm['public_project.Participant']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'responsible_participants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'responsible_for_project'", 'symmetrical': 'False', 'to': u"orm['public_project.Participant']"})
        },
        u'public_project.projectgoal': {
            'Meta': {'ordering': "['order']", 'object_name': 'ProjectGoal'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'public_project.projectpart': {
            'Meta': {'ordering': "['order']", 'object_name': 'ProjectPart'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
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
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'public_project.searchtagcacheentry': {
            'Meta': {'ordering': "['-num_results']", 'object_name': 'SearchTagCacheEntry'},
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['public_project.Document']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_results': ('django.db.models.fields.IntegerField', [], {}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['public_project.SearchTag']"})
        },
        u'public_project.siteconfig': {
            'Meta': {'object_name': 'SiteConfig'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'contact_html': ('django.db.models.fields.TextField', [], {'default': "u'This text will be shown on the contact page.'"}),
            'desc_about': ('django.db.models.fields.TextField', [], {}),
            'footer_html': ('django.db.models.fields.TextField', [], {'default': "u'This text will be shown in the footer of the site.'"}),
            'header_bg_color': ('django.db.models.fields.CharField', [], {'default': "'#EEEEEE'", 'max_length': '7'}),
            'header_image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['public_project.Image']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'important_bg_color': ('django.db.models.fields.CharField', [], {'default': "'#990000'", 'max_length': '7'}),
            'intro_text': ('django.db.models.fields.TextField', [], {'default': "u'This is a project watch website.'"}),
            'navi_bg_color': ('django.db.models.fields.CharField', [], {'default': "'#333333'", 'max_length': '7'}),
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
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['public_project']