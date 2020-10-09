from django.urls import path, re_path

from . import views

app_name = 'qa_program'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:kind>/<int:no>/',views.detail, name='detail'),
    path('<int:qid>/', views.detail_direct, name='detail_direct'),
]