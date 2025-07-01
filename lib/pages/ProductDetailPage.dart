import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import '../services/api_services.dart';

class ProductDetailPage extends StatelessWidget {
  final int productId;
  final http.Client? httpClient;  // ajout

  const ProductDetailPage({
    Key? key,
    required this.productId,
    this.httpClient,  // ajout
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Détail du Produit')),
      body: FutureBuilder<Map<String, dynamic>?>(
        future: fetchProductDetail(productId, client: httpClient),  // passe httpClient ici
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError || snapshot.data == null) {
            return const Center(child: Text('Erreur de chargement'));
          } else {
            final product = snapshot.data!;
            // 🟢 SURCHARGE model_url selon le produit
            String? modelUrl = product['model_url'];
            if (product['id'] == 5) {
              modelUrl = "https://drive.google.com/uc?export=download&id=1Oq_vVepdhZqbhX2Gm7nVcQqttLrlwZWQ";
            }
            if (product['id'] == 6) {
              modelUrl = "https://drive.google.com/uc?export=download&id=1PsD-QhE0z1R-v4mcY8-W0CFw746oLUXl";
            }
            return Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    product['name'] ?? '',
                    style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                      fontWeight: FontWeight.bold,
                      color: Colors.brown[900],
                    ),
                  ),
                  const SizedBox(height: 10),
                  Divider(color: Colors.brown[300]),
                  const SizedBox(height: 10),
                  Text(
                    "Description",
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.w600,
                      color: Colors.brown[800],
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    product['description'] ?? '',
                    style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                      height: 1.5,
                      color: Colors.grey[800],
                    ),
                  ),
                  const SizedBox(height: 20),
                  Text(
                    "Prix",
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.w600,
                      color: Colors.brown[800],
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    '${product['price']} €',
                    style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                      color: Colors.green[700],
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  const Spacer(),
                  Center(
                    child: ElevatedButton.icon(
                      onPressed: () {
                        if (modelUrl == null || modelUrl.isEmpty) {
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(
                              content: Text("Ce produit n'a pas de modèle AR disponible."),
                              duration: Duration(seconds: 2),
                            ),
                          );
                          return;
                        }
                        Navigator.pushNamed(
                          context,
                          '/ar',
                          arguments: modelUrl,
                        );
                      },
                      icon: const Icon(Icons.view_in_ar),
                      label: const Text("Voir en Réalité Augmentée"),
                      style: ElevatedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
                        textStyle: const TextStyle(fontSize: 16),
                      ),
                    ),
                  )
                ],
              ),
            );
          }
        },
      ),
    );
  }
}
