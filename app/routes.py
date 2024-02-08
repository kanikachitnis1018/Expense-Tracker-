from app import app, db
from flask import render_template, flash, redirect, url_for, get_flashed_messages
from app.form import UserInputForm
from app.models import IncomeExpenses
import json

@app.route("/")
def index():
    entries = IncomeExpenses.query.order_by(IncomeExpenses.date.desc()).all()
    return render_template("index.html", title = 'index', entries = entries)

@app.route("/add", methods = ['GET', 'POST'])
def add_expenses():
    form = UserInputForm()
    if form.validate_on_submit():
        entry = IncomeExpenses(type = form.name.data, amount = form.amount.data, category = form.category.data)
        db.session.add(entry)
        db.session.commit()
        flash("Successful Entry", 'success')
        return redirect(url_for('index'))
    return render_template("add.html", title = 'add', form = form)

@app.route("/delete/<int:entry_id>")
def delete(entry_id):
    entry = IncomeExpenses.query.get_or_404(int(entry_id))
    db.session.delete(entry)
    flash("Deleted Successfully", 'success')
    return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    income_vs_expense = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.type).group_by(IncomeExpenses.type).order_by(IncomeExpenses.type).all()

    dates = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.date).group_by(IncomeExpenses.date).order_by(IncomeExpenses.date).all()

    income_expense = []
    for total_amount, _ in income_vs_expense:
        income_expense.append(total_amount)

    over_time = []
    date_labels = []
    for amount, date in dates:
        over_time.append(amount)
        date_labels.append(date.strftime("%m-%d-%Y"))

    return render_template("dashboard.html", income_vs_expense = json.dumps(income_expense),
                           over_time = json.dumps(over_time),
                           date_labels = json.dumps(date_labels))