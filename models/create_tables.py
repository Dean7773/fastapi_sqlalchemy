from db import engine, Base
from models.users import User
from models.shops import Shop
from models.category import Category
from models.products import Product


Base.metadata.create_all(bind=engine)
