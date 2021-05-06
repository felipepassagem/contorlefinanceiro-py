from django.urls import path

from . import views

urlpatterns = [
    #path('data', views.get_data, name='data'),
    path('', views.index, name='index'),
    path('add', views.add, name='add'),
    path('edit', views.edit, name='edit')
]
