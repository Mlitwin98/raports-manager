from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('login', views.login, name='login'),
	path('logout', views.logout, name='logout'),
	path('raports_maker', views.raports_maker, name='raports_maker'),
	path('raports_view', views.raports_view, name='raports_view'),
	path('to_do_list', views.to_do_list, name='to_do_list'),
	path('delete_task/<int:taskID>', views.delete_task, name='delete_task'),
	path('edit_task/<int:taskID>', views.edit_task, name='edit_task'),
	path('raports_edit/<int:raport_id>', views.raports_edit, name='raports_edit')
]
