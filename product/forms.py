from django import forms
from core.models import Comment


class CommentToManagerForm(forms.ModelForm):
    """
    Class for handel the user comment to Manager.
    """

    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {'body': forms.Textarea(attrs={'class': 'form-control'})}


class CommentReplyForm(forms.ModelForm):
    """
    Class for handel the user comment to Manager.
    """

    class Meta:
        model = Comment
        fields = ('content',)
        widget = forms.Textarea(attrs={'class': 'form-control'})
