import json
import pika

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from models.order import Order
from services.rabbitmq import RABBITMQ_URL

router = APIRouter()


def update_order_status(order_id: int, new_status, db: Session) -> Order:
    """Обновляет статус заказа в базе данных."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = new_status
    db.commit()
    db.refresh(order)
    return order


def get_order_from_queue() -> dict | None:
    """Забирает первый заказ из очереди 'new_orders'."""
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()
    method_frame, header_frame, body = channel.basic_get(
        queue="new_orders", auto_ack=True
    )

    if method_frame:
        order_id = json.loads(body)
        connection.close()
        return order_id

    connection.close()
    return None


def send_to_notification_queue(order: Order) -> None:
    """Отправляет статус заказа в очередь для уведомлений."""
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()
    channel.basic_publish(
        exchange="",
        routing_key="customer_notifications",
        body=json.dumps({"order_id": order.id, "status": order.status})
    )
    connection.close()


@router.get("/process_order/")
def process_order(db: Session = Depends(get_db)):
    """Обрабатывает заказ из очереди."""
    order_data = get_order_from_queue()

    if not order_data:
        raise HTTPException(status_code=404, detail="No orders in queue")

    order_id = order_data["order_id"]

    # Меняем статус на "processing"
    order = update_order_status(order_id, "processing", db)

    # Отправляем уведомление
    send_to_notification_queue(order)

    # Бизнес-логика обработки заказа

    # Меняем статус на "completed"
    order = update_order_status(order_id, "completed", db)

    # Отправляем уведомление
    send_to_notification_queue(order)

    return {"message": "Order processed successfully", "order_id": order_id}
