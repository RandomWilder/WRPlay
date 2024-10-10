from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.services.raffle_service import RaffleService
from app.services.ticket_service import TicketService
from app.services.user_service import UserService

bp = Blueprint('raffle', __name__)

@bp.route('/raffles')
def list_raffles():
    raffles = RaffleService.get_active_raffles()
    return render_template('raffle/list.html', raffles=raffles)

@bp.route('/raffle/<int:raffle_id>')
def raffle_detail(raffle_id):
    raffle = RaffleService.get_raffle_by_id(raffle_id)
    if not raffle:
        flash('Raffle not found', 'error')
        return redirect(url_for('raffle.list_raffles'))
    available_tickets = RaffleService.get_available_tickets(raffle_id)
    return render_template('raffle/detail.html', raffle=raffle, available_tickets=available_tickets)

@bp.route('/raffle/<int:raffle_id>/buy', methods=['POST'])
@login_required
def buy_ticket(raffle_id):
    quantity = int(request.form.get('quantity', 1))
    success, message = TicketService.purchase_tickets(current_user.id, raffle_id, quantity)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    return redirect(url_for('raffle.raffle_detail', raffle_id=raffle_id))

@bp.route('/my-tickets')
@login_required
def my_tickets():
    tickets = TicketService.get_user_tickets(current_user.id)
    user_balance = UserService.get_user_balance(current_user.id)
    return render_template('raffle/my_tickets.html', tickets=tickets, balance=user_balance)

@bp.route('/add-funds', methods=['POST'])
@login_required
def add_funds():
    amount = float(request.form.get('amount', 0))
    if amount <= 0:
        flash('Invalid amount', 'error')
    else:
        success = UserService.update_user_balance(current_user.id, amount)
        if success:
            flash(f'Successfully added ${amount:.2f} to your balance', 'success')
        else:
            flash('Failed to add funds', 'error')
    return redirect(url_for('raffle.my_tickets'))