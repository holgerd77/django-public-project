from django import forms
from django.utils.translation import ugettext_lazy as _
    

class CommentForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    comment = forms.CharField(max_length=800)
    feedback_allowed = forms.BooleanField(required=False)
    co1_id = forms.IntegerField()
    co1_content_type = forms.CharField()
    co1_page = forms.IntegerField(required=False)
    