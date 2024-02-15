from django.contrib import admin

from orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('items',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "order_time", 'paid']
    list_filter = ('paid',)
    inlines =(OrderItemInline,)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["quantity", "id", ]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

