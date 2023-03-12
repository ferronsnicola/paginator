from django import forms


class DeckForm(forms.Form):
    name = forms.CharField(label='Card group name')
    fronts = forms.FileField(label='Select the folder with front files', widget=forms.ClearableFileInput(attrs={'multiple': True, 'webkitdirectory': True, 'directory': True}))
    back = forms.FileField(label='Select a back file')

