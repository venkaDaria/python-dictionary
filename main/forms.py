from django import forms

from main.models import Chain


class AddForm(forms.ModelForm):
    ru_value1 = forms.CharField(required=True)
    ru_info1 = forms.CharField(required=False)
    ru_value2 = forms.CharField(required=False)
    ru_info2 = forms.CharField(required=False)
    ru_value3 = forms.CharField(required=False)
    ru_info3 = forms.CharField(required=False)

    en_value1 = forms.CharField(required=True)
    en_info1 = forms.CharField(required=False)
    en_value2 = forms.CharField(required=False)
    en_info2 = forms.CharField(required=False)
    en_value3 = forms.CharField(required=False)
    en_info3 = forms.CharField(required=False)

    de_value1 = forms.CharField(required=True)
    de_info1 = forms.CharField(required=False)
    de_value2 = forms.CharField(required=False)
    de_info2 = forms.CharField(required=False)
    de_value3 = forms.CharField(required=False)
    de_info3 = forms.CharField(required=False)

    tag = forms.CharField(required=True)
    part_speech = forms.CharField(required=True)

    class Meta:
        model = Chain
        fields = ['part_speech']
