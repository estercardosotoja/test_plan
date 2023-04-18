from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()



class Forms_Checkbox(forms.Form):
    def __init__(self, options, *args, **kwargs):
        super(Forms_Checkbox, self).__init__(*args, **kwargs)
        for i, option in enumerate(options):
            self.fields['option_{}'.format(i)] = forms.BooleanField(label=option, required=False)
