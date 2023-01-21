from django.contrib import admin

from .models import (
    Word,
    WordList,
    WordListSubscriplion,
    Translation,
    WordTranslation,
)


class WordInstanceInline(admin.TabularInline):
    model = Word.list.through
    extra = 3
    # max_num = 1
    min_num = 1


class WordTranslationInstanceInline(admin.TabularInline):
    model = WordTranslation
    extra = 3
    # max_num = 1
    min_num = 1


class WordListAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "native",
        "access",
        "author",
        "words_count",
        "popularity",
    )
    search_fields = (
        "name",
        "words",
    )
    list_filter = ("native", "access")
    inlines = (WordInstanceInline,)

    def words_count(self, obj):
        return obj.words_count


class WordAdmin(admin.ModelAdmin):
    list_display = ("en", "lists_count")
    list_filter = ("list",)
    search_fields = ("en",)
    inlines = (WordTranslationInstanceInline,)


class TranslationAdmin(admin.ModelAdmin):
    pass


class WordListSubscriplionAdmin(admin.ModelAdmin):
    list_display = ("list", "user", "rate")
    list_filter = ("list",)


admin.site.register(WordList, WordListAdmin)
admin.site.register(Word, WordAdmin)
admin.site.register(Translation, TranslationAdmin)
admin.site.register(WordListSubscriplion, WordListSubscriplionAdmin)
