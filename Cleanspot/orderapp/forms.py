from django import forms

from mainapp.models import Premises


class AddPremiseToOrderForm(forms.ModelForm):

    class Meta:
        model = Premises
        fields = ('premises_owner', 'premises_type', 'premises_city', 'premises_street', 'premises_house_num',
                  'premises_apartment', 'premises_intercom', 'premises_entrance', 'premises_floor')
        widgets = {'premises_owner': forms.HiddenInput}
