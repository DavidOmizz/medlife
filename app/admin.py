from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(Appointment)
# admin.site.register(Department)
admin.site.register(Review)
admin.site.register(Doctor)
admin.site.register(Specialty)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}