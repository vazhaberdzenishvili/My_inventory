from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_paginate import get_page_parameter, Pagination

from app import db
from app.models.store import StoreModel
from app.data.pages_resource import pages
from flask_user import current_user

store_blueprint = Blueprint('StoreModel',
                            __name__,
                            template_folder='templates/store'
                            )


@store_blueprint.route('/store', methods=['GET', 'POST'])
def store():
    ROWS_PER_PAGE = 5
    page = request.args.get('page', 1, type=int)
    if current_user.is_authenticated:
        if request.method == 'POST':
            item_name = request.form['name']
            if item_name:
                data = StoreModel.query.filter_by(name=item_name)
                items = data.paginate(page=page, per_page=ROWS_PER_PAGE)
                return render_template('store.html', items=items)
            else:
                items = StoreModel.query.paginate(page=page, per_page=ROWS_PER_PAGE)
                return render_template('store.html', items=items)
        items = StoreModel.query.paginate(page=page, per_page=ROWS_PER_PAGE)
        return render_template('store.html', items=items)

    flash("გთხოვთ გაიაროთ ავტორიზაცია.")
    return redirect(url_for('UserModel.login'))


@store_blueprint.route('/add', methods=['GET', 'POST'])
def Store_add():
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']
    item = StoreModel(name, price, quantity)
    if StoreModel.find_by_name(name) is None:
        item.add_item()
        flash(f" ნივთი {name} წარმატებით დაემატა ბაზაში", 'success')
        return redirect(url_for('StoreModel.store'))
    else:
        flash(F"პროდუქტი {name} დასახელებით უკვე არსებობს ", 'error')
        return redirect(url_for('StoreModel.store'))


@store_blueprint.route('/delete/<id>/', methods=['GET', 'POST'])
def store_delete(id):
    item = StoreModel.query.get(id)
    item.delete_item()
    flash("პროდუქტი  წარმატებით წაიშალა ბაზიდან", 'success')

    return redirect(url_for('StoreModel.store'))


@store_blueprint.route('/update', methods=['GET', 'POST'])
def store_edit():
    if request.method == 'POST':
        item_data = StoreModel.query.get(request.form.get('id'))
        item_data.name = request.form['name']
        item_data.price = request.form['price']
        item_data.quantity = request.form['quantity']
        db.session.commit()
        flash(f"პროდუქტი  {item_data.name}  წარმატებით განახლდა", 'success')
        return redirect(url_for('StoreModel.store'))
