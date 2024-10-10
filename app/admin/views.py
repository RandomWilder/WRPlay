from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose, Admin
from flask_login import current_user, login_required, login_user
from flask import redirect, url_for, flash, request, Blueprint, render_template
from app.models import User, Raffle, Ticket
from app import db
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

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        flash('You need to be an admin to access this page.', 'error')
        return redirect(url_for('custom_admin.admin_login'))

class UserAdminView(SecureModelView):
    column_exclude_list = ['password_hash']
    column_list = ['id', 'username', 'is_admin', 'balance']
    form_columns = ['username', 'is_admin', 'balance']
    
    def on_model_change(self, form, model, is_created):
        if is_created:
            model.set_password('default_password')  # Set a default password for new users

class RaffleAdminView(SecureModelView):
    column_list = ['id', 'name', 'ticket_price', 'total_tickets', 'draw_date', 'is_active']
    form_columns = ['name', 'description', 'ticket_price', 'total_tickets', 'draw_date', 'is_active']

    def on_model_change(self, form, model, is_created):
        if is_created:
            RaffleService.create_raffle(
                model.name,
                model.description,
                model.ticket_price,
                model.total_tickets,
                model.draw_date
            )
            return False  # Prevent the default creation process

class TicketAdminView(SecureModelView):
    column_list = ['id', 'raffle', 'user', 'purchase_date', 'is_winner']

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You need to be an admin to access this page.', 'error')
            return redirect(url_for('custom_admin.admin_login'))
        return super(MyAdminIndexView, self).index()

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
        description = request.form.get('description', '')  # Use get() with a default value
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

def init_admin_views(admin_manager):
    admin_manager.add_view(UserAdminView(User, db.session, name='Users', endpoint='admin_users'))
    admin_manager.add_view(RaffleAdminView(Raffle, db.session, name='Raffles', endpoint='admin_raffles'))
    admin_manager.add_view(TicketAdminView(Ticket, db.session, name='Tickets', endpoint='admin_tickets'))