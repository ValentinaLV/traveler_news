from django import forms
from django.core.exceptions import ValidationError
from pagedown.widgets import PagedownWidget

from .models import Post, Comment


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget)

    class Meta:
        model = Post
        fields = ['title', 'content']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post Title'})
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')
        return new_slug


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control mt-2 mb-2',
                                             'placeholder': 'Type your comment here...',
                                             'required': 'required'})}
