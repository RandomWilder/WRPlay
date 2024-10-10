from app import db
from app.models.ticket import Ticket
from app.models.raffle import Raffle
from app.models.user import User
import random

class TicketService:
    @staticmethod
    def purchase_tickets(user_id, raffle_id, quantity):
        user = User.query.get(user_id)
        raffle = Raffle.query.get(raffle_id)
        
        if not user or not raffle:
            return False, "User or raffle not found"
        
        if not raffle.is_active:
            return False, "This raffle is not active"

        available_tickets = Ticket.query.filter_by(raffle_id=raffle_id, user_id=None).count()
        if available_tickets < quantity:
            return False, f"Only {available_tickets} tickets available"

        total_price = raffle.ticket_price * quantity
        if user.balance < total_price:
            return False, "Insufficient balance"

        if user.deduct_funds(total_price):
            available_tickets = Ticket.query.filter_by(raffle_id=raffle_id, user_id=None).all()
            selected_tickets = random.sample(available_tickets, quantity)

            for ticket in selected_tickets:
                ticket.user_id = user.id
                ticket.purchase_date = db.func.current_timestamp()

            db.session.commit()
            return True, f"Successfully purchased {quantity} ticket(s)"
        else:
            return False, "Failed to deduct funds"

    @staticmethod
    def get_user_tickets(user_id):
        return Ticket.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_raffle_tickets(raffle_id):
        return Ticket.query.filter_by(raffle_id=raffle_id).all()

    @staticmethod
    def get_all_tickets():
        return Ticket.query.all()

    @staticmethod
    def mark_winning_ticket(raffle_id):
        raffle = Raffle.query.get(raffle_id)
        if not raffle or raffle.is_active:
            return False, "Raffle not found or still active"

        tickets = Ticket.query.filter(Ticket.raffle_id == raffle_id, Ticket.user_id != None).all()
        if not tickets:
            return False, "No tickets sold for this raffle"

        winning_ticket = random.choice(tickets)
        winning_ticket.is_winner = True
        db.session.commit()

        return True, f"Ticket {winning_ticket.ticket_number} is the winner"