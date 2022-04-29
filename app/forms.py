from django import forms


class FileUploadForm(forms.Form):
    file = forms.FileField(label='Select a file')


def FileList(file_model):
    class FileList(forms.Form):
        choices = [(file.name, file.name) for file in file_model.objects.all()]
        radio = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)
    return FileList


def DataForm(dataframe, default):
    head = dataframe.columns

    class cls(forms.Form):
        sort_choices = [(choice, choice) for choice in head]
        sort_dropdown = forms.ChoiceField(choices=sort_choices, initial=default['sort_dropdown'])
        sort_ascending = forms.BooleanField(label='Ascending', initial=default['sort_ascending'])

        graph_x_dropdown = forms.ChoiceField(choices=sort_choices, initial=default['graph_x_dropdown'])
        graph_y_dropdown = forms.ChoiceField(choices=sort_choices, initial=default['graph_y_dropdown'])
    return cls
