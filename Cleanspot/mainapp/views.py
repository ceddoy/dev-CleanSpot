from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView

from cartapp.forms import AddToCartForm
from cartapp.models import UserTypeForServiceType, ServiceType, Service
from cartapp.views import ShowListServicesView


def main(request):
    return render(request, 'mainapp/index.html')


class PrivateSupportingTemplateView(ShowListServicesView):
    def get_template_names(self):
        user_type = self.kwargs['usertypeforservicetype_slug']
        service_type = self.kwargs['servisetype_slug']
        template_name = f'mainapp/{user_type}_{service_type}.html'
        return [template_name]
