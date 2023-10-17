from flask import Flask
from flask import Flask, render_template, redirect, url_for, session, flash, request


app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('index.html')






if __name__ == '__main__':
    app.run()

