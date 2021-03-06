from web.models import TaxonomyArea, TaxonomyCategory, TaxonomyItem, OwnershipRequest
from django.contrib import admin
from django import forms

admin.site.register(TaxonomyArea)
admin.site.register(TaxonomyCategory)
admin.site.register(OwnershipRequest)


class TaxonomyItemForm(forms.ModelForm):
    detail_html = forms.CharField(widget=forms.Textarea(attrs={'cols': 100, 'rows': 40}))
    detail_html.short_description = "Test"

    class Meta:
        model = TaxonomyItem


class TaxonomyItemAdmin(admin.ModelAdmin):
    form = TaxonomyItemForm


admin.site.register(TaxonomyItem, TaxonomyItemAdmin)
