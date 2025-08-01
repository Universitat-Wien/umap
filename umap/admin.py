import csv
from datetime import datetime

from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.contrib.auth.models import User
from django.contrib.gis import admin
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from .models import DataLayer, Licence, Map, Pictogram, Team, TileLayer


class CSVExportMixin:
    actions = ["as_csv"]

    @admin.action(description=_("CSV Export"))
    def as_csv(self, request, queryset):
        modelname = queryset.model.__name__.lower()
        filename = f"umap_{modelname}_{datetime.now().isoformat()}.csv"
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

        writer = csv.writer(response)
        writer.writerow(self.csv_fields)
        for user in queryset:
            writer.writerow(getattr(user, field) for field in self.csv_fields)
        return response


class TileLayerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "rank",
    )
    list_editable = ("rank",)


class MapAdmin(CSVExportMixin, admin.GISModelAdmin):
    search_fields = ("name",)
    autocomplete_fields = ("owner", "editors")
    list_filter = ("share_status",)
    csv_fields = (
        "pk",
        "name",
        "center",
        "zoom",
        "created_at",
        "modified_at",
        "edit_status",
        "share_status",
        "owner_id",
        "team_id",
    )


class PictogramAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
    )
    list_editable = ("category",)
    list_filter = ("category",)


class TeamAdmin(admin.ModelAdmin):
    filter_horizontal = ("users",)


class UserAdmin(CSVExportMixin, UserAdminBase):
    csv_fields = [
        "pk",
        "username",
        "email",
        "first_name",
        "last_name",
        "last_login",
        "date_joined",
    ]


admin.site.register(Map, MapAdmin)
admin.site.register(DataLayer)
admin.site.register(Pictogram, PictogramAdmin)
admin.site.register(TileLayer, TileLayerAdmin)
admin.site.register(Licence)
admin.site.register(Team, TeamAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
