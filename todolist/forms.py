from django import forms
from todolist.models import TodoList


class JobForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ['title']
        widgets = {
            'text': forms.TextInput(
                attrs={'id': 'post-text', 'required': True, 'placeholder': 'Add new job...'}
            ),
        }
