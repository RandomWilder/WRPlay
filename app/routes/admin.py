from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user
from app.models.user import User
from app.services.raffle_service import RaffleService
from app.services.ticket_service import TicketService
from datetime import datetime
from functools import wraps

admin_bp = Blueprint('custom_admin', __name__, url_prefix='/custom_admin')

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('You do not have permission to access this page.')
            return redirect(url_for('custom_admin.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('custom_admin.admin_panel'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, is_admin=True).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('custom_admin.admin_panel'))
        flash('Invalid admin credentials')
    return render_template('admin/login.html')

@admin_bp.route('/')
@admin_required
def admin_panel():
    return render_template('admin/panel.html')

@admin_bp.route('/create_raffle', methods=['GET', 'POST'])
@admin_required
def create_raffle():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        total_tickets = int(request.form['total_tickets'])
        ticket_price = float(request.form['ticket_price'])
        draw_time = datetime.fromisoformat(request.form['draw_time'])
        
        RaffleService.create_raffle(name, description, ticket_price, total_tickets, draw_time)
        flash('New raffle created successfully')
        return redirect(url_for('custom_admin.admin_raffles'))
    
    return render_template('admin/create_raffle.html')

@admin_bp.route('/raffles')
@admin_required
def admin_raffles():
    raffles = RaffleService.get_all_raffles()
    return render_template('admin/raffles.html', raffles=raffles)

@admin_bp.route('/raffle/<int:raffle_id>/close', methods=['POST'])
@admin_required
def close_raffle(raffle_id):
    if RaffleService.close_raffle(raffle_id):
        success, message = TicketService.mark_winning_ticket(raffle_id)
        if success:
            flash(f'Raffle closed and {message}', 'success')
        else:
            flash(f'Raffle closed but failed to draw winner: {message}', 'warning')
    else:
        flash('Failed to close raffle', 'error')
    return redirect(url_for('custom_admin.admin_raffles'))

@admin_bp.route('/tickets')
@admin_required
def admin_tickets():
    tickets = TicketService.get_all_tickets()
    return render_template('admin/tickets.html', tickets=tickets)