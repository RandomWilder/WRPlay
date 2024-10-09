from flask_admin.contrib.sqla import ModelView
from app.models import User, Raffle, Ticket
from app import db

class UserAdminView(ModelView):
    column_exclude_list = ['password_hash']

class RaffleAdminView(ModelView):
    column_list = ['id', 'name', 'total_tickets', 'ticket_price', 'draw_date', 'is_active']

class TicketAdminView(ModelView):
    column_list = ['id', 'raffle', 'user', 'purchase_date', 'is_winner']

def init_admin_views(admin_manager):
    admin_manager.add_view(UserAdminView(User, db.session, name='Users', endpoint='admin_users'))
    admin_manager.add_view(RaffleAdminView(Raffle, db.session, name='Raffles', endpoint='admin_raffles'))
    admin_manager.add_view(TicketAdminView(Ticket, db.session, name='Tickets', endpoint='admin_tickets'))