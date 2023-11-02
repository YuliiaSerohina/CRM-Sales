from flask import Flask, render_template, redirect, url_for, session, flash, request
import database
from models import User, Customer, Item, ItemGroup, Order, OrderItem, Stock, SellingPrice, CostPrice, OrderStatus
from flask_session import Session

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
            flash('Unknown username')
            return redirect(url_for('login'))
        else:
            session['user_id'] = find_user.id
            session['name'] = find_user.name
            return redirect(url_for('user_database', user=find_user.name))
    return render_template('login.html')


@app.route('/crm/', methods=['GET', 'POST'])
def user_database():
    return render_template('crm.html')





@app.route('/item_groups/', methods=['GET', 'POST'])
def item_group_add():
    return render_template('index.html')

# Create new and View products
@app.route('/items/', methods=['GET', 'POST'])
def item_add():
    return render_template('index.html')


# Edit product
@app.route('/items/<int:item_id>/', methods=['GET', 'POST'])
def item_edit():
    return render_template('index.html')


# Add to product new price
@app.route('/items/<int:item_id>/price', methods=['POST'])
def item_price_add():
    return render_template('index.html')

# Increase product stock
@app.route('/items/<int:items_id>/stock_add/', methods=['POST'])
def item_stock_add():
    return render_template('index.html')


# Decrease product stock
@app.route('/items/<int:item_id>/stock_decrease/', methods=['POST'])
def item_stock_decrease():
    return render_template('index.html')

#Create a new customer and view customer
@app.route('/customers/', methods=['GET, POST'])
def customer_add():
    return render_template('index.html')

# Create a new order status and view
@app.route('/order_statuses/',methods=['GET, POST'])
def order_statuses_add():
    return render_template('index.html')


@app.route('/orders/', methods=['GET, POST'])
def order_add():
    return render_template('index.html')

@app.route('/orders/<int:order_id>/', methods=['GET, POST'])
def order_status_edit():
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

