import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'screens/auth/connexion.dart';
import 'screens/auth/inscription.dart';
import 'screens/home/écran_principal.dart';
import 'screens/produit/écran_swipe.dart';
import 'screens/panier/écran_panier.dart';

void main() {
  Animate.defaultCurve = Curves.easeInOutCubic;
  runApp(const BinmaxApp());
}

class BinmaxApp extends StatelessWidget {
  const BinmaxApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFFE94057),
          brightness: Brightness.light,
        ),
        textTheme: GoogleFonts.poppinsTextTheme(),
      ),
      routes: {
        '/connexion': (context) => const EcranConnexion(),
        '/inscription': (context) => const EcranInscription(),
        '/principal': (context) => const EcranPrincipal(),
        '/panier': (context) => const EcranPanier(),
        '/swipe': (context) => const EcranSwipe(),
      },
    );
  }
}