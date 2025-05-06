class ProductSwipeScreen extends StatefulWidget {
  @override
  _ProductSwipeScreenState createState() => _ProductSwipeScreenState();
}

class _ProductSwipeScreenState extends State<ProductSwipeScreen> {
  final ApiService _apiService = ApiService();
  List<Product> _products = [];
  int _currentIndex = 0;

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
      print('Erreur chargement produits: $e');
    }
  }

  void _onSwipedRight() {
    // Ajouter au panier
    if (_currentIndex < _products.length - 1) {
      setState(() => _currentIndex++);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Découvrez nos produits')),
      body: _products.isEmpty
          ? Center(child: CircularProgressIndicator())
          : Stack(
              children: _products.map((product) => TinderCard(
                product: product,
                onSwipedRight: _onSwipedRight,
              )).toList(),
            ),
    );
  }
}