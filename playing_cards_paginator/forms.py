from django import forms


class DeckForm(forms.Form):
    # LOAD
    name = forms.CharField(label='Card group name')
    fronts = forms.FileField(label='Select the folder with front files', widget=forms.ClearableFileInput(attrs={'multiple': True, 'webkitdirectory': True, 'directory': True}))
    back = forms.FileField(label='Select a back file')


    # DOWNLOAD 
    pf = (
        ('A4', 'A4'),
        ('A3', 'A3'),
        ('A2', 'A2'),
        ('A1', 'A1'),
        ('A0', 'A0'),
        ('junior-legal', 'junior-legal'),
        ('letter', 'letter'),
        ('legal', 'legal'),
        ('tabloid', 'tabloid'),
        ('manual', 'manual')
    )
    cf = (
        ('Magic-Pokemon', 'Magic-Pokemon'),
        ('Yu-gi-oh!', 'Yu-gi-oh!'),
        ('7 Wonder', '7 Wonder'),
        ('57.5x89', '57.5x89'),
        ('56x87', '56x87'),
        ('manual', 'manual')
    )
    plotter_formats = forms.ChoiceField(label='Plotter Format', choices=pf)
    cards_formats = forms.ChoiceField(label='Cards Format', choices=cf)
    
    # these must be shown only if manual choice is selected
    plotter_height = forms.IntegerField(widget=forms.NumberInput)
    plotter_width = forms.IntegerField(widget=forms.NumberInput)
    cards_height = forms.IntegerField(widget=forms.NumberInput)
    cards_width = forms.IntegerField(widget=forms.NumberInput)
    
    padding = forms.IntegerField(widget=forms.NumberInput)
    ums = (
        ('mm', 'mm'),
        ('inches', 'inches')
    )
    unit_of_measurement = forms.ChoiceField(label='Unit of Measurement', choices=ums)

    cut_lines = forms.BooleanField()
    frame_lines = forms.BooleanField()
