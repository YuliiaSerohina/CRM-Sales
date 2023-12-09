from flask import Flask, render_template, redirect, url_for, session, flash, request
import database
from models import User, Customer, Item, ItemGroup, Order, OrderItem, Stock, SellingPrice, CostPrice, OrderStatus
from flask_session import Session
from sqlalchemy import desc
import io
import base64
from flask_paginate import Pagination, get_page_parameter

app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/', methods=['GET', 'POST'])
def registration():
    database.init_db()
    if request.method == 'POST':
        user_name = request.form.get('name')
        user_mail = request.form.get('mail')
        user_password = request.form.get('password')
        user_company_name = request.form.get('company_name')
        user_add_new = User(user_name, user_company_name, user_mail, user_password)
        database.db_session.add(user_add_new)
        database.db_session.commit()
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        database.init_db()
        user_name = request.form.get('name')
        user_password = request.form.get('password')
        find_user = database.db_session.query(User).filter_by(name=user_name, password=user_password).first()
        if not find_user:
            return redirect(url_for('login'))
        else:
            session['user_id'] = find_user.id
            session['name'] = find_user.name
            return redirect(url_for('user_main_page', user=find_user.name))
    return render_template('login.html')


@app.route('/logout/')
def logout():
    session.pop('name')
    return redirect(url_for('login'))


@app.route('/crm/', methods=['GET', 'POST'])
def user_main_page():
    return render_template('crm.html')


@app.route('/item_groups/', methods=['GET', 'POST'])
def item_group_add():
    database.init_db()
    user_name = session.get('name', None)
    current_user = session.get('user_id', None)
    if request.method == 'POST':
        name = request.form.get('name')
        item_group_new = ItemGroup(name, current_user)
        database.db_session.add(item_group_new)
        database.db_session.commit()
    item_groups_all = database.db_session.query(ItemGroup).\
        filter_by(user_id=current_user).order_by(ItemGroup.name).all()
    return render_template('item_groups_add.html', item_groups=item_groups_all, user=user_name)


@app.route('/items/', methods=['GET', 'POST'])
def item_add():
    database.init_db()
    user_name = session.get('name', None)
    current_user = session.get('user_id', None)
    if request.method == 'POST':
        item_name = request.form.get('name')
        item_code = request.form.get('code')
        item_group = request.form.get('group')
        item_description = request.form.get('description')
        item_new_add = Item(
            item_name,
            current_user,
            item_code,
            item_group,
            item_description
        )
        database.db_session.add(item_new_add)
        database.db_session.commit()
    items_groups_all = database.db_session.query(ItemGroup).\
        filter_by(user_id=current_user).order_by(ItemGroup.name).all()
    items_all = database.db_session.query(Item).filter_by(user_id=current_user).order_by(Item.name).all()
    return render_template('item_add.html', user=user_name, items_all=items_all, items_groups=items_groups_all)


@app.route('/items/<item_id>/', methods=['GET', 'POST'])
def item_edit(item_id):
    user_name = session.get('name', None)
    item = database.db_session.query(Item).filter_by(id=item_id).first()
    item_price = database.db_session.query(SellingPrice).filter_by(item_id=item_id).\
        order_by(desc(SellingPrice.date)).first()
    item_stock = database.db_session.query(Stock).filter_by(item_id=item_id).first()
    if request.method == "POST":
        item.name = request.form.get('name')
        item.item_code = request.form.get('code')
        item.item_group = request.form.get('group')
        item.description = request.form.get('description')
        database.db_session.commit()
    return render_template('item_edit.html', item=item, user=user_name, item_id=item_id,
                           price=item_price, stock=item_stock)


@app.route('/items/<item_id>/price/', methods=['GET', 'POST'])
def item_price_add(item_id):
    user_name = session.get('name', None)
    if request.method == 'POST':
        price = request.form.get('price')
        price_add = SellingPrice(price, item_id)
        database.db_session.add(price_add)
        database.db_session.commit()
        return redirect(url_for('item_edit', item_id=item_id))
    return render_template('price.html', user=user_name, item_id=item_id)


@app.route('/items/<item_id>/stock_add/', methods=['GET', 'POST'])
def item_stock_add(item_id):
    user_name = session.get('name', None)
    if request.method == 'POST':
        arrival_quantity = request.form.get('quantity')
        cost_price = request.form.get('cost_price')
        cost_price_add = CostPrice(cost_price, item_id)
        database.db_session.add(cost_price_add)
        database.db_session.commit()
        item_quantity_now = database.db_session.query(Stock).filter_by(item_id=item_id).first()
        if item_quantity_now is None:
            stock_add = Stock(arrival_quantity, item_id)
            database.db_session.add(stock_add)
            database.db_session.commit()
            return redirect(url_for('item_edit', item_id=item_id))
        else:
            item_quantity_after_arrival = item_quantity_now.stock + int(arrival_quantity)
            stock_add = Stock(item_quantity_after_arrival, item_id)
            database.db_session.add(stock_add)
            database.db_session.commit()
            return redirect(url_for('item_edit', item_id=item_id))
    return render_template('item_stock_add.html', user=user_name, item_id=item_id)


@app.route('/items/<item_id>/stock_decrease/', methods=['GET', 'POST'])
def item_stock_decrease(item_id):
    user_name = session.get('name')
    if request.method == 'POST':
        item_quantity_now = database.db_session.query(Stock).filter_by(item_id=item_id).first()
        if item_quantity_now is None:
            return render_template('not_enough_item.html', user=user_name, item_id=item_id)
        else:
            quantity = int(request.form.get('quantity'))
            if item_quantity_now.stock >= quantity:
                quantity_new = item_quantity_now.stock - quantity
                quantity_decrease = Stock(quantity_new, item_id)
                database.db_session.add(quantity_decrease)
                database.db_session.commit()
                return redirect(url_for('item_edit', item_id=item_id))
            else:
                return render_template('not_enough_item.html', user=user_name, item_id=item_id)
    return render_template('item_stock_decrease.html', user=user_name, item_id=item_id)


@app.route('/customers/', methods=['GET'])
def customers():
    user_name = session.get('name', None)
    current_user = session.get('user_id', None)
    customers_all = database.db_session.query(Customer).\
        filter_by(user_id=current_user).order_by(Customer.name).all()
    return render_template('customers.html', customers_all=customers_all, user=user_name)


@app.route('/customers/add/', methods=['POST', 'GET'])
def customer_add():
    current_user = session.get('user_id', None)
    user_name = session.get('name', None)
    if request.method == 'POST':
        customer_name = request.form.get('name')
        customer_phone = request.form.get('phone')
        customer_mail = request.form.get('mail')
        customer_add_new = Customer(customer_name, current_user, customer_phone, customer_mail)
        database.db_session.add(customer_add_new)
        database.db_session.commit()
        return redirect(url_for('customers'))
    return render_template('customer_add.html', user=user_name)


@app.route('/customers/<customer_id>/', methods=['POST', 'GET'])
def customer_edit(customer_id):
    user_name = session.get('name', None)
    customer_info = database.db_session.query(Customer).filter_by(id=customer_id).first()
    if request.method == 'POST':
        customer_info.name = request.form.get('name')
        customer_info.phone = request.form.get('phone')
        customer_info.mail = request.form.get('mail')
        database.db_session.commit()
    return render_template('customer_edit.html', customer=customer_info, customer_id=customer_id, user=user_name)


@app.route('/order_statuses/', methods=['GET', 'POST'])
def order_statuses_add():
    user_name = session.get('name', None)
    user_id = session.get('user_id', None)
    if request.method == 'POST':
        name = request.form.get('name')
        status_add = OrderStatus(name, user_id)
        database.db_session.add(status_add)
        database.db_session.commit()
    order_status_all = database.db_session.query(OrderStatus).filter_by(user_id=user_id).all()
    return render_template('order_statuses.html', user=user_name, statuses=order_status_all)


@app.route('/orders/', methods=['GET', 'POST'])
def order_add():
    return render_template('index.html')

@app.route('/orders/<order_id>/', methods=['GET', 'POST'])
def order_status_edit(order_id):
    return render_template('index.html')

@app.route('/report_sales_by_customers/', methods=['GET', 'POST'])
def report_sales_by_customers():
    return render_template('index.html')

@app.route('/report_sales_by_items/', methods=['GET', 'POST'])
def report_sales_by_items():
    return render_template('index.html')

@app.route('/report_gross_income/', methods=['GET', 'POST'])
def report_gross_income():
    return render_template('index.html')








if __name__ == '__main__':
    app.run()

