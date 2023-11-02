from sqlalchemy import Column, Integer, String,  ForeignKey, LargeBinary, Date
from sqlalchemy.orm import relationship
from database import Base
from datetime import date


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
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


class ItemGroup(Base):
    __tablename__ = 'item_group'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return f'Group name {self.name}'


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    photo = Column(LargeBinary)
    item_code = Column(String(50), nullable=True)
    item_group = Column(Integer, ForeignKey('item_group.id'), nullable=True)
    description = Column(String(500), nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __init__(self, name, user_id, photo=None, item_code=None, item_group=None, description=None):
        self.name = name
        self.photo = photo
        self.item_code = item_code
        self.item_group = item_group
        self.description = description
        self.user_id = user_id

    def __repr__(self):
        return f'{self.photo} {self.name}, {self.item_code}, {self.item_group}, {self.description}'


class SellingPrice(Base):
    __tablename__ = 'selling_price'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, default=date.today())
    price = Column(Integer, nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'), nullable=True)

    def __init__(self, price, item_id):
        self.price = price
        self.item_id = item_id

    def __repr__(self):
        return f'{self.date} {self.item_id} {self.price}'


class CostPrice(Base):
    __tablename__ = 'cost_price'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, default=date.today())
    price = Column(Integer, nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'), nullable=True)

    def __init__(self, price, item_id):
        self.price = price
        self.item_id = item_id

    def __repr__(self):
        return f'{self.date} {self.item_id} {self.price}'


class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock = Column(Integer, nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'), nullable=True)

    def __init__(self, stock, item_id):
        self.stock = stock
        self.item_id = item_id

    def __repr__(self):
        return f'{self.item_id} {self.stock}'


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
    order_items = relationship('OrderItem', back_populates='order')
    order_status_id = Column(Integer, ForeignKey('order_status.id'), nullable=False)
    order_total_quantity = Column(Integer, nullable=False)
    order_total_sum = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __init__(self, customer_id, order_status_id, order_total_sum, order_total_quantity, user_id):
        self.customer_id = customer_id
        self.order_status_id = order_status_id
        self.order_total_sum = order_total_sum
        self.order_total_quantity = order_total_quantity
        self.user_id = user_id

    def __repr__(self):
        return f'{self.date} {self.id} {self.order_status_id} {self.customer_id},' \
               f'{self.order_total_quantity} {self.order_total_sum}'


class OrderItem(Base):
    __tablename__ = 'order_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    order = relationship('Order', back_populates='order_items')
    item_id = Column(Integer, ForeignKey('item.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    cost_price = Column(Integer, ForeignKey('cost_price.id'), nullable=False)
    selling_price_id = Column(Integer, ForeignKey('selling_price.id'), nullable=False)
    item_selling_sum = Column(Integer, nullable=False)
    item_cost_sum = Column(Integer, nullable=False)

    def __init__(self, order_id, item_id, quantity, cost_price,
                 selling_price_id, item_selling_sum, item_cost_sum):
        self.order_id = order_id
        self.item_id = item_id
        self.quantity = quantity
        self.cost_price = cost_price
        self.selling_price_id = selling_price_id
        self.item_selling_sum = item_selling_sum
        self.item_cost_sum = item_cost_sum

    def __repr__(self):
        return f'{self.order_id} {self.item_id} {self.quantity} {self.selling_price_id} {self.item_selling_sum}'




