# binmax

# Swipemax : Application de E-Commerce Ludique

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Application mobile/web inspirée de Tinder permettant de "swiper" des produits. Les produits "matchés" sont ajoutés au panier, avec gestion de stock et livraison via QR code.

---

## 📌 Fonctionnalités Principales

### 🛠 Backend (Django)

- **Gestion des produits** : CRUD, stock en temps réel.
- **Rôles utilisateurs** : Client, Livreur, Employé, Admin.
- **Algorithme de suggestion** basé sur les catégories préférées.
- **Paiement sécurisé** via Stripe.
- **Génération de QR code** pour les livraisons.

### 📱 Frontend Client (Flutter)

- **Swipe intuitif** (gauche/droite) pour découvrir des produits.
- **Panier dynamique** avec options de paiement.
- **Historique des commandes** et suivi de livraison.

### 🚚 Module Livraison (Livreur)

- **Scan de QR code** pour accéder aux détails des commandes.
- **Mise à jour en temps réel** du statut de livraison.

---

## 🛠 Architecture Technique

### Backend

- **Framework** : Django REST Framework
- **Base de données** : PostgreSQL
- **Services externes** : Stripe (paiement), Firebase/AWS S3 (stockage images), `qrcode` (Python).

### Frontend

- **Mobile** : Flutter (iOS/Android)
- **Web** : Dashboard Admin (Django)

### Sécurité

- Authentification JWT
- Chiffrement des données sensibles.

---

## 🚀 Installation

### Prérequis

- Python 3.9+, Flutter 3.0+, PostgreSQL, Node.js (pour CDN).
- Comptes Stripe, Firebase/AWS (clés API).

### Étapes

1. **Backend (Django)**

   ```bash
   git clone [repo_url]
   cd backend
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver

   🤝 Contribution
   Forkez le projet.
   ```

Créez une branche : git checkout -b feature/ma-fonctionnalite.

Committez vos changements.

Pushez : git push origin feature/ma-fonctionnalite.

Ouvrez une Pull Request.
