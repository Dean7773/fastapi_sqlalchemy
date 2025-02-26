import pika

RABBITMQ_URL = "amqp://dean:dean@rabbitmq:5672/"


def create_channel():
    """Создает подключение к RabbitMQ."""
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()
    return connection, channel
