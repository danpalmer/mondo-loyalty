from django.shortcuts import redirect
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'home/view.html'

    def get(self, request):
        if request.user.is_authenticated():
            return redirect('accounts:dashboard')

        return super().get(request)
