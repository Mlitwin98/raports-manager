from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from django.shortcuts import get_object_or_404
from datetime import datetime
from .models import Raport, Task


# Create your views here.
def index(request):
	if request.user.is_authenticated:
		calendar=''
		try:
			calendar = request.user.groups.get().calendar_link
		except:
			pass
		return render(request, "index.html", {'calendar':calendar})
	else:
		return redirect('login')


def login(request):
	if request.method == "POST":
		email = request.POST['email']
		password = request.POST['password']
		user = auth.authenticate(request, username=email, password=password)
		if user is not None:
			auth.login(request, user)
			return redirect('index')
		else:
			messages.info(request, 'Błędne dane logowania')
			return redirect('login')
	else:
		return render(request, 'login.html')


def logout(request):
	auth.logout(request)
	return redirect('index')


def raports_maker(request):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			if request.method == "POST":
				title = request.POST['title']
				content = request.POST['content']
				author_name = request.user.first_name
				author_lastname = request.user.last_name
				if title != '' and content != '' and not title.isspace() and not content.isspace():
					raport = Raport.create(title, content, author_name, author_lastname)
					raport.save()
					messages.info(request, 'Raport wysłany')
					return redirect('raports_maker')
				else:
					messages.info(request, 'Tytuł i treść nie mogą być puste')
					return redirect('raports_maker')
			else:
				return render(request, 'raports_maker.html')
		else:
			return redirect('index')
	else:
		return redirect('login')


def raports_view(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			search_title = request.POST['title']
			search_content = request.POST['content']
			search_name = request.POST['name']
			search_lastname = request.POST['lastname']
			search_date = request.POST['date']

			raports = Raport.objects.all()

			if search_title != '' and not search_title.isspace():
				raports = Raport.objects.filter(title__icontains=search_title)
			if search_content != '' and not search_content.isspace():
				raports = raports.filter(content__icontains=search_content)
			if search_name != '' and not search_name.isspace():
				raports = raports.filter(author_name__iexact=search_name)
			if search_lastname != '' and not search_lastname.isspace():
				raports = raports.filter(author_lastname__iexact=search_lastname)
			if search_date != '':
				dates = search_date.split(' - ')
				dateStart = datetime.strptime(dates[0], '%m/%d/%Y').replace(hour=0, minute=0)
				dateEnd = datetime.strptime(dates[1], '%m/%d/%Y').replace(hour=23, minute=59)

				raports = raports.filter(dateTime__gte=dateStart)
				raports = raports.filter(dateTime__lte=dateEnd)
			return render(request, 'raports_view.html', {"raports": raports[::-1]})
		else:
			visibleRaports = 50
			numOfRaports = Raport.objects.all().count()
			if numOfRaports < visibleRaports:
				visibleRaports = numOfRaports
			raports = Raport.objects.all()[numOfRaports-visibleRaports:numOfRaports]
			return render(request, 'raports_view.html', {"raports": raports[::-1]})
	else:
		return redirect('login')


def raports_edit(request, raport_id):
	if request.user.is_authenticated:
		raport = get_object_or_404(Raport, id=raport_id)
		if request.method == "POST":
			if 'save' in request.POST:
				title = request.POST['title']
				content = request.POST['content']
				if title != '' and content != '' and not title.isspace() and not content.isspace():
					now = datetime.now()
					dt_string = now.strftime("%d-%m-%Y %H:%M")
					aut_string = request.user.first_name + " " + request.user.last_name
					raport.title = title
					raport.content = content + '\n\n\nEdytowane przez: ' + aut_string + " " + dt_string
					raport.save()
					return redirect('raports_view')
				else:
					messages.info(request, 'Tytuł i treść nie mogą być puste')
					return render(request, 'raports_edit.html', {"raport": raport})
			elif 'delete' in request.POST:
				raport.delete()
				return redirect('raports_view')
		else:
			return render(request, 'raports_edit.html', {"raport": raport})
	else:
		return redirect('login')


def to_do_list(request):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			if request.POST:
				if request.POST['title'] != '' and not request.POST['title'].isspace():
					task = Task(title=request.POST['title'])
					task.save()
				return redirect('to_do_list')
			else:
				tasks = Task.objects.all()
				return render(request, 'to_do_list.html', {"tasks": tasks})
		else:
			return redirect('index')
	else:
		return redirect('login')

def delete_task(request, taskID):
	if request.user.is_authenticated:
		if request.user.is_superuser and not taskID == None:
			Task.objects.get(id=taskID).delete()
			return redirect('to_do_list')
		else:
			return redirect('index')
	else:
		return redirect('login')

def edit_task(request, taskID):
	if request.user.is_authenticated:
		if request.user.is_superuser and request.POST:
			task = Task.objects.get(id=taskID)
			task.title = request.POST[f'title{taskID}']
			task.complete = request.POST.get(f'complete{taskID}', '') == 'on'
			task.save()
			return redirect('to_do_list')
		else:
			return redirect('index')
	else:
		return redirect('login')