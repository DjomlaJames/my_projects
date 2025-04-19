from flask import Blueprint, render_template, request, flash, jsonify,redirect, url_for
from flask_login import login_required, current_user
from .models import Expense, Income
from . import db
import json
from datetime import datetime,timedelta
from flask import jsonify

views = Blueprint('views', __name__)



@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        expense_amount = float(request.form.get('expenseAmount', 0))
        expense_currency = request.form.get('expenseCurrency')
        expense_type = request.form.get('expenseType')

        income_amount = float(request.form.get('incomeAmount', 0))
        income_currency = request.form.get('incomeCurrency')
        income_type = request.form.get('incomeType')

        if expense_amount > 0 and expense_currency and expense_type:
            new_expense = Expense(amount=expense_amount, currency=expense_currency, expense_type=expense_type,
                                  user_id=current_user.id,date_created=datetime.utcnow())
            db.session.add(new_expense)
            db.session.commit()
            flash('Expense entry added successfully!', category='success')
            print('Expense entry added successfully!')
        if income_amount > 0 and income_currency and income_type:
            new_income = Income(amount=income_amount, currency=income_currency, income_type=income_type,
                                user_id=current_user.id,date_created=datetime.utcnow())
            db.session.add(new_income)
            db.session.commit()
            flash('Income entry added successfully!', category='success')
            print('Income entry added successfully!')

    return render_template("home.html", user=current_user)


@views.route('/delete-entry', methods=['POST'])
def delete_entry():  # Promenjeno ime rute i funkcije za brisanje
    entry = json.loads(request.data)
    entry_id = entry['entryId']

    # Treba prilagoditi pretragu i brisanje za Expense i Income
    expense = Expense.query.get(entry_id)
    income = Income.query.get(entry_id)

    if expense and expense.user_id == current_user.id:
        db.session.delete(expense)
        db.session.commit()

    if income and income.user_id == current_user.id:
        db.session.delete(income)
        db.session.commit()

    return jsonify({})

@views.route('/all-entries')
@login_required
def all_entries():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    incomes = Income.query.filter_by(user_id=current_user.id).all()
    editing_entry_id = request.args.get('editing_entry_id')
    if editing_entry_id is None:
        editing_entry_id = None

    return render_template("all_entries.html", user=current_user, expenses=expenses, incomes=incomes, editing_entry_id=editing_entry_id)
@views.route('/delete-expense', methods=['POST'])
def delete_expense():
    entry = json.loads(request.data)
    entry_id = entry['entryId']
    expense = Expense.query.get(entry_id)

    if expense:
        if expense.user_id == current_user.id:
            db.session.delete(expense)
            db.session.commit()

    return jsonify({})


@views.route('/delete-income', methods=['POST'])
def delete_income():
    entry = json.loads(request.data)
    entry_id = entry['entryId']
    income = Income.query.get(entry_id)

    if income:
        if income.user_id == current_user.id:
            db.session.delete(income)
            db.session.commit()

    return jsonify({})


@views.route('/edit-expense/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.get(expense_id)
    if not expense or expense.user_id != current_user.id:
        return jsonify({"message": "Expense not found or unauthorized."}), 403

    if request.method == 'POST':
        try:
            data = request.json
            new_amount = float(data['amount'])
            new_currency = data['currency']
            new_expense_type = data['expenseType']
            new_date = datetime.strptime(data['date'], '%Y-%m-%dT%H:%M')

            if not (new_amount and new_currency and new_expense_type and new_date):
                raise ValueError("All fields are required!")

            expense.amount = new_amount
            expense.currency = new_currency
            expense.expense_type = new_expense_type
            expense.date_created = new_date

            db.session.commit()
            return jsonify({"message": "Expense entry updated successfully!"}), 200
        except ValueError as e:
            return jsonify({"message": str(e)}), 400

    return render_template('edit/edit_expense.html', expense=expense, user=current_user)


@views.route('/edit-income/<int:income_id>', methods=['GET', 'POST'])
@login_required
def edit_income(income_id):
    income = Income.query.get(income_id)

    if not income or income.user_id != current_user.id:
        return jsonify({"message": "Income not found or unauthorized."}), 403

    if request.method == 'POST':
        try:
            data = request.json
            new_amount = float(data['amount'])
            new_currency = data['currency']
            new_income_type = data['incomeType']
            new_date = datetime.strptime(data['date'], '%Y-%m-%dT%H:%M')

            if not (new_amount and new_currency and new_income_type and new_date):
                raise ValueError("All fields are required!")

            income.amount = new_amount
            income.currency = new_currency
            income.income_type = new_income_type
            income.date_created = new_date

            db.session.commit()
            return jsonify({"message": "Income entry updated successfully!"}), 200
        except ValueError as e:
            return jsonify({"message": str(e)}), 400

    return render_template('edit/edit_income.html', income=income, user=current_user)


@views.route('/get-expense/<int:expense_id>', methods=['GET'])
@login_required
def get_expense(expense_id):
    expense = Expense.query.get(expense_id)
    if expense and expense.user_id == current_user.id:
        return jsonify({
            'id': expense.id,
            'amount': expense.amount,
            'currency': expense.currency,
            'expense_type': expense.expense_type,
            'date_created': expense.date_created.strftime('%Y-%m-%dT%H:%M')
        })
    return jsonify({}), 404  # Trošak nije pronađen ili nije ovlašćen za pristup

@views.route('/get-income/<int:income_id>', methods=['GET'])
@login_required
def get_income(income_id):
    income = Income.query.get(income_id)
    if income and income.user_id == current_user.id:
        return jsonify({
            'id': income.id,
            'amount': income.amount,
            'currency': income.currency,
            'income_type': income.income_type,
            'date_created': income.date_created.strftime('%Y-%m-%dT%H:%M')
        })
    return jsonify({}), 404



@views.route('/statistics', methods=['GET'])
@login_required
def statistics():
    usd_to_eur = 0.85  # konverzija dolara u eure
    gbp_to_eur = 1.17  # konverzija funti u eure

    user_expenses = Expense.query.filter_by(user_id=current_user.id).all()
    user_incomes = Income.query.filter_by(user_id=current_user.id).all()

    total_entertainment = total_bills = total_groceries = total_expenses = 0
    total_job = total_side_hustle = total_gift = total_incomes = 0

    # Sabirajte rashode
    for expense in user_expenses:
        amount_in_eur = expense.amount
        if expense.currency == 'USD':
            amount_in_eur = expense.amount * usd_to_eur
        elif expense.currency == 'GBP':
            amount_in_eur = expense.amount * gbp_to_eur

        total_expenses += amount_in_eur  # Dodavanje na ukupni rashod

        if expense.expense_type == 'Entertainment':
            total_entertainment += amount_in_eur
        elif expense.expense_type == 'Bills':
            total_bills += amount_in_eur
        elif expense.expense_type == 'Groceries':
            total_groceries += amount_in_eur

    # Sabirajte prihode
    for income in user_incomes:
        amount_in_eur = income.amount
        if income.currency == 'USD':
            amount_in_eur = income.amount * usd_to_eur
        elif income.currency == 'GBP':
            amount_in_eur = income.amount * gbp_to_eur

        total_incomes += amount_in_eur  # Dodavanje na ukupni prihod

        if income.income_type == 'Job':
            total_job += amount_in_eur
        elif income.income_type == 'Side_hustle':
            total_side_hustle += amount_in_eur
        elif income.income_type == 'Gift':
            total_gift += amount_in_eur

    total = {
        'expenses': total_expenses,
        'incomes': total_incomes
    }

    return render_template(
        'statistics.html',
        user=current_user,
        entertainment=total_entertainment,
        bills=total_bills,
        groceries=total_groceries,
        job=total_job,
        side_hustle=total_side_hustle,
        gift=total_gift,
        total_expenses=total_expenses,  # Prosleđivanje ukupnih rashoda u template
        total_incomes=total_incomes, # Prosleđivanje ukupnih prihoda u template
        total = total  # Dodavanje ukupnih vrednosti
    )

@views.route('/get-data/', methods=['GET'])
@login_required
def get_data():
    try:
        period = request.args.get('period', 'monthly')
        now = datetime.now()

        if period == 'weekly':
            start_date = now - timedelta(weeks=1)
        elif period == 'monthly':
            start_date = now - timedelta(days=30)
        elif period == 'yearly':
            start_date = now - timedelta(days=365)
        elif period == 'all':
            start_date = datetime(1900, 1, 1)
        else:
            return jsonify(error='Invalid period'), 400

        user_expenses = Expense.query.filter(
            Expense.user_id == current_user.id,
            Expense.date_created.between(start_date, now)
        ).all()
        for u in user_expenses:
            print(u.amount)
            print(u.expense_type)
        user_incomes = Income.query.filter(
            Income.user_id == current_user.id,
            Income.date_created.between(start_date, now)
        ).all()
        for u in user_incomes:
            print(u.amount)
            print(u.income_type)

        total_entertainment = 0
        total_bills = 0
        total_groceries = 0
        total_job = 0
        total_side_hustle =0
        total_gift = 0

        for expense in user_expenses:

            if expense.expense_type == 'Entertainment':
                total_entertainment += expense.amount
            elif expense.expense_type == 'Bills':
                total_bills += expense.amount
            elif expense.expense_type == 'Groceries':
                total_groceries += expense.amount
            else:
                 return jsonify(error='Invalid expenses'), 400
        print(str(total_entertainment)+"kkk")
        for income in user_incomes:
            print(income.amount)
            if income.income_type == 'Job':
                total_job += income.amount
            elif income.income_type == 'Side_hustle':
                total_side_hustle += income.amount
            elif income.income_type == 'Gift':
                total_gift += income.amount
            else:
                 return jsonify(error='Invalid incomes'), 400
        print(str(income.amount)+"kkk")

        return jsonify(
            incomes={
                'job': total_job,
                'side_hustle': total_side_hustle,
                'gift': total_gift
            },
            expenses={
                'entertainment': total_entertainment,
                'bills': total_bills,
                'groceries': total_groceries
            }

        )

    except Exception as e:
        # Ispisivanje informacija o grešci i vraćanje odgovora sa greškom
        print(e)
        traceback.print_exc()
        return jsonify(error='Internal Server Error'), 500