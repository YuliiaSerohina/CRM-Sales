from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, LargeBinary, Date
from database import Base
from datetime import date


class User(Base):
    __tablename__= 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    organization_name = Column(String(100), nullable=False)
    mail = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)

    def __init__(self, name, organization_name, mail, password):
        self.name = name
        self.organization_name = organization_name
        self.mail = mail
        self.password = password

    def __repr__(self):
        return f'User {self.name}, Organization name {self.organization_name}, mail {self.mail}'


class ProductGroup(Base):
    __tablename__ = 'product_group'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return f'Group name {self.name}'


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    photo = Column(LargeBinary)
    product_code = Column(String(50), nullable=True)
    product_group = Column(Integer, ForeignKey('product_group.id'), nullable=True)
    description = Column(String(500), nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __init__(self, name, photo, product_code, product_group, description, user_id):
        self.name = name
        self.photo = photo
        self.product_code = product_code
        self.product_group = product_group
        self.description = description
        self.user_id = user_id

    def __repr__(self):
        return f'{self.photo} {self.name}, {self.product_code}, {self.product_group}, {self.description}'


class SellingPrice(Base):
    __tablename__ = 'selling_price'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, default=date.today())
    price = Column(Integer, nullable=False )
    product_id = Column(Integer, ForeignKey('product.id'), nullable=True)

    def __init__(self, price, product_id):
        self.price = price
        self.product_id = product_id

    def __repr__(self):
        return f'{self.date} {self.product_id} {self.price}'


class CostPrice(Base):
    __tablename__ = 'cost_price'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, default=date.today())
    price = Column(Integer, nullable=False )
    product_id = Column(Integer, ForeignKey('product.id'), nullable=True)

    def __init__(self, price, product_id):
        self.price = price
        self.product_id = product_id

    def __repr__(self):
        return f'{self.date} {self.product_id} {self.price}'



 class Stock(Base):
     __tablename__ = 'stock'
     id = Column(Integer, primary_key=True, autoincrement=True)
     stock = Column(Integer, nullable=False)
     product_id = Column(Integer, ForeignKey('product.id'), nullable=True)

     def __init__(self, stock, product_id):
         self.stock = stock
         self.product_id = product_id

     def __repr__(self):
         return f'{self.product_id} {self.stock}'


class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(30), nullable=True)
    mail = Column(String(30), nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __init__(self, name, phone, mail):
        self.name = name
        self.phone = phone
        self.mail = mail

    def __repr__(self):
        return f'{self.name} {self.phone} {self.mail}'

class OrderStatus(Base):
    __tablename__ = 'order_status'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return f'{self.name}'


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, default=date.today())
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=True)
    order_status_id = Column(Integer, ForeignKey('order_status.id'), nullable=False)
    selling_price_id = Column(Integer, ForeignKey('selling_price.id'), nullable=False)
    cost_price = Column(Integer, ForeignKey('cost_price.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    order_sum = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __init__(self, customer_id, product_id, order_status_id, order_sum,
                 selling_price_id, cost_price, quantity, user_id):
        self.customer_id = customer_id
        self.product_id = product_id
        self.order_status_id = order_status_id
        self.order_sum = order_sum
        self.selling_price_id = selling_price_id
        self.cost_price = cost_price
        self.quantity = quantity
        self.user_id = user_id

    def __repr__(self):
        return f'{self.date} {self.id} {self.order_status_id} {self.customer_id} {self.product_id},' \
               f'{self.quantity} {self.selling_price_id}{self.order_sum}'













