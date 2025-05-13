import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class ChampAnime extends StatelessWidget {
  final String hint;
  final IconData icone;
  final bool estCache;
  final String? Function(String?)? validator;
  final TextEditingController? controller;

  const ChampAnime({
    super.key,
    required this.icone,
    required this.hint,
    this.estCache = false,
    this.validator,
    this.controller,
  });

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      controller: controller,
      obscureText: estCache,
      validator: validator,
      style: GoogleFonts.inter(color: const Color(0xFF333333)),
      decoration: InputDecoration(
        prefixIcon: Icon(icone, color: const Color(0xFF666666)),
        hintText: hint,
        hintStyle: GoogleFonts.inter(color: const Color(0xFF666666)),
        errorStyle: GoogleFonts.inter(color: Colors.redAccent, fontSize: 12),
        filled: true,
        fillColor: const Color(0xFFF5F7FA),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide.none,
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: Color(0xFF1E88E5), width: 1),
        ),
        contentPadding: const EdgeInsets.symmetric(vertical: 16, horizontal: 20),
      ),
    );
  }
}