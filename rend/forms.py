from django import forms
from .models import Profile, Project
from django.contrib.auth.models import User
from .models import Comments

class VoteForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['profile','design','userbility','content']

class SignUpForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['bio','profile_pic','profile_avatar','date']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('comment_post',)

class PostForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['link','description','profile','image','title']

