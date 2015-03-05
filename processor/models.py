from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
# Create your models here.

class RhinoScript(models.Model):
	script = models.FileField(upload_to='scripts')
	created = models.TimeField(auto_now_add=True)
	modified = models.TimeField(auto_now=True)
	creator = models.ForeignKey(User)
	order = models.IntegerField(default=1)

	def __unicode__(self):
		return self.script.url

class Component(models.Model):
	name = models.CharField(unique=True, max_length=16)
	url = models.URLField()

	def __unicode__(self):
		return self.name

class ComponentForm(ModelForm):
	class Meta:
		model = Component

class Tweet(models.Model):
	key = models.CharField(max_length=16)
	content = models.TextField()

	def __unicode__(self):
		return self.content