from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('login', views.login, name='login'),
	path('logout', views.logout, name='logout'),
	path('raports_maker', views.raports_maker, name='raports_maker'),
	path('raports_view', views.raports_view, name='raports_view'),
	path('raports_edit/<int:raport_id>', views.raports_edit, name='raports_edit')
]
