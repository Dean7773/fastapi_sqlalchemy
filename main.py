from fastapi import FastAPI

from routes import consumer, notification, publisher
from services.rabbitmq import create_channel


app = FastAPI()

QUEUES = ["new_orders", "processing_orders",
          "customer_notifications", "customer_notifications_dlx"]


@app.on_event("startup")
def setup_queues():
    "Создает очереди при запуске сервера."
    connection, channel = create_channel()
    try:
        for queue in QUEUES:
            channel.queue_declare(queue=queue)
    finally:
        channel.exchange_declare(exchange="dlx_exchange",
                                 exchange_type="direct")
        channel.queue_bind(exchange="dlx_exchange",
                           queue="customer_notifications_dlx")
        connection.close()


# Подключаем роутеры
app.include_router(consumer.router)
app.include_router(publisher.router)
app.include_router(notification.router)
