# coding=UTF-8
import json, math, os, urllib, urllib2

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db.models import Count
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.html import strip_tags
from django.utils.translation import ugettext as _
from public_project.forms import *
from public_project.models import *
from public_project.search import get_query, search_for_documents


def get_research_request(request):
    if 'research_request_id' in request.GET:
        try:
            research_request = ResearchRequest.objects.get(pk=request.GET['research_request_id'])
            return [research_request,]
        except ResearchRequest.DoesNotExist:
            pass
    return None


def get_user_comment(request):
    if 'comment_id' in request.GET:
        try:
            comment = Comment.objects.get(pk=request.GET['comment_id'])
            return [comment,]
        except Comment.DoesNotExist:
            pass
    return None
    

def validate_research_request_form(request):
    
    if request.method == 'POST' and 'research_request_form' in request.POST:
        if not request.user.has_perm('public_project.can_add_research_request'):
            return "FAILED"
        rr = ResearchRequest()
        rr.nr = request.POST['nr']
        rr.title = request.POST['title']
        rr.description = request.POST['description']
        rr.save()
            
        co1_content_type = ContentType.objects.get(app_label="public_project", model=request.POST['co1_content_type'])
        co1 = co1_content_type.get_object_for_this_type(id=request.POST['co1_id'])
        rr_rel = ResearchRequestRelation()
        rr_rel.research_request = rr
        rr_rel.content_object = co1
        if(request.POST['co1_content_type'] == 'document'):
            rr_rel.page = request.POST['co1_page']
        rr_rel.save()
            
        counter_more_cos = int(request.POST['counter_more_cos'])
            
        for num_id in range(2, counter_more_cos + 2):
            if 'co' + str(num_id) + '_id' in request.POST:
                co_content_type = ContentType.objects.get(app_label="public_project", model=request.POST['co' + str(num_id) + '_content_type'])
                co = co_content_type.get_object_for_this_type(id=request.POST['co' + str(num_id) + '_id'])
                rr_rel = ResearchRequestRelation()
                rr_rel.research_request = rr
                rr_rel.content_object = co
                if(request.POST['co' + str(num_id) + '_content_type'] == 'document'):
                    rr_rel.page = request.POST['co' + str(num_id) + '_page']
                rr_rel.save()        
        return "SENT"
    
    return ""


def validate_comment_form(request):
    
    if request.method == 'POST' and 'comment_form' in request.POST:
        print request.POST
        form = CommentForm(request.POST)
        if form.is_valid():
            c = Comment()
            c.username = form.cleaned_data['username']
            c.email = form.cleaned_data['email']
            c.comment = form.cleaned_data['comment']
            c.feedback_allowed = form.cleaned_data['feedback_allowed']
            c.activation_hash = os.urandom(16).encode('hex')
            c.save()
            
            co1_content_type = ContentType.objects.get(app_label="public_project", model=form.cleaned_data['co1_content_type'])
            co1 = co1_content_type.get_object_for_this_type(id=form.cleaned_data['co1_id'])
            cr = CommentRelation()
            cr.comment = c
            cr.content_object = co1
            if(form.cleaned_data['co1_content_type'] == 'document'):
                cr.page = form.cleaned_data['co1_page']
            cr.save()
            
            counter_more_cos = int(request.POST['counter_more_cos'])
            
            for num_id in range(2, counter_more_cos + 2):
                if 'co' + str(num_id) + '_id' in request.POST:
                    co_content_type = ContentType.objects.get(app_label="public_project", model=request.POST['co' + str(num_id) + '_content_type'])
                    co = co_content_type.get_object_for_this_type(id=request.POST['co' + str(num_id) + '_id'])
                    cr = CommentRelation()
                    cr.comment = c
                    cr.content_object = co
                    if(request.POST['co' + str(num_id) + '_content_type'] == 'document'):
                        cr.page = request.POST['co' + str(num_id) + '_page']
                    cr.save()
            
            email_users = User.objects.filter(userprofile__receive_new_comment_emails=True)
            
            #try:
            for i in range(0,1):
                for user in email_users:
                    sep = "-----------------------------------------------------------\n"
                    subject = _("NEW_COMMENT_EMAIL_SUBJECT") + ': ' + unicode(c)
                    
                    msg  = _("NEW_COMMENT_EMAIL_MESSAGE") + "\n"
                    msg += 'http://%s%s' % (Site.objects.get_current().domain, c.get_absolute_url()) + "\n\n"
                    msg += sep
                    msg += _("Name") + ": " + unicode(c.username) + "\n"
                    msg += _("E-Mail") + ": " + unicode(c.email) + "\n"
                    if c.feedback_allowed:
                        fa_str = _("yes")
                    else:
                        fa_str = _("no")
                    msg += _("Questions via mail allowed") + ": " + fa_str + "\n"
                    msg += _("Comment") + ":\n"
                    msg += c.comment + "\n" + sep
                    
                    msg += _("Comment on") + ":" + "\n"
                    for cr in c.commentrelation_set.all():
                        msg += unicode(cr.content_object) + "\n"
                        msg += 'http://%s%s' % (Site.objects.get_current().domain, cr.content_object.get_absolute_url()) + "\n"
                    
                    msg += "\n"
                    
                    if user.has_perm('public_project.change_comment') and user.email:
                        msg += _("NEW_COMMENT_EMAIL_MESSAGE_ACTIVATION") + "\n"
                        msg += 'http://%s/%s?activation_hash=%s&user=%s' \
                            % (Site.objects.get_current().domain, _("activate_comment_url"), c.activation_hash, urllib.quote_plus(unicode(user))) + "\n"
                    
                    send_mail(subject, msg, settings.EMAIL_FROM, [user.email], fail_silently=False)
            #except AttributeError:
            #    pass
            
            return "SENT"
        else:
            print form.errors
            return "FAILED"
    return ""


def merge_with_search_tag_docs(document_list, object):
    for tag in object.search_tags.all():
        search_docs = search_for_documents(tag.name)
        for doc in search_docs:
            if doc in document_list:
                index = document_list.index(doc)
                if not hasattr(document_list[index], 'search_tags'):
                    document_list[index].search_tags = []
                document_list[index].search_tags.append(tag.name)
            else:
                document_list.append(doc)
    document_list.sort(key=lambda x:x.title)
    return document_list


def index(request):
    research_request_list = ResearchRequest.objects.all()
    comment_list = Comment.objects.filter(published=True)
    
    if Event.objects.count() > 0:
        latest_event = Event.objects.all()[0]
    else:
        latest_event = None
    if Document.objects.count() > 0:
        latest_document = Document.objects.all()[0]
    else:
        latest_document = None 
    
    context = RequestContext(request, {
        'site_config': SiteConfig.objects.get_site_config(request),
        'site_category': SiteCategory.objects.get_or_create(category='home')[0],
        'current_project_goal_group': ProjectGoalGroup.objects.get_current(),
        'project_part_list': ProjectPart.objects.all(),
        'latest_event': latest_event,
        'latest_document': latest_document,
        'activity_list': ActivityLog.objects.all()[0:5],
        'research_request_list': research_request_list[0:3],
        'num_total_research_requests': len(research_request_list),
        'comment_list': comment_list[0:1],
        'num_total_comments': len(comment_list),
    })
    return render_to_response('index.html', context)


def project_parts(request):
    site_category = SiteCategory.objects.get_or_create(category='project_parts')[0]
    
    main_project_parts = ProjectPart.objects.annotate(count=Count('main_project_parts')).filter(count=0)
    only_mpps = len(main_project_parts) == ProjectPart.objects.count()
    middle = int(math.floor(float(len(main_project_parts))/float(2)))
    
    if len(main_project_parts) >= 4:
        middle -= 2
    
    context = RequestContext(request, {
        'site_config': SiteConfig.objects.get_site_config(request),
        'site_category': site_category,
        'only_mpps': only_mpps,
        'main_project_part_list_left': main_project_parts[0:middle],
        'main_project_part_list_right': main_project_parts[middle:],
    })
    return render_to_response('project_parts.html', context)


def project_part(request, project_part_id):
    project_part = get_object_or_404(ProjectPart, pk=project_part_id)
    
    comment_form_status = validate_comment_form(request)
    
    content_type = ContentType.objects.get(app_label="public_project", model="projectpart")
    comment_list = Comment.objects.filter(commentrelation__content_type=content_type).filter(commentrelation__object_id=project_part.id).filter(published=True).distinct()
    
    context = RequestContext(request, {
        'site_config': SiteConfig.objects.get_site_config(request),
        'site_category': SiteCategory.objects.get_or_create(category='project_parts')[0],
        'user_comment': get_user_comment(request),
        'project_part': project_part,
        'question_list': project_part.get_questions(),
        'event_list': project_part.get_events(),
        'document_list': project_part.get_documents(),
        'content_document_list': merge_with_search_tag_docs([], project_part),
        'comment_form_status': comment_form_status,
        'comment_list': comment_list[0:3],
        'num_total_comments': len(comment_list),
    })
    return render_to_response('project_part.html', context)


def goals(request):
    
    all_main_project_parts = ProjectPart.objects.annotate(count=Count('main_project_parts')).filter(count=0)
    main_project_parts = []
    for main_pp in all_main_project_parts:
        if main_pp.projectgoalgroup_set.count() > 0:
            main_project_parts.append(main_pp)
    middle = int(math.floor(float(len(main_project_parts))/float(2)))
    
    context = RequestContext(request, {
        'site_config': SiteConfig.objects.get_site_config(request),
        'site_category': SiteCategory.objects.get_or_create(category='goals')[0],
        'common_goal_group_list': ProjectGoalGroup.objects.filter(project_part=None).order_by('event'),
        'main_project_part_list_left': main_project_parts[0:middle],
        'main_project_part_list_right': main_project_parts[middle:],
    })
    return render_to_response('goals.html', context)


def questions(request):
    all_mpps = ProjectPart.objects.annotate(count=Count('main_project_parts')).filter(count=0)
    main_project_parts = []
    for mpp in all_mpps:
        if mpp.get_num_questions() > 0:
            main_project_parts.append(mpp)
    middle = int(math.floor(float(len(main_project_parts))/float(2)))
    
    research_request_list = ResearchRequest.objects.all()
    
    context = RequestContext(request, {
        'site_config': SiteConfig.objects.get_site_config(request),
        'site_category': SiteCategory.objects.get_or_create(category='questions')[0],
        'main_project_part_list_left': main_project_parts[0:middle],
        'main_project_part_list_right': main_project_parts[middle:],
        'research_request_list': research_request_list[0:3],
        'num_total_research_requests': len(research_request_list),
    })
    return render_to_response('questions.html', context)


def question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    research_request_form_status = validate_research_request_form(request)
    content_type = ContentType.objects.get(app_label="public_project", model="question")
    research_request_list = ResearchRequest.objects.filter(researchrequestrelation__content_type=content_type).filter(researchrequestrelation__object_id=question.id).distinct()
    
    comment_form_status = validate_comment_form(request)
    content_type = ContentType.objects.get(app_label="public_project", model="question")
    comment_list = Comment.objects.filter(commentrelation__content_type=content_type).filter(commentrelation__object_id=question.id).filter(published=True).distinct()
    
    context = RequestContext(request, {
        'site_config': SiteConfig.objects.get_site_config(request),
        'site_category': SiteCategory.objects.get_or_create(category='questions')[0],
        'user_comment': get_user_comment(request),
        'research_request': get_research_request(request),
        'question': question,
        'document_list': question.documents.all(),
        'research_request_form_status': research_request_form_status,
        'research_request_list': research_request_list[0:3],
        'num_total_research_requests': len(research_request_list),
        'comment_form_status': comment_form_status,
        'comment_list': comment_list[0:3],
        'num_total_comments': len(comment_list),
    })
    return render_to_response('question.html', context)


def participants(request):
    site_category = SiteCategory.objects.get_or_create(category='participants')[0]
    participant_types = ParticipantType.objects.all()
    middle = int(math.floor(float(len(participant_types))/float(2)))
    
    if len(participant_types) >= 4:
        middle -= 2
    
    context = RequestContext(request, {
        'site_config': SiteConfig.objects.get_site_config(request),
        'site_category': site_category,
        'common_participant_list': Participant.objects.filter(belongs_to=None).filter(type=None),
        'participant_type_list_left': participant_types[0:middle],
        'participant_type_list_right': participant_types[middle:],
    })
    return render_to_response('participants.html', context)


def participant(request, participant_id):
    participant = get_object_or_404(Participant, pk=participant_id)
    
    comment_form_status = validate_comment_form(request)
    content_type = ContentType.objects.get(app_label="public_project", model="participant")
    comment_list = Comment.objects.filter(commentrelation__content_type=content_type).filter(commentrelation__object_id=participant.id).filter(published=True).distinct()
    
    context = RequestContext(request, {
        'site_config': SiteConfig.objects.get_site_config(request),
        'site_category': SiteCategory.objects.get_or_create(category='participants')[0],
        'user_comment': get_user_comment(request),
        'participant': participant,
        'question_list': participant.get_questions(),
        'event_list': participant.get_events(),
        'document_list': participant.get_documents(),
        'content_document_list': merge_with_search_tag_docs([], participant),
        'comment_form_status': comment_form_status,
        'comment_list': comment_list[0:3],
        'num_total_comments': len(comment_list),
    })
    return render_to_response('participant.html', context)


def events(request):
    site_category = SiteCategory.objects.get_or_create(category='events')[0]
    
    all_mpps = ProjectPart.objects.annotate(count=Count('main_project_parts')).filter(count=0)
    main_project_parts = []
    for mpp in all_mpps:
        if mpp.get_num_events() > 0:
            main_project_parts.append(mpp)
    
    context = RequestContext(request, {
        'site_config': SiteConfig.objects.get_site_config(request),
        'site_category': SiteCategory.objects.get_or_create(category='events')[0],
        'project_goal_group_list': ProjectGoalGroup.objects.all().order_by('event'),
        'chronology_list': Event.objects.all(),
        'main_project_part_list': main_project_parts,
    })
    return render_to_response('events.html', context)


def event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    
    content_document_list = merge_with_search_tag_docs([], event)
    
    comment_form_status = validate_comment_form(request)
    content_type = ContentType.objects.get(app_label="public_project", model="event")
    comment_list = Comment.objects.filter(commentrelation__content_type=content_type).filter(commentrelation__object_id=event.id).filter(published=True).distinct()
    
    context = RequestContext(request, {
        'site_config': SiteConfig.objects.get_site_config(request),
        'site_category': SiteCategory.objects.get_or_create(category='events')[0],
        'user_comment': get_user_comment(request),
        'event': event,
        'document_list': event.related_documents.order_by("title"),
        'content_document_list': content_document_list,
        'comment_form_status': comment_form_status,
        'comment_list': comment_list[0:3],
        'num_total_comments': len(comment_list),
    })
    return render_to_response('event.html', context)


def web_source(request, web_source_id):
    web_source = get_object_or_404(WebSource, pk=web_source_id)
    
    req = urllib2.Request(web_source.url, headers={'User-Agent' : "Magic Browser"}) 
    response = urllib2.urlopen(req)
    html = response.read()
    
    search_tags = SearchTag.objects.all()
    found_search_tag_list = []
    for st in search_tags:
        if st.name.lower() in unicode(html, errors='replace').lower():
            found_search_tag_list.append(st)
    
    context = RequestContext(request, {
        'site_config': SiteConfig.objects.get_site_config(request),
        'web_source': web_source,
        'found_search_tag_list': found_search_tag_list,
    })
    if request.user.is_authenticated():
        return render_to_response('web_source.html', context)
    else:
        raise Http404


def documents(request):
    site_category = SiteCategory.objects.get_or_create(category='documents')[0]
    
    all_mpps = ProjectPart.objects.annotate(count=Count('main_project_parts')).filter(count=0)
    main_project_parts = []
    for mpp in all_mpps:
        if mpp.get_num_documents() > 0:
            main_project_parts.append(mpp)
    middle = int(math.floor(float(len(main_project_parts))/float(2)))
    
    if len(main_project_parts) >= 4:
        middle -= 2
    
    context = RequestContext(request, {
        'site_config': SiteConfig.objects.get_site_config(request),
        'site_category': site_category,
        'main_project_part_list_left': main_project_parts[0:middle],
        'main_project_part_list_right': main_project_parts[middle:],
    })
    return render_to_response('documents.html', context)


def xhr_universal_search(request):
    if request.method == 'GET' and 'query' in request.GET:
        query_string = request.GET['query']
        query_string = unicode(query_string).encode('utf-8')
        
        if len(query_string) >= 4:
            entry_query = get_query(query_string, ['name',])
            p_list = list(Participant.objects.select_related().filter(entry_query)[0:10])
            
            entry_query = get_query(query_string, ['name',])
            pp_list = list(ProjectPart.objects.select_related().filter(entry_query)[0:10])
            
            entry_query = get_query(query_string, ['title',])
            q_list = list(Question.objects.select_related().filter(entry_query)[0:10])
            
            entry_query = get_query(query_string, ['title',])
            e_list = list(Event.objects.select_related().filter(entry_query)[0:10])
            
            entry_query = get_query(query_string, ['title',])
            d_list = list(Document.objects.select_related().filter(entry_query)[0:10])
            
            object_list = p_list + pp_list + q_list + e_list + d_list
        else:
            object_list = []
        
        res = {
            'values': {},
            'options': [],
        }
        print query_string
        if 'with_query_search' in request.GET:
            if len(query_string) < 4:
                option = query_string
            else:
                option = '<i class="icon-search"></i> ' + query_string
            res['values'][option] = {
                'content_type': 'query_search',
                'id': 0,
                'absolute_url': '/' + _('search_url') + '?q=' + urllib.quote_plus(query_string),
            }
            res['options'].append(option)
        
        for object in object_list:
            content_type = object.__class__.__name__.lower()
            id = object.id
            
            if not 'ommit_content_type' in request.GET or not (content_type == request.GET['ommit_content_type'] and str(id) == request.GET['ommit_id']):
                option = '<i class="' + object.get_icon_class() + '"></i> ' + unicode(object)
                res['values'][option] = {
                    'content_type': content_type,
                    'id': id,
                    'absolute_url': object.get_absolute_url(),
                }
                res['options'].append(option)
        
        mimetype = 'application/javascript'
        return HttpResponse(json.dumps(res), mimetype)
    else:
        raise Http404


def xhr_document_tags(request):
    if request.method == 'POST':
        
        colors = {
            'projectpart': '#0d9434',
            'participant': '#3e3ec7',
            'event': '#c91a1a',
        }
        if request.POST['document_id']:
            document = get_object_or_404(Document, pk=request.POST['document_id'])
            if request.POST['content_type']:
                st_dict_list = SearchTagCacheEntry.objects.filter(document=document).filter(tag__content_type__model=request.POST['content_type']).values('tag__name', 'tag__content_type__model',).annotate(num_tags=Count('tag__name')).order_by('-num_tags')
                #cache_entries = SearchTagCacheEntry.objects.filter(document=document).filter(tag__content_type__model=request.POST['content_type'])
            else:
                st_dict_list = SearchTagCacheEntry.objects.filter(document=document).values('tag__name', 'tag__content_type__model',).annotate(num_tags=Count('tag__name')).order_by('-num_tags')
            st_dict_list = st_dict_list[0:16]
            size_start = 10
            size_span = 10
        else:
            if request.POST['content_type']:
                st_dict_list = SearchTagCacheEntry.objects.filter(tag__content_type__model=request.POST['content_type']).values('tag__name', 'tag__content_type__model',).annotate(num_tags=Count('tag__name')).order_by('-num_tags')[0:22]
            else:
                st_dict_list = SearchTagCacheEntry.objects.values('tag__name', 'tag__content_type__model',).annotate(num_tags=Count('tag__name')).order_by('-num_tags')[0:22]
            size_start = 12
            size_span = 12
        
        if len(st_dict_list) > 0:
            first = st_dict_list[0]
            max_num_results = first['num_tags']
        
        words = []
        for st_dict in st_dict_list:
            text = st_dict['tag__name']
            size = size_start + int(round((float(st_dict['num_tags'])/ float(max_num_results)) * size_span))
            color = colors[st_dict['tag__content_type__model']]
            
            word = { "text": text, "size":size, "color": color, }
            words.append(word)
        
        data = json.dumps(words)
        
        mimetype = 'application/javascript'
        return HttpResponse(data, mimetype)
    else:
        raise Http404


def document(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    comment_form_status = validate_comment_form(request)
    
    query_string = ''
    found_pages = []
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ['document__title', 'content',])
        found_pages = Page.objects.select_related().filter(document=document).filter(entry_query).order_by('number')
    
    content_type = ContentType.objects.get(app_label="public_project", model="document")
    tmp_comment_list = Comment.objects.filter(commentrelation__content_type=content_type).filter(commentrelation__object_id=document.id).filter(published=True).distinct()
    print len(tmp_comment_list)
    comment_list = []
    for comment in tmp_comment_list:
        print type(comment)
        cr = comment.commentrelation_set.filter(content_type=content_type, object_id=document.id)[0]
        comment.page = cr.page
        comment_list.append(comment)
    comment_list.sort(key=lambda x:x.page)
    
    context = RequestContext(request, {
        'site_config': SiteConfig.objects.get_site_config(request),
        'site_category': SiteCategory.objects.get_or_create(category='documents')[0],
        'user_comment': get_user_comment(request),
        'document': document,
        'found_pages': found_pages,
        'comment_form_status': comment_form_status,
        'comment_list': comment_list,
        'num_total_comments': len(comment_list),
        'query_string': query_string,
    })
    return render_to_response('document.html', context)


def search(request):
    
    if ('q' in request.GET) and request.GET['q'].strip():
        
        query_string = request.GET['q']
        
        entry_query = get_query(query_string, ['name', 'description',])
        project_part_list = ProjectPart.objects.select_related().filter(entry_query)
        
        entry_query = get_query(query_string, ['title', 'description',])
        question_list = Question.objects.select_related().filter(entry_query)
        
        entry_query = get_query(query_string, ['name', 'description',])
        participant_list = Participant.objects.select_related().filter(entry_query)
        
        entry_query = get_query(query_string, ['title', 'description',])
        event_list = Event.objects.select_related().filter(entry_query)
        
        document_list = search_for_documents(query_string)
        
        context = RequestContext(request, {
            'site_config': SiteConfig.objects.get_site_config(request),
            'query': query_string,
            'project_part_list': project_part_list,
            'question_list': question_list,
            'participant_list': participant_list,
            'event_list': event_list,
            'document_list': document_list,
            'q': query_string,
        })
        
        return render_to_response('search.html', context)
    else:
        return HttpResponse("An Error occured!")


def research_requests(request, object_id, content_type):
    
    if not content_type:
        object = None
        research_request_list = ResearchRequest.objects.all()
    
    if content_type == 'question':
        object = get_object_or_404(Question, pk=object_id)
        content_type = ContentType.objects.get(app_label="public_project", model="question")
        research_request_list = ResearchRequest.objects.filter(researchrequestrelation__content_type=content_type).filter(researchrequestrelation__object_id=object.id).distinct()
    
    ph_title = unicode(object)
    
    context = RequestContext(request, {
        'site_config': SiteConfig.objects.get_site_config(request),
        'rr_object': object,
        'research_request_list': research_request_list,
        'num_total_research_requests': len(research_request_list),
        'content_type': content_type,
        'ph_title': ph_title,    
    })    
    
    return render_to_response('research_requests.html', context)


def comments(request, object_id, content_type):
    
    if not content_type:
        object = None
        comment_list = Comment.objects.filter(published=True)
    
    if content_type == 'project_part':
        object = get_object_or_404(ProjectPart, pk=object_id)
        content_type = ContentType.objects.get(app_label="public_project", model="projectpart")
        comment_list = Comment.objects.filter(commentrelation__content_type=content_type).filter(commentrelation__object_id=object.id).filter(published=True).distinct()
    if content_type == 'question':
        object = get_object_or_404(Question, pk=object_id)
        content_type = ContentType.objects.get(app_label="public_project", model="question")
        comment_list = Comment.objects.filter(commentrelation__content_type=content_type).filter(commentrelation__object_id=object.id).filter(published=True).distinct()
    if content_type == 'participant':
        object = get_object_or_404(Participant, pk=object_id)
        content_type = ContentType.objects.get(app_label="public_project", model="participant")
        comment_list = Comment.objects.filter(commentrelation__content_type=content_type).filter(commentrelation__object_id=object.id).filter(published=True).distinct()
    if content_type == 'event':
        object = get_object_or_404(Event, pk=object_id)
        content_type = ContentType.objects.get(app_label="public_project", model="event")
        comment_list = Comment.objects.filter(commentrelation__content_type=content_type).filter(commentrelation__object_id=object.id).filter(published=True).distinct()
    if content_type == 'document':
        object = get_object_or_404(Document, pk=object_id)
        content_type = ContentType.objects.get(app_label="public_project", model="document")
        comment_list = Comment.objects.filter(commentrelation__content_type=content_type).filter(commentrelation__object_id=object.id).filter(published=True).distinct()
    
    ph_title = unicode(object)
    
    context = RequestContext(request, {
        'site_config': SiteConfig.objects.get_site_config(request),
        'commented_object': object,
        'comment_list': comment_list,
        'num_total_comments': len(comment_list),
        'content_type': content_type,
        'ph_title': ph_title,    
    })    
    
    return render_to_response('comments.html', context)


def api(request):
    context = RequestContext(request, {
        'site_config': SiteConfig.objects.get_site_config(request),
    })
    return render_to_response('api.html', context)


def contact(request):
    image_list = Image.objects.all()
    
    context = RequestContext(request, {
        'site_config': SiteConfig.objects.get_site_config(request),
        'image_list': image_list,
    })
    return render_to_response('contact.html', context)


def activate_comment(request):
    c = get_object_or_404(Comment, activation_hash=request.GET['activation_hash'])
    site_config = SiteConfig.objects.get_site_config(request)
    
    res  = '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body>'
    res += '<div style="margin:20px;padding:20px;border:1px solid #999;float:left;color:#333;font-size:14px;'
    res += 'font-family:arial, helvetica, sans-serif;">'
    
    if not c.published:
        c.published = True
        c.published_by = request.GET['user']
        c.save()
        res += _("The following comment was activated for publication on website:") + '<br><br>'
        res += unicode(c)
        
        #User mail
        subject = _("Your comment on %s was published") % site_config.short_title
                    
        msg  = _("Hello %s,") % c.username + "\n\n"
        msg += _("thank you for your comment, which you can find under the following url:") + "\n"
        msg += 'http://%s%s' % (Site.objects.get_current().domain, c.get_absolute_url()) + "\n\n"
        
        msg += _("You can use the url above to tell others about your comment.") + "\n\n"
        
        msg += _("If you want to share your comment on a social network,") + "\n"
        msg += _("you can use the following share urls as a staring point:") + "\n\n"
        
        msg += "Twitter:\n" + c.get_twitter_url() + "\n\n"
        msg += "Facebook:\n" + c.get_facebook_url() + "\n\n"
        msg += "Google+:\n" + c.get_google_plus_url() + "\n\n"
        msg += "App.net:\n" + c.get_app_net_url() + "\n\n\n"
        
        msg += _("Greetings") + "\n\n"
        msg += _("Your %s team") % site_config.short_title + "\n"

        send_mail(subject, msg, settings.EMAIL_FROM, [c.email,], fail_silently=False)
        
        al = ActivityLog()
        al.content_object = c
        al.type = 'NC'
        al.save()
        
    else:
        res += _("Comment already activated by user %s.") % (c.published_by)
    
    res += '</div></body></html>'
    
    return HttpResponse(res)


def custom_404_view(request):
    context = RequestContext(request, {
        'site_config': SiteConfig.objects.get_site_config(request),
    })
    return render_to_response('404.html', context)
    
    