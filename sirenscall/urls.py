from django.urls import path, re_path

from . import views

app_name = 'sirenscall'
urlpatterns = [
    path('', views.index, name='index'),

    path('recorder/', views.recorder_index, name='recorder_index'),
    path('recorder/<int:recorder_id>/', views.recorder_detail, name='recorder_detail'),
    path('recorder/submit', views.recorder_submit, name='recorder_submit'),
    path('recorder/check', views.recorder_pwd_check, name='recorder_pwd_check'),

    path('radar/', views.radar, name='radar'),
    path('radar/upload', views.file_upload, name='radar_upload'),
    path('radar/download_check', views.file_download_check, name='radar_download_check'),
    path('radar/download', views.blank, name='radar_blank'),
    path('radar/download/<str:file_id>radar<str:password>/', views.file_download, name='radar_download'),
    # re_path(r'^radar/downloadFile/(?P<file_name>.+)$', views.file_download, name='radar_downlaod'),
    # path('radar/download', views.file_download, name='radar_download'),


    path('test/', views.testpage, name='testpage'),
    path('test/submit', views.test_form, name='test_form'),
]