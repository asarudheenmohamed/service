"""Register in product review and rating models."""


from django.contrib import admin

from app.rating.models import RatingTag, Rating


class RatingAdmin(admin.ModelAdmin):
    readonly_fields = [
        'customer',
        'increment_id',
        'rating',
        'comments',
        'created_at',
        'rating_tag']

    list_display = [f.name for f in Rating._meta.fields]


class RatingTagAdmin(admin.ModelAdmin):

    list_display = [f.name for f in RatingTag._meta.fields]

admin.site.register(RatingTag, RatingTagAdmin)
admin.site.register(Rating, RatingAdmin)
