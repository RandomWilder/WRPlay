from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Raffle
from app import db
from datetime import datetime

bp = Blueprint('admin_routes', __name__, url_prefix='/admin')  # Changed the name to 'admin_routes'

@bp.route('/')
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash('You do not have permission to access this page')
        return redirect(url_for('main.index'))
    raffles = Raffle.query.all()
    return render_template('admin/panel.html', raffles=raffles)

@bp.route('/create_raffle', methods=['GET', 'POST'])
@login_required
def create_raffle():
    if not current_user.is_admin:
        flash('You do not have permission to access this page')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        name = request.form['name']
        total_tickets = int(request.form['total_tickets'])
        ticket_price = float(request.form['ticket_price'])
        draw_date = datetime.strptime(request.form['draw_date'], '%Y-%m-%d')
        
        raffle = Raffle(name=name, total_tickets=total_tickets, ticket_price=ticket_price, draw_date=draw_date)
        db.session.add(raffle)
        db.session.commit()
        flash('Raffle created successfully')
        return redirect(url_for('admin_routes.admin_panel'))
    
    return render_template('admin/create_raffle.html')