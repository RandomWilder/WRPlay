from flask import Blueprint, render_template
from app.services.raffle_service import RaffleService

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    active_raffles = RaffleService.get_active_raffles()
    return render_template('index.html', raffles=active_raffles)