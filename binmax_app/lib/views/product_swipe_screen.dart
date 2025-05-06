import 'package:flutter/material.dart';
import 'package:cards_swiper/cards_swiper.dart';
import '../widgets/product_card.dart';
import '../models/product.dart';
import '../services/api_service.dart';

class ProductSwipeScreen extends StatefulWidget {
  const ProductSwipeScreen({super.key});

  @override
  State<ProductSwipeScreen> createState() => _ProductSwipeScreenState();
}

class _ProductSwipeScreenState extends State<ProductSwipeScreen> {
  final ApiService _apiService = ApiService();
  final SwiperController _swiperController = SwiperController();
  List<Product> _products = [];

  @override
  void initState() {
    super.initState();
    _loadProducts();
  }

  Future<void> _loadProducts() async {
    try {
      final products = await _apiService.getProducts();
      setState(() => _products = products);
    } catch (e) {
      print('Erreur de chargement: $e');
    }
  }

  void _onSwipe(int index, SwiperDirection direction) {
    if (direction == SwiperDirection.right) {
      // Ajouter au panier
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Découvrez nos produits')),
      body: _products.isEmpty
          ? const Center(child: CircularProgressIndicator())
          : Swiper(
              itemBuilder: (context, index) => ProductCard(product: _products[index]),
              itemCount: _products.length,
              controller: _swiperController,
              curve: Curves.easeInOut,
              onIndexChanged: _onSwipe,
              layout: SwiperLayout.STACK,
              itemWidth: 300,
              itemHeight: 400,
            ),
    );
  }
}