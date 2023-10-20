
from django import forms

operations = [
    ('merge',"merge pdf"),
    ('extract',"pdf to text"),
    ('pdfjpg',"pdf to jpg"),
    ('imagepdf',"image to pdf"),
    ('compress',"compress pdf"),
]

class uploadFileForms(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple':True}))
    operations = forms.CharField(label='Select Operation', widget=forms.Select(choices=operations))
