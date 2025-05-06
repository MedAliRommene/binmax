class Product {
  final int id;
  final String reference;
  final String name;
  final String description;
  final double price;
  final int quantity;
  final int vendus;
  final int reste;

  Product({
    required this.id,
    required this.reference,
    required this.name,
    required this.description,
    required this.price,
    required this.quantity,
    required this.vendus,
    required this.reste,
  });

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
      id: json['id'],
      reference: json['reference'],
      name: json['name'],
      description: json['description'],
      price: (json['price'] as num).toDouble(),
      quantity: json['quantity'],
      vendus: json['vendus'],
      reste: json['reste'],
    );
  }
}