import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:google_fonts/google_fonts.dart';

class EcranPrincipal extends StatefulWidget {
  const EcranPrincipal({super.key});

  @override
  _EcranPrincipalState createState() => _EcranPrincipalState();
}

class _EcranPrincipalState extends State<EcranPrincipal> {
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

  void _handleCategorySelection(String category) {
    Navigator.pushNamed(context, '/swipe', arguments: category);
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
            fontWeight: FontWeight.w800,
            fontSize: 24,
            color: const Color(0xFFE94057),
          ),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.search_rounded, color: Color(0xFFE94057)),
            onPressed: _handleSearch,
          ).animate().fadeIn(delay: 800.ms),
        ],
      ),
      drawer: _menuNavigation(context),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Choisissez une catégorie',
                style: GoogleFonts.inter(
                  fontSize: 24,
                  fontWeight: FontWeight.w700,
                  color: const Color(0xFF333333),
                ),
              ).animate().fadeIn(delay: 200.ms),
              const SizedBox(height: 24),
              Expanded(
                child: GridView.builder(
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 2,
                    crossAxisSpacing: 16,
                    mainAxisSpacing: 16,
                    childAspectRatio: 1.0,
                  ),
                  itemCount: _categories.length,
                  itemBuilder: (context, index) {
                    return GestureDetector(
                      onTap: () => _handleCategorySelection(_categories[index]),
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
                        child: Center(
                          child: Text(
                            _categories[index],
                            style: GoogleFonts.inter(
                              fontSize: 18,
                              fontWeight: FontWeight.w600,
                              color: const Color(0xFFE94057),
                            ),
                            textAlign: TextAlign.center,
                          ),
                        ),
                      ),
                    ).animate().fadeIn(delay: Duration(milliseconds: 200 + index * 100));
                  },
                ),
              ),
            ],
          ),
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) {
          setState(() => _currentIndex = index);
          if (index == 1) {
            Navigator.pushNamed(context, '/panier');
          }
        },
        selectedItemColor: const Color(0xFFE94057),
        unselectedItemColor: const Color(0xFF666666),
        backgroundColor: Colors.white,
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.home_rounded),
            label: 'Accueil',
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
              color: Color(0xFFE94057),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                const CircleAvatar(
                  radius: 30,
                  backgroundColor: Colors.white,
                  child: Icon(Icons.person, size: 40, color: Color(0xFFE94057)),
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
      leading: Icon(icone, color: const Color(0xFFE94057)),
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
}