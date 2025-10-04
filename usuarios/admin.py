from django.contrib import admin
from .models import CustomUser 

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "nivel", "lattes", "linkedin", "researchgate")
    search_fields = ("username", "email", "nivel")
# Register your models here.
