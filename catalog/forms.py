from django.forms import ModelForm, forms

from catalog.models import Products, Version
from common.views import StyleFormMixin


class ProductsForm(ModelForm, StyleFormMixin):
    class Meta:
        model = Products
        exclude = ('views_count', 'created_at', 'updated_at')

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')
        prohibited_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                            'радар']
        # my_set = set(prohibited_words)
        if cleaned_data in prohibited_words:
            raise forms.ValidationError('Данное слово нельзя использовать в карточке')

        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description')
        prohibited_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                            'радар']
        if cleaned_data in prohibited_words:
            raise forms.ValidationError('Данное слово нельзя использовать в карточке')

        return cleaned_data


class VersionForm(ModelForm, StyleFormMixin):
    class Meta:
        model = Version
        fields = ('version_number', 'version_title', 'version_is_active')