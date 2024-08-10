from django import forms
from .models import Post,Category,Comment



class PostCreateForm(forms.ModelForm):
    category= forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    class Meta:
        model = Post
        fields = ['title', 'post_author', 'category', 'content', 'image_file', 'audio_file']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }


 
class PostEditForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','post_author','category','content','image_file','audio_file']

        widgets = {
            'title':forms.TextInput(attrs={'class': 'form-control'}),
            'title_tag':forms.TextInput(attrs={'class': 'form-control'}),
            'content':forms.Textarea(attrs={'class': 'form-control'}),

        }
 

class FollowForm(forms.Form):
    target_profile_id = forms.IntegerField(widget=forms.HiddenInput())


class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['content','post','comment_author']
        widgets = {
            'content':forms.Textarea(attrs={'class':'form-control mb-10','placeholder':'Share your thoughts...'})
        }

