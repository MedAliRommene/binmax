class User {
  final int id;
  final String username;
  final String role;
  final String location;
  final ClientProfile? clientProfile;

  User({
    required this.id,
    required this.username,
    required this.role,
    required this.location,
    this.clientProfile,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      username: json['username'],
      role: json['role'],
      location: json['location'] ?? '',
      clientProfile: json['client_profile'] != null
          ? ClientProfile.fromJson(json['client_profile'])
          : null,
    );
  }
}

class ClientProfile {
  final int id;
  final String nom;
  final String prenom;
  final String adresse;
  final double soldeDeCredit;

  ClientProfile({
    required this.id,
    required this.nom,
    required this.prenom,
    required this.adresse,
    required this.soldeDeCredit,
  });

  factory ClientProfile.fromJson(Map<String, dynamic> json) {
    return ClientProfile(
      id: json['id'],
      nom: json['nom'],
      prenom: json['prenom'],
      adresse: json['adresse'],
      soldeDeCredit: (json['solde_de_credit'] as num).toDouble(),
    );
  }
}