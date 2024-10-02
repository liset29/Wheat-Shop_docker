from django import forms

from wheat.models import Orders


class OrderForm(forms.ModelForm):
    contact_name = forms.CharField(required=True, label='Имя',
                                   widget=forms.TextInput(attrs={'class': 'form-input'}))

    phone = forms.CharField(max_length=15, required=True, label='Телефон',
                            widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Orders
        fields = ('city', 'address',)
