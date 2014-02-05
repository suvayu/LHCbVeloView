from django.contrib import admin
from django.db import models

# Create your models here.
class Diagrams(models.Model):
    name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


# class Trends(models.Model):
#     name = models.CharField(max_length=30)
#     created = models.DateTimeField(auto_now_add=True)
#
#     def __unicode__(self):
#         return self.name


class DiagramsAdmin(admin.ModelAdmin):
    search_fields = ["name"]

admin.site.register(Diagrams, DiagramsAdmin)