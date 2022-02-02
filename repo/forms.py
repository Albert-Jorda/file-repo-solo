from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from repo.models import File, Folder
from django import forms


class FolderRenameForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name']


class FileRenameForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name']


class FileUploadForm(forms.ModelForm):
    def __init__(self, owner, *args, **kwargs):
        super(FileUploadForm, self).__init__(*args, **kwargs)
        self.fields['folder'].queryset = Folder.objects.filter(owner=owner)

    class Meta:
        model = File
        fields = ['folder', 'file']


class FileUploadToFolderForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']


class FolderCreationForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name']


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='Required', required=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']


class ChangePassWordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_new_password = forms.CharField(widget=forms.PasswordInput)


class ChangeUsernameForm(forms.Form):
    new_username = forms.CharField()
    # ask password for confirmation
    password = forms.CharField(widget=forms.PasswordInput)


class ChangeEmailForm(forms.Form):
    new_email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class ChangeImageForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['image']