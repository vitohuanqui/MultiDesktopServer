from django.contrib import admin

from accounts.models import Document, UserIP, Log


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """
    Transaction Model admin parameters.
    """

    list_display = ('user', )
    search_fields = ('user__username', )


@admin.register(UserIP)
class UserIPAdmin(admin.ModelAdmin):
    list_display = ('user', )

@admin.register(Log)
class UserIPAdmin(admin.ModelAdmin):
    list_display = ('user', )
