from django import forms
from django.core.validators import MaxLengthValidator

from core.models import Comment


class CommentToManagerForm(forms.ModelForm):
    """
    Class for handel the user comment to Manager.
    """

    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {'content': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 630px;'})}
        validators = [MaxLengthValidator(limit_value=1000)]


class CommentReplyForm(forms.ModelForm):
    """
    Class for handel the user comment to Manager.
    """

    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {'content': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 500px;'})}
        validators = [MaxLengthValidator(limit_value=1000)]


class ProductSearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'search for product',
                                                           'style': 'width: 350px;height:45px;'},))
