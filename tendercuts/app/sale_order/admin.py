from django.contrib import admin

# Register your models here.


from app.sale_order.model import OrderTimeElapsed


class OrderTimeElapsedAdmin(admin.ModelAdmin):
    list_display = [f.name for f in OrderTimeElapsed._meta.fields]


admin.site.register(OrderTimeElapsed, OrderTimeElapsedAdmin)
