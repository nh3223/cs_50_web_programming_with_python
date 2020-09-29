from django.urls import path

from . import views

app_name = 'encyclopedia'

urlpatterns = [
    path('', views.index, name='index'),
    path('wiki/<str:title>', views.entry, name='entry'),
    path('search', views.search, name='search'),
    path('new_page', views.new_page, name='new_page'),
    path('wiki/edit/<str:title>', views.edit, name='edit'),
    path('random_page', views.random_page, name='random_page')
]
