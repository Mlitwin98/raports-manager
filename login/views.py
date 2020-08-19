from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
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
