from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.services.raffle_service import RaffleService
from app.services.ticket_service import TicketService

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
    return render_template('raffle/detail.html', raffle=raffle)

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
    return render_template('raffle/my_tickets.html', tickets=tickets)