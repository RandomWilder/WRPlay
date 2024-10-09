from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Raffle, Ticket
from app import db

bp = Blueprint('raffle', __name__)

@bp.route('/raffle/<int:raffle_id>')
def raffle_detail(raffle_id):
    raffle = Raffle.query.get_or_404(raffle_id)
    return render_template('raffle_detail.html', raffle=raffle)

@bp.route('/raffle/<int:raffle_id>/buy', methods=['POST'])
@login_required
def buy_ticket(raffle_id):
    raffle = Raffle.query.get_or_404(raffle_id)
    if not raffle.is_active:
        flash('This raffle is no longer active')
        return redirect(url_for('raffle.raffle_detail', raffle_id=raffle_id))
    
    ticket = Ticket(raffle_id=raffle.id, user_id=current_user.id)
    db.session.add(ticket)
    db.session.commit()
    flash('Ticket purchased successfully')
    return redirect(url_for('raffle.raffle_detail', raffle_id=raffle_id))