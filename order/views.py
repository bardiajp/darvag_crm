from django.shortcuts import render
from django.views import View

from .models import Quote


class QuoteView(View):
    def get(self, request, pk):
        quote = Quote.objects.get(pk=pk)
        context = {
            'quote': quote,
            'address': quote.address,
            'company': quote.company,
            'items': quote.items.all(),
            'packages': quote.packages.all(),
        }
        print(context)
        return render(request, 'crm/quote_template.html', context)
