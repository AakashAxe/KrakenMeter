from django.contrib import admin

from .models import ProcessedFiles, MPANCore, Meter, Reading

# Register your models here.
admin.site.register(ProcessedFiles)
admin.site.register(MPANCore)
admin.site.register(Meter)
admin.site.register(Reading)


