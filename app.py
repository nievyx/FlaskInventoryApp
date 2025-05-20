from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///item.db'
db = SQLAlchemy(app)


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(200), nullable=False)
    buy_from = db.Column(db.String(200), nullable=False)
    seller_name = db.Column(db.String(200), nullable=False)
    seller_price = db.Column(db.Float, nullable=False)
    seller_shipping = db.Column(db.Float, nullable=False)
    selling_on = db.Column(db.String(200), nullable=False)
    my_price = db.Column(db.Float, nullable=False)
    my_shipping = db.Column(db.Float, nullable=False)


@app.route('/', methods=['GET'])
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)


@app.route('/', methods=["POST"])
def create():
    new_item = Item()
    for key, value in request.form.items():
        setattr(new_item, key, value)
    try:
        db.session.add(new_item)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return 'There was an issue adding you item: {}'.format(e)


# app route: update
@app.route('/update/<int:id>', methods=['GET'])
def edit(id):
    item = Item.query.get_or_404(id)
    return render_template('update.html', i=item)


@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    item = Item.query.get_or_404(id)

    for key, value in request.form.items():
        setattr(item, key, value)

    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue updating your item'


# app route= delete
@app.route('/delete/<int:id>')
def delete(id):
    deleted = Item.query.get_or_404(id)
    db.session.delete(deleted)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)