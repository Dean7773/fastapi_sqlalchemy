from sqlalchemy.orm import Session

from db import SessionLocal, Base, engine
from models import Category, Order, Product, Shop, User


def reset_database():
    """Полностью очищает и пересоздает базу данных."""
    Base.metadata.drop_all(bind=engine)  # Удаляем все таблицы
    Base.metadata.create_all(bind=engine)  # Создаем заново


def seed_data():
    """Заполняет базу тестовыми данными."""
    session: Session = SessionLocal()

    try:
        # Добавляем пользователей
        users = [
            User(username="ivan_ivanov", email="ivan@example.com",
                 password="hashed_password"),
            User(username="maria_smirnova", email="maria@example.com",
                 password="hashed_password"),
            User(username="petr_sidorov", email="petr@example.com",
                 password="hashed_password"),
        ]
        session.add_all(users)
        session.commit()

        # Добавляем магазины
        shops = [
            Shop(name="TechStore", owner_id=users[0].id),
            Shop(name="BookWorld", owner_id=users[1].id)
        ]
        session.add_all(shops)
        session.commit()

        # Добавляем категории
        categories = [
            Category(name="Электроника"),
            Category(name="Книги"),
        ]
        session.add_all(categories)
        session.commit()

        # Добавляем товары
        products = [
            Product(name="Ноутбук", price=60000,
                    shop_id=shops[0].id, category_id=categories[0].id),
            Product(name="Смартфон", price=30000,
                    shop_id=shops[0].id, category_id=categories[0].id),
            Product(name="Книга Python", price=1500,
                    shop_id=shops[1].id, category_id=categories[1].id),
        ]
        session.add_all(products)
        session.commit()

        # Добавляем заказы
        orders = [
            Order(user_id=users[0].id, shop_id=shops[0].id,
                  product_id=products[0].id, status="new"),
            Order(user_id=users[1].id, shop_id=shops[1].id,
                  product_id=products[2].id, status="new"),
        ]
        session.add_all(orders)
        session.commit()

        print("Тестовые данные добавлены в БД!")
    except Exception as e:
        print(f"Ошибка при добавлении тестовых данных: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    reset_database()
    seed_data()
