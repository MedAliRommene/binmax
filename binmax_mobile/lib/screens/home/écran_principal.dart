import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:google_fonts/google_fonts.dart';

class EcranPrincipal extends StatefulWidget {
  const EcranPrincipal({super.key});

  @override
  _EcranPrincipalState createState() => _EcranPrincipalState();
}

class _EcranPrincipalState extends State<EcranPrincipal> {
  int _indexCategorie = 0;
  final List<String> _categories = ['Électronique', 'Mode', 'Maison', 'Beauté'];
  int _currentIndex = 0;

  void _handleSearch() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Recherche non implémentée')),
    );
  }

  void _handleMenuItem(String title) {
    if (title == 'Déconnexion') {
      Navigator.pushReplacementNamed(context, '/connexion');
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('$title non implémenté')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA),
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        title: Text(
          'BinMax',
          style: GoogleFonts.inter(
            fontWeight: FontWeight.w700,
            fontSize: 24,
            color: const Color(0xFF1E88E5),
          ),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.search_rounded, color: Color(0xFF1E88E5)),
            onPressed: _handleSearch,
          ).animate().fadeIn(delay: 800.ms),
        ],
      ),
      drawer: _menuNavigation(context),
      body: SafeArea(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
              child: Text(
                'Découvrez nos offres',
                style: GoogleFonts.inter(
                  fontSize: 24,
                  fontWeight: FontWeight.w700,
                  color: const Color(0xFF333333),
                ),
              ).animate().fadeIn(delay: 200.ms),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: _selecteurCategories(),
            ).animate().fadeIn(delay: 400.ms),
            Expanded(
              child: _productGrid(),
            ),
          ],
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) {
          setState(() => _currentIndex = index);
          if (index == 1) {
            Navigator.pushNamed(context, '/swipe');
          } else if (index == 2) {
            Navigator.pushNamed(context, '/panier');
          }
        },
        selectedItemColor: const Color(0xFF1E88E5),
        unselectedItemColor: const Color(0xFF666666),
        backgroundColor: Colors.white,
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.home_rounded),
            label: 'Accueil',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.swipe_rounded),
            label: 'Swipe',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.shopping_cart_rounded),
            label: 'Panier',
          ),
        ],
      ),
    );
  }

  Widget _menuNavigation(BuildContext context) {
    return Drawer(
      backgroundColor: Colors.white,
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          DrawerHeader(
            decoration: const BoxDecoration(
              color: Color(0xFF1E88E5),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                const CircleAvatar(
                  radius: 30,
                  backgroundColor: Colors.white,
                  child: Icon(Icons.person, size: 40, color: Color(0xFF1E88E5)),
                ),
                const SizedBox(height: 12),
                Flexible(
                  child: Text(
                    'Mon Profil',
                    style: GoogleFonts.inter(
                      fontSize: 20,
                      color: Colors.white,
                      fontWeight: FontWeight.w700,
                    ),
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                const SizedBox(height: 4),
                Flexible(
                  child: Text(
                    'Utilisateur',
                    style: GoogleFonts.inter(
                      fontSize: 14,
                      color: Colors.white70,
                    ),
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
              ],
            ),
          ),
          _itemMenu(Icons.person_rounded, 'Profil'),
          _itemMenu(Icons.local_shipping_rounded, 'Livraison'),
          _itemMenu(Icons.account_balance_wallet_rounded, 'Crédit'),
          _itemMenu(Icons.settings_rounded, 'Paramètres'),
          _itemMenu(Icons.notifications_rounded, 'Notifications'),
          const Divider(color: Colors.black12),
          _itemMenu(Icons.logout_rounded, 'Déconnexion'),
        ],
      ),
    );
  }

  Widget _itemMenu(IconData icone, String titre) {
    return ListTile(
      leading: Icon(icone, color: const Color(0xFF1E88E5)),
      title: Text(
        titre,
        style: GoogleFonts.inter(
          color: const Color(0xFF333333),
          fontWeight: FontWeight.w500,
        ),
      ),
      onTap: () => _handleMenuItem(titre),
    ).animate().fadeIn(delay: 400.ms).slideX(begin: -0.2);
  }

  Widget _selecteurCategories() {
    return SizedBox(
      height: 40,
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        itemCount: _categories.length,
        itemBuilder: (ctx, index) => Padding(
          padding: const EdgeInsets.symmetric(horizontal: 8),
          child: GestureDetector(
            onTap: () => setState(() => _indexCategorie = index),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              decoration: BoxDecoration(
                color: _indexCategorie == index
                    ? const Color(0xFF1E88E5)
                    : const Color(0xFFF5F7FA),
                borderRadius: BorderRadius.circular(20),
              ),
              child: Text(
                _categories[index],
                style: GoogleFonts.inter(
                  color: _indexCategorie == index
                      ? Colors.white
                      : const Color(0xFF666666),
                  fontWeight: FontWeight.w600,
                  fontSize: 14,
                ),
              ),
            ),
          ),
        ).animate().fadeIn(delay: Duration(milliseconds: 200 + index * 100)),
      ),
    );
  }

  Widget _productGrid() {
    return GridView.builder(
      padding: const EdgeInsets.all(16),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        crossAxisSpacing: 16,
        mainAxisSpacing: 16,
        childAspectRatio: 0.75,
      ),
      itemCount: 6, // Placeholder
      itemBuilder: (context, index) {
        return GestureDetector(
          onTap: () => Navigator.pushNamed(context, '/swipe'),
          child: Container(
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(12),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.1),
                  blurRadius: 8,
                  offset: const Offset(0, 4),
                ),
              ],
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                ClipRRect(
                  borderRadius: const BorderRadius.vertical(top: Radius.circular(12)),
                  child: Image.network(
                    'https://via.placeholder.com/150',
                    height: 120,
                    width: double.infinity,
                    fit: BoxFit.cover,
                    errorBuilder: (context, error, stackTrace) => Container(
                      height: 120,
                      color: const Color(0xFFF5F7FA),
                      child: const Icon(
                        Icons.image,
                        size: 60,
                        color: Color(0xFF666666),
                      ),
                    ),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.all(12),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Produit ${index + 1}',
                        style: GoogleFonts.inter(
                          fontSize: 16,
                          fontWeight: FontWeight.w600,
                          color: const Color(0xFF333333),
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        'Offre exclusive',
                        style: GoogleFonts.inter(
                          fontSize: 12,
                          color: const Color(0xFF666666),
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        '€${(99.99 - index * 10).toStringAsFixed(2)}',
                        style: GoogleFonts.inter(
                          fontSize: 16,
                          fontWeight: FontWeight.w700,
                          color: const Color(0xFF26A69A),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ).animate().fadeIn(delay: Duration(milliseconds: 200 + index * 100));
      },
    );
  }
}