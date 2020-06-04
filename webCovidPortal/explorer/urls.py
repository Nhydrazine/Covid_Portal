from django.urls import path;
from explorer import views;

urlpatterns = [
    path('', views.index, name="index"),
    path('taxa', views.taxa, name="taxa"),
    path('sequencerecords', views.sequencerecords, name="sequencerecords"),
    path('sequences', views.sequences, name='sequences'),
];
