from django.db.models import Sum
from django.shortcuts import render
from django.views.generic import View

from googlesheet.models import Receipt


class GoogleSheetView(View):
    def get(self, request):
        date = []
        rubles = []
        receipts = Receipt.objects.all()

        total = Receipt.objects.all().aggregate(Sum('price_usd'))

        for receipt in receipts:
            datestr = receipt.delivery_date.strftime("%m/%d/%Y")
            date.append(datestr)
            rubles.append(receipt.price_rub)

        context = {
            'data': receipts, 'rubles': rubles, 'date': date, 'total': total
        }
        return render(request, 'statistics.html', context)
