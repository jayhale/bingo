from django.contrib import admin

from ideas.models import ( CenterSquareIdea, SquareIdea, CenterSquareVote,
    SquareVote )


class CenterSquareIdeaAdmin(admin.ModelAdmin):
    pass
admin.site.register(CenterSquareIdea, CenterSquareIdeaAdmin)


class SquareIdeaAdmin(admin.ModelAdmin):
    pass
admin.site.register(SquareIdea, SquareIdeaAdmin)


class CenterSquareVoteAdmin(admin.ModelAdmin):
    pass
admin.site.register(CenterSquareVote, CenterSquareVoteAdmin)


class SquareVoteAdmin(admin.ModelAdmin):
    pass
admin.site.register(SquareVote, SquareVoteAdmin)