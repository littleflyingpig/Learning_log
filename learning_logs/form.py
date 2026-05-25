from django import forms
from .models import Topic, Entry

class FormTopic(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': '主题'}

class FormEntry(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': '内容'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
