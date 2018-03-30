from django.contrib import admin
from .models import Rank


class RankingAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'score', 'puzzle_name', 'taken_at'
    )

    list_filter = (
        'puzzle__name',
    )

    ordering = (
        'score',
    )

    def puzzle_name(self, obj):
        return obj.puzzle.name if obj.puzzle else 'None'

    puzzle_name.short_description = 'Puzzle Name'

    def username(self, obj):
        return obj.user.username

    username.short_description = 'Username'


admin.site.register(Rank, RankingAdmin)
