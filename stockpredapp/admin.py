from django.contrib import admin

from .models import Rnn_data, Rnn_result, Code_name

# Register your models here.


class Code_nameAdmin(admin.ModelAdmin):
    search_fields = ['stock_name']


admin.site.register(Rnn_data)
admin.site.register(Rnn_result)
admin.site.register(Code_name, Code_nameAdmin)
