import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ProductListPage extends StatefulWidget {
  const ProductListPage({Key? key}) : super(key: key);

  @override
  State<ProductListPage> createState() => _ProductListPageState();
}

class _ProductListPageState extends State<ProductListPage> {
  List<dynamic> products = [];
  bool isLoading = true;
  String errorMessage = '';

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final String? apiKey = ModalRoute.of(context)!.settings.arguments as String?;
    if (apiKey != null) {
      _fetchProducts(apiKey);
    } else {
      setState(() {
        isLoading = false;
        errorMessage = "Clé d'authentification manquante.";
      });
    }
  }

  Future<void> _fetchProducts(String apiKey) async {
    final url = Uri.parse('https://38cf-2001-861-3a02-a880-5dfd-14ce-366c-f1f1.ngrok-free.app/api/revendeurs/products');
    try {
      final response = await http.get(
        url,
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': apiKey,
        },
      );
      if (response.statusCode == 200) {
        setState(() {
          products = json.decode(response.body)['products'];
          isLoading = false;
        });
      } else {
        setState(() {
          errorMessage = 'Erreur lors du chargement des produits : ${response.statusCode}';
          isLoading = false;
        });
      }
    } catch (e) {
      setState(() {
        errorMessage = 'Erreur lors de la connexion à l’API : $e';
        isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Liste des produits'),
      ),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : errorMessage.isNotEmpty
          ? Center(child: Text(errorMessage))
          : ListView.builder(
        itemCount: products.length,
        itemBuilder: (context, index) {
          final product = products[index];
          return ListTile(
            title: Text(product['name'] ?? 'Nom indisponible'),
            subtitle: Text(product['description'] ?? 'Pas de description'),
            trailing: Text("${product['price']} €"),
          );
        },
      ),
    );
  }
}