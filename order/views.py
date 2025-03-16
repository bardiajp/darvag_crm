from django.shortcuts import render
from django.views import View
from .models import Quote

from accounts.models import Company


class QuoteView(View):
    def get(self, request, pk):
        quote = Quote.objects.get(pk=pk)
        context = {
            'quote' : quote,
            'address' : quote.address,
            'company' : quote.company,
            'items' : quote.items.all(),
        }
        return render(request, 'crm/quote_template.html', context)

