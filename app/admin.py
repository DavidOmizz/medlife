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
    
@admin.register(Post)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug','category','views')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title', )}
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'active', 'created_on')
    search_fields = ('name', 'email', 'body')    
    
    
    