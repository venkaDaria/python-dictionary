from django.contrib import admin

from main.models import Word, WordBlock, Chain, Tag


class WordAdmin(admin.ModelAdmin):
    list_display = (
        'value',
        'lang',
        'order',
        'info',
        'block',
        'created_at'
    )
    list_filter = ('lang',)
    search_fields = ('value',)


class WordInline(admin.StackedInline):
    model = Word
    extra = 1


class WordBlockAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'get_words',
        'created_at',
    )
    inlines = [WordInline]

    def get_words(self, obj):
        return obj.words_string()

    get_words.short_description = 'Words'


class ChainAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'ru_block',
        'en_block',
        'de_block',
        'part_speech',
        'tag',
        'created_at',
    )


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
    )


admin.site.register(Word, WordAdmin)
admin.site.register(WordBlock, WordBlockAdmin)
admin.site.register(Chain, ChainAdmin)
admin.site.register(Tag, TagAdmin)
