from django.contrib import admin
from .models import LegalAct, Chapter, Section

class SectionInline(admin.TabularInline):
    model = Section
    extra = 1

class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1

@admin.register(LegalAct)
class LegalActAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description')
    inlines = [ChapterInline]

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter_number', 'act')
    list_filter = ('act',)
    inlines = [SectionInline]

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'section_number', 'chapter')
    list_filter = ('chapter__act',)
    search_fields = ('title', 'content', 'section_number')
