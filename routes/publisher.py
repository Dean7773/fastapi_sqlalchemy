import json
import pika

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
from models.order import Order
from services.rabbitmq import RABBITMQ_URL

router = APIRouter()


@router.post("/orders/")
def create_order(
        user_id: int,
        shop_id: int,
        product_id: int,
        db: Session = Depends(get_db)
):
    """Создает новый заказ и отправляет его в очередь new_orders."""
    order = Order(user_id=user_id, shop_id=shop_id, product_id=product_id)
    db.add(order)
    db.commit()
    db.refresh(order)

    # Отправляем заказ в очередь
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()
    channel.basic_publish(
        exchange="",
        routing_key="new_orders",
        body=json.dumps({"order_id": order.id})
    )
    connection.close()

    return {"message": "Order created", "order_id": order.id}
