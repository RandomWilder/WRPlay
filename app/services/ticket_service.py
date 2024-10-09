from app import db
from app.models.ticket import Ticket
from app.models.raffle import Raffle

class TicketService:
    @staticmethod
    def purchase_tickets(user, raffle_id, quantity):
        raffle = Raffle.query.get(raffle_id)
        if not raffle or not raffle.is_active:
            return False, "This raffle is not available"

        available_tickets = Ticket.query.filter_by(raffle_id=raffle_id, is_sold=False).count()
        if available_tickets < quantity:
            return False, "Not enough tickets available"

        total_price = raffle.ticket_price * quantity
        if user.balance < total_price:
            return False, "Insufficient balance"

        user.balance -= total_price
        purchased_tickets = Ticket.query.filter_by(raffle_id=raffle_id, is_sold=False).limit(quantity).all()
        for ticket in purchased_tickets:
            ticket.is_sold = True
            ticket.user_id = user.id

        db.session.commit()
        return True, f"Successfully purchased {quantity} ticket(s)"

    @staticmethod
    def get_user_tickets(user):
        return Ticket.query.filter_by(user_id=user.id).all()