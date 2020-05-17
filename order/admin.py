from django.contrib import admin
from .models import Order

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
  list_display = ('ordernum', 'fcuser', 'register_date',)
  # list_display = ('ordernum', )

admin.site.register(Order, OrderAdmin)