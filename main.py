from flask import Flask, render_template, redirect, url_for, session, flash, request



app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('index.html')


#Create new group product
@app.route('/product_groups/', method=['GET', 'POST'])
def product_group_add():
    return render_template('index.html')

# Create new and View products
@app.route('/products/', methods=['GET', 'POST'])
def product_add():
    return render_template('index.html')


# Edit product
@app.route('/products/<int: product_id>/', methods=['GET', 'POST'])
def product_edit():
    return render_template('index.html')


# Add to product new price
@app.route('/products/<int: product_id>/price', methods=['POST'])
def product_price_add():
    return render_template('index.html')

# Increase product stock
@app.route('/products/<int: product_id>/stock_add/', method=['POST'])
def product_stock_add():
    return render_template('index.html')


# Decrease product stock
@app.route('/products/<int: product_id>/stock_decrease/', method=['POST'])
def product_stock_decrease():
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

@app.route('/report_sales_by_products/', method=['GET', 'POST'])
def report_sales_by_products():
    return render_template('index.html')

@app.route('/report_gross_income/', method=['GET', 'POST'])
def report_gross_income():
    return render_template('index.html')








if __name__ == '__main__':
    app.debug = True
    app.run()

