from django.contrib import admin

from .models import Booking, BusinessHour, Restaurant, Setting, Table


class BookingHourInline(admin.TabularInline):
    model = BusinessHour
    extra = 7
    show_change_link = True


class TableInline(admin.TabularInline):
    model = Table
    extra = 1
    show_change_link = True


class SettingInline(admin.TabularInline):
    model = Setting
    extra = 1
    show_change_link = True


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "address1",
        "address2",
        "postcode",
        "created_at",
        "modified_at",
    )
    inlines = (
        BookingHourInline,
        TableInline,
        SettingInline,
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "restaurant",
        "table",
        "date",
        "created_at",
        "modified_at",
    )
