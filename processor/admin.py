from django.contrib import admin
from processor.models import RhinoScript, Component, Tweet

admin.site.register(RhinoScript)
admin.site.register(Component)

admin.site.register(Tweet)