# coding: utf-8

from django.conf.urls import url
from django.contrib import admin

from main.views import AddView, ShowView, SomeDeleteView, EditView, SomeListView, SomeDetailView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$',  # Главная страница
        # HomeView.as_view(),
        SomeListView.as_view(),  # Пример ListView
        name='home'),

    url(r'^add/$',
        AddView.as_view(),  # Добавить
        name='add'),

    url(r'^edit/(?P<pk>\d+)/$',
        EditView.as_view(),  # Редакитировать
        name='edit'),

    url(r'^delete/(?P<pk>\d+)/$',
        SomeDeleteView.as_view(),  # Удалить
        name='delete'),

    url(r'^show/$',
        ShowView.as_view(),  # Просмотр
        name='show'),

    url(r'^detail/(?P<pk>\d+)/$',  # Пример DetailView
        SomeDetailView.as_view(),
        name='detail'),
]
