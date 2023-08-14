from app import app
from flask import render_template

@app.route('/')
@app.route('/test')
def test():
    title = 'test'
    return render_template('test.html')