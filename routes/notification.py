import json
import pika

from fastapi import APIRouter, HTTPException

from services.rabbitmq import RABBITMQ_URL

router = APIRouter()


def get_rabbitmq_channel():
    """Создает соединение и канал."""
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    return connection, connection.channel()


def search_message(queue, order_id):
    """Поиск сообщения в очередях."""
    messages = []
    connection, channel = get_rabbitmq_channel()

    while True:
        method_frame, header_frame, body = channel.basic_get(
            queue=queue, auto_ack=False
        )
        if not method_frame:
            break

        message = json.loads(body)
        if message.get("order_id") == order_id:
            messages.append(message["status"])
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    connection.close()
    return messages


@router.get("/order_messages/{order_id}")
def get_order_messages(order_id: int):
    """Получает сообщения о статусе заказа из customer_notifications."""
    messages = search_message("customer_notifications", order_id)
    if not messages:
        messages = search_message("customer_notifications_dlx", order_id)

    if not messages:
        raise HTTPException(
            status_code=404,
            detail="Нет сообщений для данного заказа"
        )

    return {"order_id": order_id, "statuses": messages}
