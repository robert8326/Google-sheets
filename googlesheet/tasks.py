import requests
import datetime
import gspread
import telepot

from environs import Env
from config.celery import app
from xml.etree import ElementTree
from googlesheet.models import Receipt
from decimal import Decimal

env = Env()
env.read_env()


#######################
###  SHEDULE TASKS  ###
#######################


@app.task(ignore_result=True, name='google_sheets.update_data')
def update_data():  # Celery задача для обновления, создания и удаления объектов
    sa = gspread.service_account(filename='google_sheets.json')
    sh = sa.open("Receipt")
    wsk = sh.worksheet("Sheet1")
    datas = wsk.get_all_records()

    now = datetime.date.today().strftime('%d/%m/%Y')
    response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp?date_req=' + now, stream=True)
    tree = ElementTree.fromstring(response.content)

    for x in tree.iter('Valute'):
        if x.get('ID') == 'R01235':
            worth = x.find('Value').text
            y = worth.replace(',', '.')
            worth = float(y)

    order_id = []
    receipts = Receipt.objects.all().values_list('order_id', flat=True)
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
        order_id.append(data['заказ №'])

    if receipts.count() > len(order_id):  # для удаления объектов
        ids = set(receipts) - set(order_id)
        Receipt.objects.filter(order_id__in=ids).delete()


@app.task(ignore_result=True, name='google_sheets.send_message')  # Пока не актуален, но работает правильно
def send_message():  # Celery задача для отправки смс на телеграм
    token = env.str('token')
    id_ = env.str('id')
    telegramBot = telepot.Bot(token)

    data = Receipt.objects.filter(delivery_date__gte=datetime.date.today())
    for dt in data:
        text = f'Срок вашегоs заказа - {dt.order_id} прошел'
        telegramBot.sendMessage(id_, text, parse_mode="Markdown")
