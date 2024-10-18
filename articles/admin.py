from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Scope, Tag

class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        main_tag_count = sum(1 for form in self.forms if form.cleaned_data.get('is_main'))
        if main_tag_count > 1:
            raise ValidationError('Должен быть только один основной раздел.')
        if main_tag_count == 0:
            raise ValidationError('Необходимо указать один основной раздел.')
        return super().clean()

class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
