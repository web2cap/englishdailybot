from django.contrib import admin

from .models import (
    Word,
    Collection,
    CollectionSubscription,
    Translation,
    WordTranslation,
)


class WordInstanceInline(admin.TabularInline):
    model = Word.collection.through
    extra = 3
    min_num = 0


class WordTranslationInstanceInline(admin.TabularInline):
    model = WordTranslation
    extra = 3
    min_num = 1


class CollectionAdmin(admin.ModelAdmin):
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
    list_display = ("en", "collections_count")
    list_filter = ("collection",)
    search_fields = ("en",)
    inlines = (WordTranslationInstanceInline,)


class TranslationAdmin(admin.ModelAdmin):
    pass


class CollectionSubscriplionAdmin(admin.ModelAdmin):
    list_display = ("collection", "user", "rate")
    list_filter = ("collection",)


admin.site.register(Collection, CollectionAdmin)
admin.site.register(Word, WordAdmin)
admin.site.register(Translation, TranslationAdmin)
admin.site.register(CollectionSubscription, CollectionSubscriplionAdmin)
