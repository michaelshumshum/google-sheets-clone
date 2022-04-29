from django.urls import path, re_path


from . import views

urlpatterns = [
    re_path(r'^main\/(\d+)\/$', views.index, name='main'),
    re_path(r'^main\/(\d+)\/raw$', views.raw_data, name='main'),
    path('', views.upload_files, name='upload_files'),
]
