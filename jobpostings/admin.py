from django.contrib import admin

from .models import User, Company, Jobposting, Apply

admin.site.register(User)
admin.site.register(Company)
admin.site.register(Jobposting)
admin.site.register(Apply)
