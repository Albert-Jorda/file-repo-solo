from repo.models import File, Folder
from django import forms

class FileUploadForm(forms.ModelForm):
    def __init__(self, owner, *args, **kwargs):
        super(FileUploadForm, self).__init__(*args, **kwargs)
        self.fields['folder'].queryset = Folder.objects.filter(owner=owner)

    class Meta:
        model = File
        fields = [
            'folder',
            'file'
        ]