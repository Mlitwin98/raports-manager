from django.db import models
from django.contrib.auth.models import Group


# Create your models here.
class Raport(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	author_name = models.CharField(max_length=100)
	author_lastname = models.CharField(max_length=100)
	dateTime = models.DateTimeField(auto_now_add=True)
	objects = models.Manager()

	@classmethod
	def create(cls, title, content, author_name, author_lastname):
		raport = cls(title=title, content=content, author_name=author_name, author_lastname=author_lastname)
		return raport

class Task(models.Model):
	title = models.TextField()
	complete = models.BooleanField(default=False)

Group.add_to_class('calendar_link', models.TextField(blank=True))