from django.contrib import admin

from accounts.models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """
    Transaction Model admin parameters.
    """

    list_display = ('user', )
    search_fields = ('user__username', )
