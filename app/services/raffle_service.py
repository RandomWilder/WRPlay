from app import db
from app.models.raffle import Raffle
from app.models.ticket import Ticket
from datetime import datetime

class RaffleService:
    @staticmethod
    def create_raffle(name, description, ticket_price, total_tickets, draw_date):
        raffle = Raffle(
            name=name,
            description=description,
            ticket_price=ticket_price,
            total_tickets=total_tickets,
            draw_date=draw_date,
            is_active=True
        )
        db.session.add(raffle)
        db.session.flush()  # This assigns an ID to the raffle

        # Create tickets for the raffle
        tickets = [Ticket(raffle_id=raffle.id, ticket_number=i+1) for i in range(total_tickets)]
        db.session.bulk_save_objects(tickets)
        
        db.session.commit()
        return raffle

    @staticmethod
    def get_raffle_by_id(raffle_id):
        return Raffle.query.get(raffle_id)

    @staticmethod
    def get_active_raffles():
        return Raffle.query.filter_by(is_active=True).all()

    @staticmethod
    def get_all_raffles():
        return Raffle.query.all()

    @staticmethod
    def close_raffle(raffle_id):
        raffle = Raffle.query.get(raffle_id)
        if raffle and raffle.is_active:
            raffle.is_active = False
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_available_tickets(raffle_id):
        return Ticket.query.filter_by(raffle_id=raffle_id, user_id=None).count()