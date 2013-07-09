from public_project.models import Document, Page, SearchTag, SearchTagCacheEntry
from public_project.search import get_query



def create_cache_entry(tag, document):
    entry_query = get_query(tag.name, ['document__title', 'content',])
    num_results = Page.objects.select_related().filter(document=document).filter(entry_query).count()
    
    if num_results > 0:
        ce = SearchTagCacheEntry()
        if SearchTagCacheEntry.objects.filter(document=document).filter(tag__name=tag.name).count() == 0 and \
           SearchTagCacheEntry.objects.filter(document=document).filter(tag__name=tag.name.title()).count() == 0 and \
           SearchTagCacheEntry.objects.filter(document=document).filter(tag__name=tag.name.upper()).count() == 0:
            ce.tag = tag
            ce.document = document
            ce.num_results = num_results
            ce.save()


def rebuild_cache_for_tag(tag):
    tag.searchtagcacheentry_set.all().delete()
    docs = Document.objects.all()
    for doc in docs:
        create_cache_entry(tag, doc)

def rebuild_cache_for_object(object):
    for tag in object.search_tags.all():
        rebuild_cache_for_tag(tag)


def rebuild_cache_for_document(document):
    SearchTagCacheEntry.objects.filter(document=document).delete()
    
    for tag in SearchTag.objects.all():
        create_cache_entry(tag, document)




















