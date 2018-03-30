from django.contrib import admin
from .models import Puzzle, Parts


class PuzzleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    search_fields = (
        'name',
    )


class PartsAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'x', 'y', 'puzzle_name'
    )
    list_filter = (
        'puzzle__name',
    )
    readonly_fields = (
        'ratio', 'most_far_distance'
    )

    def puzzle_name(self, obj):
        return obj.puzzle.name if obj.puzzle else 'None'

    puzzle_name.short_description = 'Puzzle Name'


admin.site.register(Puzzle, PuzzleAdmin)
admin.site.register(Parts, PartsAdmin)
