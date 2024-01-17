from django.contrib import admin

from orders.models import Order, OrderItem, Receipt


class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "order_time", ]


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["quantity", "id", ]



class ReceiptAdmin(admin.ModelAdmin):
    list_display = ["time", "calculation", "id", ]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Receipt, ReceiptAdmin)
