import 'package:flutter/material.dart';
import 'package:flutter_swiper_null_safety/flutter_swiper_null_safety.dart';
import '../services/api_service.dart';
import '../models/product.dart';
import 'cart_screen.dart';

class ClientHomeScreen extends StatefulWidget {
  @override
  _ClientHomeScreenState createState() => _ClientHomeScreenState();
}

class _ClientHomeScreenState extends State<ClientHomeScreen> {
  List<Product> _products = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadProducts();
  }

  void _loadProducts() async {
    setState(() => _isLoading = true);
    try {
      final products = await ApiService.getProducts();
      setState(() {
        _products = products;
        _isLoading = false;
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to load products: $e')),
      );
      setState(() => _isLoading = false);
    }
  }

  void _addToCart(Product product) async {
    try {
      await ApiService.addToCart(product.id, 1);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('${product.name} added to cart')),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to add to cart: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Product Swipe'),
        actions: [
          IconButton(
            icon: Icon(Icons.shopping_cart),
            onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => CartScreen())),
          ),
        ],
      ),
      body: _isLoading
          ? Center(child: CircularProgressIndicator())
          : Swiper(
              itemCount: _products.length,
              itemBuilder: (context, index) {
                final product = _products[index];
                return Card(
                  elevation: 4,
                  child: Column(
                    children: [
                      Image.network(
                        'http://localhost:8000${product.reference}', // Adjust based on your image URL
                        height: 200,
                        fit: BoxFit.cover,
                      ),
                      ListTile(
                        title: Text(product.name),
                        subtitle: Text('${product.price}€ - ${product.reste} left'),
                      ),
                      ElevatedButton(
                        onPressed: () => _addToCart(product),
                        child: Text('Add to Cart'),
                      ),
                    ],
                  ),
                );
              },
              layout: SwiperLayout.TINDER,
              itemWidth: 300,
              itemHeight: 400,
            ),
    );
  }
}