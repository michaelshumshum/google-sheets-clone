from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
import csv
import pandas
import math
import plotly
from io import BytesIO
from base64 import b64encode

from .forms import FileUploadForm, FileList, DataForm
from .models import File

pandas.options.plotting.backend = 'plotly'

_VIEWS = {}
_TEMPLATES = {}
for file in os.listdir('views'):
    with open(f'views/{file}', 'r') as f:
        _VIEWS[file.split('.')[0]] = f.read()
for file in os.listdir('templates'):
    with open(f'templates/{file}', 'r') as f:
        _TEMPLATES[file.split('.')[0]] = f.read()


def select_files(request):
    return redirect('upload_files')


def upload_files(request):
    msg = 'Upload your file here.'
    if request.method == 'POST':
        if 'file' in request.FILES.keys():
            form = FileUploadForm(request.POST, request.FILES)
            if request.FILES['file'].content_type != 'text/csv':
                msg = 'File is not CSV.'
            elif request.FILES['file'].name in [file.name for file in File.objects.all()]:
                msg = f'"{request.FILES["file"].name}" already exists.'
            elif form.is_valid():
                dataframe = pandas.read_csv(request.FILES['file'].file)
                f = File(name=request.FILES['file'].name, dataframe=dataframe)
                f.save()
                return redirect(f'main/{f.id}/')
            else:
                msg = 'File is invalid.'
        else:
            form = FileList(File)(request.POST)
            if form.is_valid():
                file_name = form.cleaned_data.get('radio')
                for file in File.objects.all():
                    if file.name == file_name:
                        return redirect(f'main/{file.id}/')
            else:
                msg = 'Something went wrong.'

    form1 = FileUploadForm()
    form2 = FileList(File)

    context = {
        'msg': msg,
        'form1': form1,
        'form2': form2,
    }
    return render(request, 'upload.html', context)


def raw_data(request, id):
    file = File.objects.get(id=id)
    context = {
        'data': file.dataframe.to_html(index=False)
    }
    return render(request, 'raw.html', context)


def index(request, id):
    def sigfig(x, n): return round(x, -int(math.floor(math.log10(x))) + (n - 1))

    def apply_params(params, dataframe):
        if params['sort_dropdown']:
            ascending = params['sort_ascending'] == 'on'
            params['sort_ascending'] = ascending
            dataframe.sort_values(params['sort_dropdown'], ascending=ascending, inplace=True)

    def get_summary(dataframe):
        summary = []
        for index, column in enumerate(dataframe.columns):
            d = {
                'name': column,
                'number of valid entries': dataframe[column].count(),
                'mode': list(dataframe[column].mode())[0]
            }
            if dataframe.dtypes[index] == object:
                d['choices'] = set(dataframe[column])
            else:
                d['average'] = sigfig(dataframe[column].mean(), 3)
                try:
                    d['stdev'] = sigfig(dataframe[column].std(), 3)
                except:
                    pass
                d['quartiles'] = list(dataframe[column].quantile([0, 0.25, 0.5, 0.75, 1]))

            summary.append(d)
        return summary

    def draw_graph(dataframe, x, y):  # returns HTML div
        fig = dataframe.plot(x=x, y=y, kind='scatter')
        return plotly.offline.plot(fig, auto_open=False, output_type="div")
    params = {
        'sort_dropdown': None,
        'sort_ascending': None,
        'graph_x_dropdown': None,
        'graph_y_dropdown': None
    }
    file = File.objects.get(id=id)
    for p in params:
        params[p] = request.GET.get(p)
    dataframe = file.dataframe.copy()
    apply_params(params, dataframe)
    summary = get_summary(dataframe)
    if params['graph_x_dropdown'] and params['graph_y_dropdown']:
        graph = draw_graph(dataframe, params['graph_x_dropdown'], params['graph_y_dropdown'])
    else:
        graph = None
    context = {
        'data_summary': summary,
        'form': DataForm(file.dataframe, params),
        'dataframe_html': dataframe.to_html(index=False),
        'graph': graph
    }
    return render(request, 'index.html', context)
