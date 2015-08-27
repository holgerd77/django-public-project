from django import forms
from django.db.models import Count
from django.contrib import admin, messages
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.actions import delete_selected
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _
from public_project.models import *


def get_num_search_tags(obj):
    num = obj.search_tags.count()
    if num > 0:
        return str(num)
    else:
        return ""

def get_num_web_sources(obj):
    num = obj.web_sources.count()
    if num > 0:
        return str(num)
    else:
        return ""

def get_num_project_parts(obj):
    num = obj.project_parts.count()
    if num > 0:
        return str(num)
    else:
        return ""

def get_num_participants(obj):
    num = obj.participants.count()
    if num > 0:
        return str(num)
    else:
        return ""

def get_num_events(obj):
    num = obj.events.count()
    if num > 0:
        return str(num)
    else:
        return ""

def get_num_documents(obj):
    num = obj.documents.count()
    if num > 0:
        return str(num)
    else:
        return ""

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )


class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_url', 'attribution_with_url',)
    search_fields = ['title',]
    
    def image_url(self, obj):
        return '<a href="' + obj.image.url + '" target="_blank">' + obj.image.url + '</a>'
    image_url.allow_tags = True
    image_url.short_description = _('Image')
    
    def attribution_with_url(self, obj):
        if obj.attribution_url:
            return '<a href="' + obj.attribution_url + '" target="_blank">' + obj.attribution + '</a>'
        else:
            return obj.attribution
    attribution_with_url.allow_tags = True
    attribution_with_url.short_description = _('Attribution')


class WebSourceInline(GenericTabularInline):
    model = WebSource


class CustomSiteConfigAdminForm(forms.ModelForm):
    intro_text = forms.CharField(widget=forms.Textarea(attrs={'class':'htmleditor'}))
    about_text = forms.CharField(widget=forms.Textarea(attrs={'class':'htmleditor'}))
    footer = forms.CharField(widget=forms.Textarea(attrs={'class':'htmleditor'}))
    contact_text = forms.CharField(widget=forms.Textarea(attrs={'class':'htmleditor'}))


class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_title', 'title_color',)
    save_on_top = True
    form = CustomSiteConfigAdminForm


class CustomSiteCategoryAdminForm(forms.ModelForm):
    intro_text = forms.CharField(widget=forms.Textarea(attrs={'class':'htmleditor'}))


class SiteCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'num_documents', 'num_web_sources')
    save_on_top = True
    inlines = [
        WebSourceInline,
    ]
    filter_horizontal = ('documents',)
    form = CustomSiteCategoryAdminForm
    
    def num_documents(self, obj):
        return get_num_documents(obj)
    num_documents.short_description = _('Documents')
    
    def num_web_sources(self, obj):
        return get_num_web_sources(obj)
    num_web_sources.short_description = _('Web sources')


class ParticipantTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'order',)
    list_editable = ('order',)


class SearchTagInline(GenericTabularInline):
    model = SearchTag


class CustomMembershipAdminForm(forms.ModelForm):
    
    def clean_to_participant(self):
        to_p = self.cleaned_data['to_participant']
        from_p = self.cleaned_data['from_participant']
        if to_p == from_p:
            raise forms.ValidationError(_("A participant can't have a membership with itself. At least in this system."))
        if to_p.from_memberships.count() > 0:
            raise forms.ValidationError(_("A participant can't belong to a participant which already belongs to another participant. Things would get to complicated."))
        return to_p

class MembershipInline(admin.TabularInline):
    model = Membership
    fk_name = 'from_participant'
    form = CustomMembershipAdminForm


class IsGroupFilter(SimpleListFilter):
    title = _('Is Group')
    parameter_name = 'is_group'
    
    def lookups(self, request, model_admin):
        return (
            ('groups', _('Only groups')),
        )
    
    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        return queryset.annotate(count=Count('belongs_to')).filter(count=0)


class GroupMembersFilter(SimpleListFilter):    
    title = _('Group Members')
    parameter_name = 'group_members'
    
    def lookups(self, request, model_admin):
        groups = Participant.objects.annotate(count=Count('belongs_to')).filter(count=0)
        
        lookups = []
        
        for group in groups:
            lookups.append((group.id, unicode(group),))
        return tuple(lookups)
    
    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        memberships = Membership.objects.filter(to_participant=int(self.value()))
        from_participants = []
        for m in memberships:
            from_participants.append(m.from_participant.id)
        #from_participants.append(int(self.value()))
        return queryset.filter(id__in=from_participants)
    

class CustomParticipantAdminForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'htmleditor'}))


class ParticipantAdmin(admin.ModelAdmin):
    actions = ['delete_selected',]
    list_display = ('name', 'type', 'order', 'is_group', 'in_num_groups', 'num_search_tags', 'num_web_sources',)
    list_editable = ('type', 'order',)
    list_filter = ('type', IsGroupFilter, GroupMembersFilter,)
    search_fields = ['name', 'description',]
    save_on_top = True
    inlines = [
        MembershipInline,
        SearchTagInline,
        WebSourceInline,
    ]
    form = CustomParticipantAdminForm
    
    def is_group(self, obj):
        if obj.from_memberships.count() == 0:
            return True
        else:
            return False
    is_group.boolean = True
    is_group.short_description = _('Is Group')
    
    def in_num_groups(self, obj):
        if obj.from_memberships.count() > 0:
            return str(obj.from_memberships.count())
        else:
            return ""
    in_num_groups.short_description = _('In number of groups')
    
    def num_search_tags(self, obj):
        return get_num_search_tags(obj)
    num_search_tags.short_description = _('Search tags')
    
    def num_web_sources(self, obj):
        return get_num_web_sources(obj)
    num_web_sources.short_description = _('Web sources')
    
    def delete_warning_msg(self, request, participant):
        msg  = _('The following associations with "%s" will be deleted') % unicode(participant)  + u': '
        msg += u'%i Events, ' % participant.related_events.count()
        msg += u'%i Documents' % participant.related_documents.count()
        messages.warning(request, msg)

    def delete_view(self, request, object_id, extra_context=None):
        self.delete_warning_msg(request, Participant.objects.get(pk=object_id))
        return super(ParticipantAdmin, self).delete_view(request, object_id, extra_context)
    
    def delete_selected(self, request, queryset):
        for object in queryset.all():
            self.delete_warning_msg(request, object)
        return delete_selected(self, request, queryset)


class CustomProjectPartAdminForm(forms.ModelForm):
    
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'htmleditor'}))

    def clean_main_project_parts(self):
        data = self.cleaned_data['main_project_parts']
        for main_pp in data.all():
            if main_pp.main_project_parts.count() > 0:
                raise forms.ValidationError(_("A project part can't have a main project part which has a main project part itself. Things would get to complicated."))
        return data


class IsMainProjectPartFilter(SimpleListFilter):
    title = _('Is Main Topic')
    parameter_name = 'is_main_topic'
    
    def lookups(self, request, model_admin):
        return (
            ('main_project_parts', _('Only main topics')),
        )
    
    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        return queryset.annotate(count=Count('main_project_parts')).filter(count=0)


class MainProjectPartFilter(SimpleListFilter):    
    title = _('Main Topics')
    parameter_name = 'main_topics'
    
    def lookups(self, request, model_admin):
        main_project_parts = ProjectPart.objects.annotate(count=Count('main_project_parts')).filter(count=0)
        
        lookups = []
        
        for main_pp in main_project_parts:
            lookups.append((main_pp.id, unicode(main_pp),))
        return tuple(lookups)
    
    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        
        return queryset.filter(main_project_parts__in=[int(self.value()),])
        


class ProjectPartAdmin(admin.ModelAdmin):
    actions = ['delete_selected',]
    list_display = ('name', 'order', 'is_main_project_part', 'in_num_main_project_parts', 'num_search_tags', 'num_web_sources')
    list_editable = ('order',)
    list_filter = (IsMainProjectPartFilter, MainProjectPartFilter,)
    search_fields = ['name',]
    save_on_top = True
    inlines = [
        SearchTagInline,
        WebSourceInline,
    ]
    filter_horizontal = ('main_project_parts',)
    form = CustomProjectPartAdminForm
    
    def is_main_project_part(self, obj):
        if obj.main_project_parts.count() == 0:
            return True
        else:
            return False
    is_main_project_part.boolean = True
    is_main_project_part.short_description = _('Is Main Topic')
    
    def in_num_main_project_parts(self, obj):
        if obj.main_project_parts.count() > 0:
            return str(obj.main_project_parts.count())
        else:
            return ""
    in_num_main_project_parts.short_description = _('Main Topics')
    
    def num_search_tags(self, obj):
        return get_num_search_tags(obj)
    num_search_tags.short_description = _('Search tags')
    
    def num_web_sources(self, obj):
        return get_num_web_sources(obj)
    num_web_sources.short_description = _('Web sources')
    
    def delete_warning_msg(self, request, project_part):
        msg  = _('The following associations with "%s" will be deleted') % unicode(project_part)  + u': '
        msg += u'%i Events, ' % project_part.related_events.count()
        msg += u'%i Documents' % project_part.related_documents.count()
        messages.warning(request, msg)

    def delete_view(self, request, object_id, extra_context=None):
        self.delete_warning_msg(request, ProjectPart.objects.get(pk=object_id))
        return super(ProjectPartAdmin, self).delete_view(request, object_id, extra_context)
    
    def delete_selected(self, request, queryset):
        for object in queryset.all():
            self.delete_warning_msg(request, object)
        return delete_selected(self, request, queryset)


class CustomEventAdminForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'htmleditor'}))


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'important', 'date', 'num_project_parts', 'num_participants', 'num_search_tags', 'num_web_sources',)
    filter_horizontal = ('project_parts', 'participants',)
    inlines = [
        SearchTagInline,
        WebSourceInline,
    ]
    list_filter = ('event_type', 'important',)
    search_fields = ['title', 'description',]
    save_on_top = True
    form = CustomEventAdminForm
    
    def num_project_parts(self, obj):
        return get_num_project_parts(obj)
    num_project_parts.short_description = _('Topics')
    
    def num_participants(self, obj):
        return get_num_participants(obj)
    num_participants.short_description = _('Participants')
    
    def num_search_tags(self, obj):
        return get_num_search_tags(obj)
    num_search_tags.short_description = _('Search tags')
    
    def num_web_sources(self, obj):
        return get_num_web_sources(obj)
    num_web_sources.short_description = _('Web sources')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'answered', 'num_project_parts', 'num_participants', 'num_events', 'num_documents', 'num_web_sources',)
    search_fields = ['title',]
    inlines = [
        WebSourceInline,
    ]
    filter_horizontal = ('project_parts', 'participants', 'events', 'documents')
    save_on_top = True
    
    def num_project_parts(self, obj):
        return get_num_project_parts(obj)
    num_project_parts.short_description = _('Topics')
    
    def num_participants(self, obj):
        return get_num_participants(obj)
    num_participants.short_description = _('Participants')
    
    def num_events(self, obj):
        return get_num_events(obj)
    num_events.short_description = _('Events')
    
    def num_documents(self, obj):
        return get_num_documents(obj)
    num_documents.short_description = _('Documents')
    
    def num_web_sources(self, obj):
        return get_num_web_sources(obj)
    num_web_sources.short_description = _('Web sources')


class ProjectGoalInline(admin.StackedInline):
    model = ProjectGoal


class ProjectGoalGroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'event', 'project_part', 'is_current', 'num_performance_figures',)
    save_on_top = True
    inlines = [
        ProjectGoalInline,
    ]
    
    def num_performance_figures(self, obj):
        num = obj.projectgoal_set.count()
        if num > 0:
            return str(num)
        else:
            return ""
    num_performance_figures.short_description = _('Performance figures')


class CustomDocumentAdminForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'htmleditor'}))
    
    class Meta:
        exclude = ('pdf_images_generated',)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'document', 'date', 'num_project_parts', 'num_participants', 'num_events',)
    search_fields = ['title', 'description',]
    filter_horizontal = ('participants', 'project_parts', 'events',)
    save_on_top = True
    form = CustomDocumentAdminForm
    
    def num_project_parts(self, obj):
        return get_num_project_parts(obj)
    num_project_parts.short_description = _('Topics')
    
    def num_participants(self, obj):
        return get_num_participants(obj)
    num_participants.short_description = _('Participants')
    
    def num_events(self, obj):
        return get_num_events(obj)
    num_events.short_description = _('Events')


class PageAdmin(admin.ModelAdmin):
    list_display = ('document', 'number')


class SearchTagCacheEntryAdmin(admin.ModelAdmin):
    list_display = ('tag', 'document', 'num_results')


class ResearchRequestInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        # get forms that actually have valid data
        count = 0
        rr_content_type = ContentType.objects.get(app_label='public_project', model='question')
        for form in self.forms:
            try:
                if form.cleaned_data:
                    if form.cleaned_data['content_type'] == rr_content_type:
                        count += 1
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        if count < 1:
            raise forms.ValidationError(_('A research request must be associated with a question'))


class ResearchRequestRelationInline(admin.TabularInline):
    formset = ResearchRequestInlineFormset
    model = ResearchRequestRelation

class ResearchRequestAdmin(admin.ModelAdmin):
    list_display = ('question', 'nr', 'title', 'open', 'date_added',)
    list_filter = ('open',)
    search_fields = ['title',]
    save_on_top = True
    inlines = [
        ResearchRequestRelationInline,
    ]
    
    def question(self, obj):
        return obj.get_related_question()
    question.short_description = _('Question')


class CommentRelationInline(admin.TabularInline):
    model = CommentRelation


class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'published', 'published_by', 'date_added',)
    list_filter = ('published','published_by',)
    search_fields = ['username', 'comment',]
    save_on_top = True
    exclude = ('activation_hash',)
    inlines = [
        CommentRelationInline,
    ]

class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'content_object', 'content_type', 'object_id', 'date')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(SiteConfig, SiteConfigAdmin)
admin.site.register(SiteCategory, SiteCategoryAdmin)
admin.site.register(ParticipantType, ParticipantTypeAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(ProjectPart, ProjectPartAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(ProjectGoalGroup, ProjectGoalGroupAdmin)
admin.site.register(Document, DocumentAdmin)
#admin.site.register(SearchTagCacheEntry, SearchTagCacheEntryAdmin)
#admin.site.register(Page, PageAdmin)
admin.site.register(ResearchRequest, ResearchRequestAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ActivityLog, ActivityLogAdmin)
