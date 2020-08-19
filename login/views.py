from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages


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
