import 'package:flutter/material.dart';
import 'pages/authentication_page.dart';
import 'pages/product_list_page.dart';

void main() {
  runApp(PayeTonKawaApp());
}

class PayeTonKawaApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'PayeTonKawa',
      theme: ThemeData(
        primarySwatch: Colors.brown,
      ),
      // La page d'accueil est celle d'authentification/inscription
      home: const AuthenticationPage(),
      routes: {
        // Route pour accéder à la liste des produits (authentification requise)
        '/products': (context) => const ProductListPage(),
      },
    );
  }
}
