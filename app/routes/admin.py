from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.services.raffle_service import RaffleService
from datetime import datetime

admin_bp = Blueprint('admin_routes', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.')
        return redirect(url_for('main.index'))
    return render_template('admin/panel.html')

@admin_bp.route('/create_raffle', methods=['GET', 'POST'])
@login_required
def create_raffle():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        name = request.form['name']
        total_tickets = int(request.form['total_tickets'])
        winning_tickets = int(request.form['winning_tickets'])
        ticket_price = float(request.form['ticket_price'])
        draw_time = datetime.fromisoformat(request.form['draw_time'])
        
        RaffleService.create_raffle(name, total_tickets, winning_tickets, draw_time, ticket_price)
        flash('New raffle created successfully')
        return redirect(url_for('admin_routes.admin_raffles'))
    
    return render_template('admin/create_raffle.html')

@admin_bp.route('/raffles')
@login_required
def admin_raffles():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.')
        return redirect(url_for('main.index'))

    raffles = RaffleService.get_all_raffles()
    return render_template('admin/raffles.html', raffles=raffles)