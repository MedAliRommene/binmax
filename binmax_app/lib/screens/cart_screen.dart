import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/cart.dart';

class CartScreen extends StatefulWidget {
  @override
  _CartScreenState createState() => _CartScreenState();
}

class _CartScreenState extends State<CartScreen> {
  Cart? _cart;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadCart();
  }

  void _loadCart() async {
    setState(() => _isLoading = true);
    try {
      final cart = await ApiService.getCart();
      setState(() {
        _cart = cart;
        _isLoading = false;
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to load cart: $e')),
      );
      setState(() => _isLoading = false);
    }
  }

  void _checkout() async {
    try {
      await ApiService.checkout('DOMICILE', '123 Main St'); // Adjust address dynamically
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Order placed successfully')),
      );
      _loadCart();
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Checkout failed: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Cart')),
      body: _isLoading
          ? Center(child: CircularProgressIndicator())
          : _cart == null || _cart!.items.isEmpty
              ? Center(child: Text('Cart is empty'))
              : Column(
                  children: [
                    Expanded(
                      child: ListView.builder(
                        itemCount: _cart!.items.length,
                        itemBuilder: (context, index) {
                          final item = _cart!.items[index];
                          return ListTile(
                            title: Text(item.product.name),
                            subtitle: Text('${item.quantity} x ${item.product.price}€'),
                          );
                        },
                      ),
                    ),
                    ElevatedButton(
                      onPressed: _checkout,
                      child: Text('Checkout'),
                    ),
                  ],
                ),
    );
  }
}