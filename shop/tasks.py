from time import sleep
from test_api.celery import shared_task

@shared_task()
def send_email_task(sender, instance):
    original_items = instance.items
    id_ = instance.id
    sleep(60*5) 
    cart = sender.objects.get(id=id_)
    if cart.items == original_items:
        print('Корзина не обновлялась 5 минут')
        return 'Notified'
    return False