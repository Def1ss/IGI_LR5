from django.contrib import admin
from .models import News, GlossaryTerm, Vacancy, FAQ, CompanyHistory, CompanyContact

admin.site.register(News)
admin.site.register(GlossaryTerm)
admin.site.register(Vacancy)
admin.site.register(FAQ)

@admin.register(CompanyHistory)
class CompanyHistoryAdmin(admin.ModelAdmin):
    list_display = ("year", "event")
    list_filter = ("year",)
    search_fields = ("event",)

@admin.register(CompanyContact)
class CompanyContactAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "phone")
    search_fields = ("name", "role")