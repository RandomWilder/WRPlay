import unittest
from app import create_app, db
from app.models import User, Raffle, Ticket
from config import TestConfig

class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_model(self):
        user = User(username='testuser')
        user.set_password('testpass')
        db.session.add(user)
        db.session.commit()
        self.assertIsNotNone(user.id)
        self.assertTrue(user.check_password('testpass'))
        self.assertFalse(user.check_password('wrongpass'))

    def test_raffle_model(self):
        raffle = Raffle(name='Test Raffle', total_tickets=100, ticket_price=10.0, draw_date='2023-12-31')
        db.session.add(raffle)
        db.session.commit()
        self.assertIsNotNone(raffle.id)
        self.assertEqual(raffle.name, 'Test Raffle')
        self.assertTrue(raffle.is_active)

    def test_ticket_model(self):
        user = User(username='testuser')
        raffle = Raffle(name='Test Raffle', total_tickets=100, ticket_price=10.0, draw_date='2023-12-31')
        db.session.add_all([user, raffle])
        db.session.commit()

        ticket = Ticket(raffle_id=raffle.id, user_id=user.id)
        db.session.add(ticket)
        db.session.commit()

        self.assertIsNotNone(ticket.id)
        self.assertEqual(ticket.raffle, raffle)
        self.assertEqual(ticket.user, user)
        self.assertFalse(ticket.is_winner)

if __name__ == '__main__':
    unittest.main()