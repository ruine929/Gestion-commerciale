from models.vente import Vente
from models.produit import Produit
from models.client import Client
from services.stock_service import StockService
from app import db
from datetime import datetime, timedelta
from sqlalchemy import func

class VenteService:
    """Service pour la gestion des ventes"""
    
    @staticmethod
    def create_vente(produit_id, client_id, quantite, prix_unitaire=None, remise=0.0, notes=None):
        """Crée une nouvelle vente"""
        produit = Produit.query.get(produit_id)
        client = Client.query.get(client_id)
        
        if not produit or not client:
            return None, "Produit ou client non trouvé"
        
        if produit.stock_actuel < quantite:
            return None, f"Stock insuffisant. Stock disponible: {produit.stock_actuel}"
        
        if prix_unitaire is None:
            prix_unitaire = produit.prix_vente
        
        vente = Vente(
            produit_id=produit_id,
            client_id=client_id,
            quantite=quantite,
            prix_unitaire=prix_unitaire,
            remise=remise,
            notes=notes
        )
        
        # Calculer le montant total via méthode du modèle
        vente.calculer_montant_total()
        
        try:
            db.session.add(vente)
            produit.stock_actuel -= quantite
            db.session.commit()
            return vente, "Vente créée avec succès"
        except Exception as e:
            db.session.rollback()
            return None, f"Erreur lors de la création de la vente: {str(e)}"
    
    @staticmethod
    def get_ventes_by_period(date_debut=None, date_fin=None):
        """Retourne les ventes pour une période donnée"""
        query = Vente.query
        if date_debut:
            query = query.filter(Vente.date_vente >= date_debut)
        if date_fin:
            query = query.filter(Vente.date_vente <= date_fin)
        return query.order_by(db.desc(Vente.date_vente)).all()
    
    @staticmethod
    def get_ventes_by_client(client_id):
        """Retourne les ventes d'un client"""
        return Vente.query.filter_by(client_id=client_id).order_by(db.desc(Vente.date_vente)).all()
    
    @staticmethod
    def get_ventes_by_product(produit_id):
        """Retourne les ventes d'un produit"""
        return Vente.query.filter_by(produit_id=produit_id).order_by(db.desc(Vente.date_vente)).all()
    
    @staticmethod
    def calculate_daily_sales(days=7):
        """Calcule les ventes quotidiennes sur les derniers jours"""
        date_debut = datetime.utcnow() - timedelta(days=days)
        ventes = Vente.query.filter(
            Vente.date_vente >= date_debut,
            Vente.statut == 'completed'
        ).all()
        
        sales_by_day = {
            (datetime.utcnow() - timedel
