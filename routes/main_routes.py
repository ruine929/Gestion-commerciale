from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from services.statistique_service import StatistiqueService
from services.alerte_service import AlerteService
from services.stock_service import StockService

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Page d'accueil : redirection selon l'état de connexion"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))

@main_bp.route('/login')
def login():
    """Page de connexion"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('login.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Tableau de bord principal"""
    try:
        # Données du tableau de bord
        dashboard_data = StatistiqueService.get_dashboard_data()

        # Alertes
        alertes = AlerteService.get_all_alerts()
        summary_alertes = AlerteService.get_alerts_summary()

        # Résumé du stock
        stock_summary = StockService.get_stock_summary()

        return render_template(
            'index.html',
            dashboard_data=dashboard_data,
            alertes=alertes[:5],  # Afficher seulement les 5 premières alertes
            summary_alertes=summary_alertes,
            stock_summary=stock_summary
        )
    except Exception as e:
        flash(f"Erreur lors du chargement du tableau de bord: {str(e)}", "error")
        return render_template(
            'index.html',
            dashboard_data={},
            alertes=[],
            summary_alertes={},
            stock_summary={}
        )

@main_bp.route('/about')
def about():
    """Page À propos"""
    return render_template(
        'base.html',
        content="À propos de l'application de gestion commerciale"
    )
