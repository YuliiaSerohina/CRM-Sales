from flask import Flask, render_template, redirect, url_for, session, flash, request
import database
from models import User, Customer, Item, ItemGroup, Order, OrderItem, Stock, SellingPrice, CostPrice, OrderStatus
from flask_session import Session

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('index.html')


#Create new group product
@app.route('/item_groups/', method=['GET', 'POST'])
def item_group_add():
    return render_template('index.html')

# Create new and View products
@app.route('/items/', methods=['GET', 'POST'])
def item_add():
    return render_template('index.html')


# Edit product
@app.route('/items/<int: item_id>/', methods=['GET', 'POST'])
def item_edit():
    return render_template('index.html')


# Add to product new price
@app.route('/items/<int: item_id>/price', methods=['POST'])
def item_price_add():
    return render_template('index.html')

# Increase product stock
@app.route('/items/<int: items_id>/stock_add/', method=['POST'])
def item_stock_add():
    return render_template('index.html')


# Decrease product stock
@app.route('/items/<int: item_id>/stock_decrease/', method=['POST'])
def item_stock_decrease():
    return render_template('index.html')

#Create a new customer and view customer
@app.route('/customers/', method=['GET, POST'])
def customer_add():
    return render_template('index.html')

# Create a new order status and view
@app.route('/order_statuses/',method=['GET, POST'])
def order_statuses_add():
    return render_template('index.html')


@app.route('/orders/', method=['GET, POST'])
def order_add():
    return render_template('index.html')

@app.route('/orders/<int: order_id>/', method=['GET, POST'])
def order_status_edit():
    return render_template('index.html')

@app.route('/report_sales_by_customers/', method=['GET', 'POST'])
def report_sales_by_customers():
    return render_template('index.html')

@app.route('/report_sales_by_items/', method=['GET', 'POST'])
def report_sales_by_items():
    return render_template('index.html')

@app.route('/report_gross_income/', method=['GET', 'POST'])
def report_gross_income():
    return render_template('index.html')








if __name__ == '__main__':
    app.debug = True
    app.run()

