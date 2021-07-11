from django.contrib import admin
from .models import Product,Category,Customer,Order
# Register your models here.


class AdminProduct(admin.ModelAdmin):
    # table view
    list_display = ['name','price','category']


admin.site.register(Product,AdminProduct)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)