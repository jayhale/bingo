from django.contrib import admin

from cards.models import Card, CardSquare, Square, Week


class CardAdmin(admin.ModelAdmin):
    pass
admin.site.register(Card, CardAdmin)


class CardSquareAdmin(admin.ModelAdmin):
    pass
admin.site.register(CardSquare, CardSquareAdmin)


class SquareAdmin(admin.ModelAdmin):
    exclude = ('order', )
    list_filter = ('week', )
admin.site.register(Square, SquareAdmin)


class WeekAdmin(admin.ModelAdmin):
    pass
admin.site.register(Week, WeekAdmin)