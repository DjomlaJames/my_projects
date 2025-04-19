from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from .models import Expense, Income
from . import db
from datetime import datetime
from .config import CURRENCY_CONVERSION

edit = Blueprint('edit', __name__)


@edit.route('/show-edit-expense/<int:expense_id>', methods=['GET'])
@login_required
def show_edit_expense(expense_id):
    expense = Expense.query.get(expense_id)
    if not expense or expense.user_id != current_user.id:
        flash('Expense not found or you are not authorized to edit it.', category='error')
        return redirect(url_for('views.all_entries'))

    return render_template('edit/edit_expense.html', expense=expense)



@edit.route('/show-edit-income/<int:income_id>', methods=['GET'])
def show_edit_income(income_id):
    income = Income.query.get(income_id)
    if not income or income.user_id != current_user.id:
        flash('Income not found or you are not authorized to edit it.', category='error')
        return redirect(url_for('views.all_entries'))

    return render_template('edit/edit_income.html', income=income)
