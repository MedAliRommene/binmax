class Produit {
  final String id;
  final String nom;
  final String description;
  final double prix;
  final List<String> imageUrls;
  final String categorie;

  Produit({
    required this.id,
    required this.nom,
    required this.description,
    required this.prix,
    required this.imageUrls,
    required this.categorie,
  });

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is Produit && runtimeType == other.runtimeType && id == other.id;

  @override
  int get hashCode => id.hashCode;
}