from django import forms
from django.utils.timezone import now

from cartapp.models import DaysOfWeek, Service, WindowWashing
from common.const import CLEANING_TIME_CHOICES


class AddToCartForm(forms.Form):

    services = forms.ModelMultipleChoiceField(queryset=Service.objects.all(),
                                              widget=forms.CheckboxSelectMultiple,
                                              required=False,
                                              error_messages={'required': 'Необходимо выбрать услугу/услуги!'}
                                              )

    comment = forms.CharField(max_length=1024, widget=forms.Textarea, required=False)

    cleaning_days = forms.ModelMultipleChoiceField(queryset=DaysOfWeek.objects.all(),
                                                   widget=forms.CheckboxSelectMultiple(),
                                                   required=False,
                                                   error_messages={'required': 'Необходимо выбрать день/дни недели!'}
                                                   )

    cleaning_time = forms.ChoiceField(choices=CLEANING_TIME_CHOICES,
                                      widget=forms.RadioSelect,
                                      required=False,
                                      error_messages={'required': 'Необходимо выбрать промежуток времени уборки!'}
                                      )

    number_stuff = forms.IntegerField(min_value=1,
                                      widget=forms.NumberInput(attrs={'id': 'amount',
                                                                      'value': '1'}),
                                      required=False
                                      )
    is_windows = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        services_d = kwargs.pop('services_dict')
        self.service_type = kwargs.pop('type_servise')
        super().__init__(*args, **kwargs)
        self.fields['services'].queryset = services_d
        result_required_for_daily_as_scheduled = True if self.service_type == 'daily_as_scheduled' else False
        result_required_for_services = True if self.service_type not in ['window_cleaning', 'daily_as_scheduled'] else False
        self.fields['cleaning_days'].required = result_required_for_daily_as_scheduled
        self.fields['cleaning_time'].required = result_required_for_daily_as_scheduled
        self.fields['services'].required = result_required_for_services



    # def clean_cleaning_days(self):
    #     if 'daily_as_scheduled' == self.service_type:
    #         empty_list = True if len(self.cleaned_data['cleaning_days']) == 0 else False
    #         if empty_list:
    #             raise forms.ValidationError('Необходимо выбрать по каким дням необходима уборка')
    #         else:
    #             return self.cleaned_data['cleaning_days']

class AddToCartWindowsForm(forms.ModelForm):
    class Meta:
        model = WindowWashing
        fields = '__all__'


class AddDateToCartForm(forms.Form):
    date_order = forms.DateField(widget=forms.RadioSelect)
    is_other_date = forms.BooleanField(required=False)

    def clean_date_order(self):
        date_order = self.cleaned_data['date_order']
        now_date = now().date()
        if date_order < now_date:
            raise forms.ValidationError('Нельзя вводить задним числом дату')
        return date_order
