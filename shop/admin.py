from django.contrib import admin
from django.utils.safestring import mark_safe

from shop.models import Product, Payment, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]
    list_display_links = ('id', 'name', 'code')
    save_on_top = True

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image_url.url} width="100" height="100"')

    get_image.short_description = 'Миниатюра'


admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderItem)
