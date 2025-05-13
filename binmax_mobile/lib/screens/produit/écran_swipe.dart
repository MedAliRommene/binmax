import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:smooth_page_indicator/smooth_page_indicator.dart';
import 'package:binmax_mobile/models/produit.dart';
import 'package:binmax_mobile/screens/panier/écran_panier.dart';

class EcranSwipe extends StatefulWidget {
  const EcranSwipe({super.key});

  @override
  _EcranSwipeState createState() => _EcranSwipeState();
}

class _EcranSwipeState extends State<EcranSwipe> with SingleTickerProviderStateMixin {
  final List<Produit> _produits = [];
  double _dragOffset = 0.0;
  bool _isLiking = false;
  bool _isDisliking = false;
  String? _selectedCategory;
  final PageController _pageController = PageController();

  @override
  void initState() {
    super.initState();
    _chargerProduits();
  }

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  void _chargerProduits() {
    _produits.clear();
    _produits.addAll([
      // Électronique (3 produits)
      Produit(
        id: '1',
        nom: 'Casque Audio Premium',
        description: 'Qualité sonore exceptionnelle',
        prix: 299.99,
        imageUrls: [
          'https://images.unsplash.com/photo-1505740420928-5e560c06d30e',
          'https://images.unsplash.com/photo-1613040809024-b297ef6b5209',
          'https://images.unsplash.com/photo-1590658268037-6bf12165a8df',
        ],
        categorie: 'Électronique',
      ),
      Produit(
        id: '5',
        nom: 'Smartphone Ultra',
        description: 'Technologie de pointe',
        prix: 799.99,
        imageUrls: [
          'https://images.unsplash.com/photo-1598327105666-5b89351aff97',
          'https://images.unsplash.com/photo-1607936854279-55e8a4c64888',
        ],
        categorie: 'Électronique',
      ),
      Produit(
        id: '6',
        nom: 'Écouteurs Sans Fil',
        description: 'Liberté et confort',
        prix: 129.99,
        imageUrls: [
          'https://images.unsplash.com/photo-1590658268037-6bf12165a8df',
          'https://images.unsplash.com/photo-1610793561111-2e1a850f2b6f',
        ],
        categorie: 'Électronique',
      ),
      // Mode (3 produits)
      Produit(
        id: '2',
        nom: 'Sneakers Tendances',
        description: 'Confort et style au quotidien',
        prix: 129.99,
        imageUrls: [
          'https://images.unsplash.com/photo-1542291026-7eec264c27ff',
          'https://images.unsplash.com/photo-1608231387042-66d1773070a5',
          'https://images.unsplash.com/photo-1600585154340-be6161a56a0c',
        ],
        categorie: 'Mode',
      ),
      Produit(
        id: '7',
        nom: 'Veste en Cuir',
        description: 'Élégance intemporelle',
        prix: 249.99,
        imageUrls: [
          'https://images.unsplash.com/photo-1521223342351-8df75ed9b6ef',
          'https://images.unsplash.com/photo-1551488831-00ddcb6c6bd3',
        ],
        categorie: 'Mode',
      ),
      Produit(
        id: '8',
        nom: 'Sac à Main Design',
        description: 'Accessoire chic et pratique',
        prix: 89.99,
        imageUrls: [
          'https://images.unsplash.com/photo-1584917865442-de8e836bb114',
          'https://images.unsplash.com/photo-1585487000160-6ebcfceb29c4',
        ],
        categorie: 'Mode',
      ),
      // Maison (3 produits)
      Produit(
        id: '3',
        nom: 'Lampe LED Moderne',
        description: 'Éclairage intelligent pour votre maison',
        prix: 49.99,
        imageUrls: [
          'https://images.unsplash.com/photo-1513506003901-1e6a229e2d15',
          'https://images.unsplash.com/photo-1574779562612-a7a03f454e89',
          'https://images.unsplash.com/photo-1597794001988-59596b02c28b',
        ],
        categorie: 'Maison',
      ),
      Produit(
        id: '9',
        nom: 'Coussin Décoratif',
        description: 'Confort et style pour votre salon',
        prix: 29.99,
        imageUrls: [
          'https://images.unsplash.com/photo-1586104196936-c4d1b7f18f80',
          'https://images.unsplash.com/photo-1600585154340-be6161a56a0c',
        ],
        categorie: 'Maison',
      ),
      Produit(
        id: '10',
        nom: 'Tapis Moderne',
        description: 'Chaleur et élégance',
        prix: 99.99,
        imageUrls: [
          'https://images.unsplash.com/photo-1600585154340-be6161a56a0c',
          'https://images.unsplash.com/photo-1611095564985-897f952e2e86',
        ],
        categorie: 'Maison',
      ),
      // Beauté (3 produits)
      Produit(
        id: '4',
        nom: 'Parfum Luxe',
        description: 'Fragrance unique et durable',
        prix: 89.99,
        imageUrls: [
          'https://images.unsplash.com/photo-1587017530098-3b4b3c4f6a6b',
          'https://images.unsplash.com/photo-1541643600914-78b084683601',
          'https://images.unsplash.com/photo-1611944212120-432f0fb9181f',
        ],
        categorie: 'Beauté',
      ),
      Produit(
        id: '11',
        nom: 'Palette de Maquillage',
        description: 'Couleurs vibrantes pour tous les looks',
        prix: 39.99,
        imageUrls: [
          'https://images.unsplash.com/photo-1512496015851-a90fb38ba796',
          'https://images.unsplash.com/photo-1591376056760-6fb29c9b47b1',
        ],
        categorie: 'Beauté',
      ),
      Produit(
        id: '12',
        nom: 'Crème Hydratante',
        description: 'Soin doux pour la peau',
        prix: 24.99,
        imageUrls: [
          'https://images.unsplash.com/photo-1571781741790-3cd376b4d301',
          'https://images.unsplash.com/photo-1625772156158-1e0f3f3b8b26',
        ],
        categorie: 'Beauté',
      ),
    ]);
    setState(() {});
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _selectedCategory = ModalRoute.of(context)?.settings.arguments as String?;
    if (_selectedCategory != null) {
      _produits.retainWhere((produit) => produit.categorie == _selectedCategory);
      setState(() {});
    }
  }

  void _gererSwipe(DragUpdateDetails details) {
    setState(() {
      _dragOffset += details.delta.dx;
      _isLiking = _dragOffset > 50;
      _isDisliking = _dragOffset < -50;
    });
  }

  void _gererFinSwipe(DragEndDetails details) {
    if (_dragOffset.abs() > 100) {
      final produit = _produits.first;
      if (_dragOffset > 0) {
        EcranPanier.addToCart(produit);
      }
      setState(() {
        if (_produits.isNotEmpty) {
          _produits.removeAt(0);
          _pageController.jumpToPage(0); // Reset to first image
        }
        _dragOffset = 0.0;
        _isLiking = false;
        _isDisliking = false;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(_dragOffset > 0 ? 'Ajouté au panier !' : 'Produit ignoré'),
          backgroundColor: _dragOffset > 0 ? const Color(0xFFE94057) : Colors.grey,
        ),
      );
    } else {
      setState(() {
        _dragOffset = 0.0;
        _isLiking = false;
        _isDisliking = false;
      });
    }
  }

  void _handleLike() {
    final produit = _produits.first;
    EcranPanier.addToCart(produit);
    setState(() {
      if (_produits.isNotEmpty) {
        _produits.removeAt(0);
        _pageController.jumpToPage(0); // Reset to first image
      }
      _dragOffset = 0.0;
      _isLiking = false;
      _isDisliking = false;
    });
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Ajouté au panier !'),
        backgroundColor: Color(0xFFE94057),
      ),
    );
  }

  void _handleDislike() {
    setState(() {
      if (_produits.isNotEmpty) {
        _produits.removeAt(0);
        _pageController.jumpToPage(0); // Reset to first image
      }
      _dragOffset = 0.0;
      _isLiking = false;
      _isDisliking = false;
    });
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Produit ignoré'),
        backgroundColor: Colors.grey,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Container(
        decoration: const BoxDecoration(
          gradient: RadialGradient(
            center: Alignment.center,
            radius: 1.5,
            colors: [Color(0xFFFFFFFF), Color(0xFFF5F7FA)],
          ),
        ),
        child: SafeArea(
          child: Column(
            children: [
              AppBar(
                backgroundColor: Colors.transparent,
                elevation: 0,
                leading: IconButton(
                  icon: const Icon(Icons.arrow_back_ios_new_rounded, color: Color(0xFFE94057)),
                  onPressed: () => Navigator.pop(context),
                ).animate().fadeIn(delay: 200.ms),
                title: Text(
                  'Swipe - ${_selectedCategory ?? "Tous"}',
                  style: GoogleFonts.inter(
                    fontWeight: FontWeight.w700,
                    fontSize: 24,
                    color: const Color(0xFF333333),
                  ),
                ),
              ),
              Expanded(
                child: Center(
                  child: _produits.isNotEmpty
                      ? Stack(
                          alignment: Alignment.center,
                          children: [
                            GestureDetector(
                              onPanUpdate: _gererSwipe,
                              onPanEnd: _gererFinSwipe,
                              child: _carteProduit(_produits.first),
                            ),
                            if (_isLiking)
                              Positioned(
                                top: 30,
                                left: 30,
                                child: _swipeOverlay(Icons.favorite, const Color(0xFFE94057)),
                              ),
                            if (_isDisliking)
                              Positioned(
                                top: 30,
                                right: 30,
                                child: _swipeOverlay(Icons.close, const Color(0xFF666666)),
                              ),
                            Positioned(
                              bottom: 20,
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  _actionButton(
                                    icon: Icons.close,
                                    color: const Color(0xFF666666),
                                    onPressed: _handleDislike,
                                  ),
                                  const SizedBox(width: 30),
                                  _actionButton(
                                    icon: Icons.favorite,
                                    color: const Color(0xFFE94057),
                                    onPressed: _handleLike,
                                  ),
                                ],
                              ),
                            ),
                          ],
                        )
                      : _aucunProduit(),
                ),
              ),
            ],
          ),
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: 0, // Accueil is active
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
        onTap: (index) {
          if (index == 1) {
            Navigator.pushReplacementNamed(context, '/panier');
          }
        },
      ),
    );
  }

  Widget _carteProduit(Produit produit) {
    return Transform.translate(
      offset: Offset(_dragOffset, 0),
      child: Transform.rotate(
        angle: _dragOffset / 1000,
        child: Transform.scale(
          scale: 1.0 + (_dragOffset.abs() / 5000),
          child: Container(
            width: 360,
            height: 540,
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(
                color: Colors.transparent,
                width: 2,
              ),
              gradient: const LinearGradient(
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
                colors: [Color(0xFFE94057), Color(0xFFF27121)],
                stops: [0.0, 1.0],
              ),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.15),
                  blurRadius: 12,
                  offset: const Offset(0, 6),
                ),
              ],
            ),
            child: Container(
              margin: const EdgeInsets.all(2),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(14),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Stack(
                    children: [
                      ClipRRect(
                        borderRadius: const BorderRadius.vertical(top: Radius.circular(14)),
                        child: SizedBox(
                          height: 320,
                          width: 360,
                          child: PageView.builder(
                            controller: _pageController,
                            itemCount: produit.imageUrls.length,
                            itemBuilder: (context, index) {
                              return Image.network(
                                produit.imageUrls[index],
                                height: 320,
                                width: 360,
                                fit: BoxFit.cover,
                                errorBuilder: (context, error, stackTrace) => Container(
                                  height: 320,
                                  color: const Color(0xFFF5F7FA),
                                  child: const Icon(
                                    Icons.image,
                                    size: 160,
                                    color: Color(0xFF666666),
                                  ),
                                ),
                              );
                            },
                          ),
                        ),
                      ),
                      Positioned(
                        top: 10,
                        right: 10,
                        child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                          decoration: BoxDecoration(
                            color: const Color(0xFFE94057),
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Text(
                            produit.categorie,
                            style: GoogleFonts.inter(
                              fontSize: 12,
                              fontWeight: FontWeight.w600,
                              color: Colors.white,
                            ),
                          ),
                        ),
                      ),
                      Positioned(
                        bottom: 10,
                        left: 0,
                        right: 0,
                        child: Center(
                          child: SmoothPageIndicator(
                            controller: _pageController,
                            count: produit.imageUrls.length,
                            effect: const WormEffect(
                              dotHeight: 8,
                              dotWidth: 8,
                              activeDotColor: Color(0xFFE94057),
                              dotColor: Color(0xFF666666),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                  Padding(
                    padding: const EdgeInsets.all(20),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          produit.nom,
                          style: GoogleFonts.inter(
                            fontSize: 22,
                            fontWeight: FontWeight.w800,
                            color: const Color(0xFF333333),
                          ),
                        ),
                        const SizedBox(height: 10),
                        Text(
                          produit.description,
                          style: GoogleFonts.inter(
                            fontSize: 14,
                            color: const Color(0xFF666666),
                          ),
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                        ),
                        const SizedBox(height: 14),
                        Text(
                          '${produit.prix}€',
                          style: GoogleFonts.inter(
                            fontSize: 20,
                            fontWeight: FontWeight.w800,
                            color: const Color(0xFFF27121),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    ).animate().fadeIn(delay: 400.ms);
  }

  Widget _swipeOverlay(IconData icon, Color color) {
    return Transform.rotate(
      angle: icon == Icons.favorite ? -0.2 : 0.2,
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: color.withOpacity(0.2),
          borderRadius: BorderRadius.circular(12),
          boxShadow: [
            BoxShadow(
              color: color.withOpacity(0.3),
              blurRadius: 8,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: Icon(
          icon,
          size: 40,
          color: color,
        ),
      ),
    ).animate().fadeIn(duration: 200.ms).scale();
  }

  Widget _actionButton({required IconData icon, required Color color, required VoidCallback onPressed}) {
    return ElevatedButton(
      style: ElevatedButton.styleFrom(
        backgroundColor: Colors.white,
        foregroundColor: color,
        shape: const CircleBorder(),
        padding: const EdgeInsets.all(16),
        elevation: 8,
      ),
      onPressed: onPressed,
      child: Icon(icon, size: 32, color: color),
    ).animate().fadeIn(delay: 600.ms);
  }

  Widget _aucunProduit() {
    return Container(
      padding: const EdgeInsets.all(20),
      child: Text(
        'Aucun produit dans cette catégorie',
        style: GoogleFonts.inter(
          fontSize: 18,
          color: const Color(0xFF666666),
          fontWeight: FontWeight.w500,
        ),
      ),
    ).animate().fadeIn(delay: 400.ms);
  }
}