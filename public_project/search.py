import re
from django.db.models import Q
from public_project.models import Page


#PublicDocs
def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 


#PublicDocs
def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    #terms = normalize_query(query_string)
    for term in [query_string]: # Using complete query string instead of separated terms
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def search_for_documents(query_string):
    entry_query = get_query(query_string, ['document__title', 'content',])
    found_pages = Page.objects.select_related().filter(entry_query).order_by('document','number')
        
    document_list = []
    for page in found_pages:
        if page.document not in document_list:
            page.document.search_tags = [query_string,]
            document_list.append(page.document)
    
    return document_list
     