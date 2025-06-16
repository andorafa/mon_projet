import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

import 'ProductDetailPage.dart';
import 'authentication_page.dart';

final _secureStorage = FlutterSecureStorage();

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
    final argKey = ModalRoute.of(context)?.settings.arguments as String?;
    if (argKey != null && argKey.isNotEmpty) {
      _fetchProducts(argKey);
    } else {
      _secureStorage.read(key: 'api_key').then((storedKey) {
        if (storedKey != null) {
          _fetchProducts(storedKey);
        } else {
          setState(() {
            isLoading = false;
            errorMessage = "Clé d'authentification manquante.";
          });
        }
      });
    }
  }

  Future<void> _fetchProducts(String apiKey) async {
    setState(() {
      isLoading = true;
      errorMessage = '';
    });
    final url = Uri.parse('https://payetonkawa-api.onrender.com/api/revendeurs/products');
    try {
      final response = await http.get(
        url,
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': apiKey,
        },
      );
      if (response.statusCode == 200) {
        final body = json.decode(response.body);
        setState(() {
          products = body as List<dynamic>;
          isLoading = false;
        });
      } else {
        setState(() {
          errorMessage = 'Erreur ${response.statusCode} lors du chargement des produits.';
          isLoading = false;
        });
      }
    } catch (e) {
      setState(() {
        errorMessage = 'Erreur de connexion à l’API : $e';
        isLoading = false;
      });
    }
  }

  Future<void> _logout() async {
    final apiKey = await _secureStorage.read(key: 'api_key');
    if (apiKey != null) {
      try {
        await http.post(
          Uri.parse('https://payetonkawa-api.onrender.com/api/logout'),
          headers: {
            'Content-Type': 'application/json',
            'x-api-key': apiKey,
          },
        );
      } catch (_) {
        // Ignorer les erreurs de déconnexion silencieusement
      }
    }

    await _secureStorage.delete(key: 'api_key');

    Navigator.of(context).pushAndRemoveUntil(
      MaterialPageRoute(
        builder: (_) => const AuthenticationPage(),
        settings: const RouteSettings(arguments: "Déconnexion réussie, à bientôt"),
      ),
          (route) => false,
    );

  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Liste des produits'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: _logout,
          ),
        ],
      ),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : errorMessage.isNotEmpty
          ? Center(child: Text(errorMessage))
          : ListView.builder(
        padding: const EdgeInsets.all(12),
        itemCount: products.length,
        itemBuilder: (context, index) {
          final product = products[index];
          return Card(
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            child: ListTile(
              title: Text(product['name'] ?? 'Nom indisponible'),
              trailing: const Icon(Icons.chevron_right),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => ProductDetailPage(productId: product['id']),
                  ),
                );
              },
            ),
          );
        },
      ),
    );
  }
}