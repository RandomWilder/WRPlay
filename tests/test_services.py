import unittest
from app import create_app, db
from app.models.user import User
from app.models.raffle import Raffle
from app.models.ticket import Ticket
from app.services.raffle_service import RaffleService
from app.services.ticket_service import TicketService
from datetime import datetime, timedelta

class TestServices(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_raffle(self):
        raffle = RaffleService.create_raffle(100, 1, datetime.utcnow() + timedelta(days=1), 10.0)
        self.assertIsNotNone(raffle.id)
        self.assertEqual(raffle.total_tickets, 100)
        self.assertEqual(Ticket.query.filter_by(raffle_id=raffle.id).count(), 100)

    def test_purchase_tickets(self):
        user = User(username='testuser', balance=100.0)
        db.session.add(user)
        raffle = RaffleService.create_raffle(100, 1, datetime.utcnow() + timedelta(days=1), 10.0)
        db.session.commit()

        success, message = TicketService.purchase_tickets(user, raffle.id, 2)
        self.assertTrue(success)
        self.assertEqual(user.balance, 80.0)
        self.assertEqual(Ticket.query.filter_by(raffle_id=raffle.id, is_sold=True).count(), 2)

    def test_conduct_raffle_draw(self):
        raffle = RaffleService.create_raffle(100, 1, datetime.utcnow() - timedelta(days=1), 10.0)
        user = User(username='testuser', balance=100.0)
        db.session.add(user)
        db.session.commit()

        TicketService.purchase_tickets(user, raffle.id, 1)
        winning_tickets = RaffleService.conduct_raffle_draw(raffle.id)

        self.assertEqual(len(winning_tickets), 1)
        self.assertTrue(winning_tickets[0].is_winner)
        self.assertFalse(raffle.is_active)

if __name__ == '__main__':
    unittest.main()