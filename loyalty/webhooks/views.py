from django.http import HttpResponse
from django.views.generic import DetailView
from django.db.transaction import on_commit

from loyalty.accounts.models import Account

from .tasks import scrape_balance_for_last_transaction


class Hook(DetailView):
    model = Account

    def post(self, request, pk):
        account = self.get_object()
        print(request.POST)
        if account.schemes.filter(erroring=False).exists():
            on_commit(lambda: scrape_balance_for_last_transaction(account))
        return HttpResponse()
