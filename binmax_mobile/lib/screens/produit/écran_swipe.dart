import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:binmax_mobile/models/produit.dart';

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

  @override
  void initState() {
    super.initState();
    _chargerProduits();
  }

  void _chargerProduits() {
    _produits.addAll([
      Produit(
        id: '1',
        nom: 'Casque Audio Premium',
        description: 'Qualité sonore exceptionnelle',
        prix: 299.99,
        imageUrl: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e',
        categorie: 'Électronique',
      ),
      Produit(
        id: '2',
        nom: 'Sneakers Tendances',
        description: 'Confort et style au quotidien',
        prix: 129.99,
        imageUrl: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff',
        categorie: 'Mode',
      ),
      Produit(
        id: '3',
        nom: 'Lampe LED Moderne',
        description: 'Éclairage intelligent pour votre maison',
        prix: 49.99,
        imageUrl: 'https://images.unsplash.com/photo-1513506003901-1e6a229e2d15',
        categorie: 'Maison',
      ),
    ]);
    setState(() {});
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
      setState(() {
        if (_produits.isNotEmpty) {
          _produits.removeAt(0);
        }
        _dragOffset = 0.0;
        _isLiking = false;
        _isDisliking = false;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(_dragOffset > 0 ? 'Produit aimé !' : 'Produit ignoré'),
          backgroundColor: _dragOffset > 0 ? const Color(0xFF26A69A) : Colors.red,
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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA),
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios_new_rounded, color: Color(0xFF1E88E5)),
          onPressed: () => Navigator.pop(context),
        ).animate().fadeIn(delay: 200.ms),
        title: Text(
          'Swipe Deals',
          style: GoogleFonts.inter(
            fontWeight: FontWeight.w700,
            fontSize: 24,
            color: const Color(0xFF333333),
          ),
        ),
      ),
      body: SafeArea(
        child: Center(
          child: _produits.isNotEmpty
              ? Stack(
                  children: [
                    GestureDetector(
                      onPanUpdate: _gererSwipe,
                      onPanEnd: _gererFinSwipe,
                      child: _carteProduit(_produits.first),
                    ),
                    if (_isLiking)
                      Positioned(
                        top: 20,
                        left: 20,
                        child: _swipeOverlay('Like', const Color(0xFF26A69A)),
                      ),
                    if (_isDisliking)
                      Positioned(
                        top: 20,
                        right: 20,
                        child: _swipeOverlay('Dislike', Colors.red),
                      ),
                  ],
                )
              : _aucunProduit(),
        ),
      ),
    );
  }

  Widget _carteProduit(Produit produit) {
    return Transform.translate(
      offset: Offset(_dragOffset, 0),
      child: Transform.rotate(
        angle: _dragOffset / 1000,
        child: Container(
          width: 350,
          height: 500,
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
                  produit.imageUrl,
                  height: 300,
                  width: 350,
                  fit: BoxFit.cover,
                  errorBuilder: (context, error, stackTrace) => Container(
                    height: 300,
                    color: const Color(0xFFF5F7FA),
                    child: const Icon(
                      Icons.image,
                      size: 150,
                      color: Color(0xFF666666),
                    ),
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      produit.nom,
                      style: GoogleFonts.inter(
                        fontSize: 20,
                        fontWeight: FontWeight.w700,
                        color: const Color(0xFF333333),
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      produit.description,
                      style: GoogleFonts.inter(
                        fontSize: 14,
                        color: const Color(0xFF666666),
                      ),
                    ),
                    const SizedBox(height: 12),
                    Text(
                      '${produit.prix}€',
                      style: GoogleFonts.inter(
                        fontSize: 18,
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
      ),
    ).animate().fadeIn(delay: 400.ms);
  }

  Widget _swipeOverlay(String text, Color color) {
    return Transform.rotate(
      angle: text == 'Like' ? -0.2 : 0.2,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          border: Border.all(color: color, width: 2),
          borderRadius: BorderRadius.circular(8),
          color: color.withOpacity(0.1),
        ),
        child: Text(
          text,
          style: GoogleFonts.inter(
            fontSize: 24,
            fontWeight: FontWeight.w700,
            color: color,
          ),
        ),
      ),
    ).animate().fadeIn(duration: 200.ms);
  }

  Widget _aucunProduit() {
    return Container(
      padding: const EdgeInsets.all(20),
      child: Text(
        'Aucun produit disponible',
        style: GoogleFonts.inter(
          fontSize: 18,
          color: const Color(0xFF666666),
          fontWeight: FontWeight.w500,
        ),
      ),
    ).animate().fadeIn(delay: 400.ms);
  }
}