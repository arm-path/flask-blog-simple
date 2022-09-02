from flask import render_template

from app import app


@app.route('/')
def base_view():
    return render_template('base.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')
