from django.contrib import admin
from eventex.subscriptions.models import  Subscription
from django.utils.timezone import now


class SubscriptionModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'cpf', 'created_at', 'subscribed_today')
    date_hierarchy = 'created_at'
    search_fields = ('name', 'email', 'cpf')
    list_filter = ('created_at',)

    def subscribed_today(self, obj):
       return obj.created_at == now().date() 

    subscribed_today.short_description = 'Inscritos Hoje'
    subscribed_today.boolean = True


admin.site.register(Subscription, SubscriptionModelAdmin)