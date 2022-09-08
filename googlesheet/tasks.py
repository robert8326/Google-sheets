import requests
import datetime
import gspread

from config.celery import app
from xml.etree import ElementTree
from googlesheet.models import Receipt
from decimal import Decimal


#######################
###  SHEDULE TASKS  ###
#######################


@app.task(ignore_result=True, name='google_sheets.update_data')
def update_data():
    """A function to read and write a data from a Google page"""
    sa = gspread.service_account(filename='google_sheets.json')
    sh = sa.open("Receipt")
    wsk = sh.worksheet("Sheet1")
    datas = wsk.get_all_records()

    now = datetime.date.today().strftime('%d/%m/%Y')
    response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp?date_req=' + now, stream=True)
    tree = ElementTree.fromstring(response.content)

    """ Get information about the conversion of dollars to rubles according to the exchange
         rate of the Central Bank of the Russian Federation """
    for x in tree.iter('Valute'):
        if x.get('ID') == 'R01235':
            worth = x.find('Value').text
            y = worth.replace(',', '.')
            worth = float(y)

    """Saving data to the database """
    for data in datas:
        rubles = round(worth, 2) * data['стоимость,$']
        date = datetime.datetime.strptime(data['срок поставки'], '%d.%m.%Y').date()
        Receipt.objects.update_or_create(
            order_id=data['заказ №'],
            defaults={
                'source_id': data['№'],
                'order_id': data['заказ №'],
                'price_usd': Decimal(data['стоимость,$']),
                'price_rub': round(Decimal(rubles), 2),
                'delivery_date': date,
            }
        )
