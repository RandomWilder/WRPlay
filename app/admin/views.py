from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from flask_login import current_user
from flask import redirect, url_for, flash
from app.models import User, Raffle, Ticket
from app import db
from app.services.raffle_service import RaffleService

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        flash('You need to be an admin to access this page.', 'error')
        return redirect(url_for('main.index'))

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
            return redirect(url_for('main.index'))
        return super(MyAdminIndexView, self).index()

def init_admin_views(admin_manager):
    admin_manager.add_view(UserAdminView(User, db.session, name='Users', endpoint='flask_admin_users'))
    admin_manager.add_view(RaffleAdminView(Raffle, db.session, name='Raffles', endpoint='flask_admin_raffles'))
    admin_manager.add_view(TicketAdminView(Ticket, db.session, name='Tickets', endpoint='flask_admin_tickets'))