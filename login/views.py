from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from datetime import datetime
from .models import Raport


# Create your views here.
def index(request):
	if request.user.is_authenticated:
		return render(request, "index.html")
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
			messages.info(request, 'invalid credentials')
			return redirect('login')
	else:
		return render(request, 'login.html')


def logout(request):
	auth.logout(request)
	return redirect('index')


def raports_maker(request):
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
			return redirect('reports_maker')
	else:
		return render(request, 'raports_maker.html')


def raports_view(request):
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
			dateStart = datetime.strptime(dates[0], '%m/%d/%Y').date()
			dateEnd = datetime.strptime(dates[1], '%m/%d/%Y').date()

			raports = raports.filter(dateTime__gte=dateStart)
			raports = raports.filter(dateTime__lte=dateEnd)
		return render(request, 'raports_view.html', {"raports": raports})
	else:
		visibleRaports = 50
		numOfRaports = Raport.objects.all().count()
		if numOfRaports < visibleRaports:
			visibleRaports = numOfRaports
		raports = Raport.objects.all()[numOfRaports-visibleRaports:numOfRaports]
		return render(request, 'raports_view.html', {"raports": raports})
