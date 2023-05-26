from django import forms


class DeckForm(forms.Form):
    # LOAD
    name = forms.CharField(label='Card group name', required=False)
    fronts = forms.FileField(label='Select the folder with front files', widget=forms.ClearableFileInput(attrs={'multiple': True, 'webkitdirectory': True, 'directory': True}), required=False)
    back = forms.FileField(label='Select a back file', required=False)


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
        ('7 Wonders', '7 Wonders'),
        ('57.5x89', '57.5x89'),
        ('56x87', '56x87'),
        ('manual', 'manual')
    )
    plotter_formats = forms.ChoiceField(label='Plotter Format', choices=pf, required=False)
    cards_formats = forms.ChoiceField(label='Cards Format', choices=cf, required=False)
    
    # these must be shown only if manual choice is selected
    plotter_height = forms.IntegerField(widget=forms.NumberInput, required=False, min_value=1)
    plotter_width = forms.IntegerField(widget=forms.NumberInput, required=False, min_value=1)
    cards_height = forms.IntegerField(widget=forms.NumberInput, required=False, min_value=1)
    cards_width = forms.IntegerField(widget=forms.NumberInput, required=False, min_value=1)
    
    padding = forms.IntegerField(widget=forms.NumberInput, required=False, min_value=0)
    ums = (
        ('mm', 'mm'),
        ('inches', 'inches')
    )
    unit_of_measurement = forms.ChoiceField(label='Unit of Measurement', choices=ums, required=False)

    cut_lines = forms.BooleanField(required=False)
    overlay_cut_cross = forms.BooleanField(required=False)
    frame_lines = forms.BooleanField(required=False)
