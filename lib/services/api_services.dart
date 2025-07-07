import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;

/// Cette fonction récupère le détail d’un produit à partir de l’API backend.
/// ⚠️ Correction : on ajoute l’en-tête 'x-api-key' récupéré dans le secure storage,
/// pour que l’API autorise la requête (sinon elle renvoie 401 Unauthorized).
Future<Map<String, dynamic>?> fetchProductDetail(int productId, {http.Client? client}) async {
  final httpClient = client ?? http.Client();
  final apiUrl = 'https://payetonkawa-api.onrender.com/api/revendeurs/products/$productId';

  // ✅ Récupère la clé d’API stockée dans le SecureStorage (injection auth côté front)
  final storage = const FlutterSecureStorage();
  final apiKey = await storage.read(key: 'api_key');

  final response = await httpClient.get(
    Uri.parse(apiUrl),
    headers: {
      'Content-Type': 'application/json',
      if (apiKey != null) 'x-api-key': apiKey, // ✅ Ajoute la clé API à la requête
    },
  );

  if (response.statusCode == 200) {
    final data = json.decode(response.body) as Map<String, dynamic>;
    print("DEBUG Product Detail reçu : $data");
    return data;
  } else {
    print('Erreur récupération du produit : ${response.statusCode}');
    return null;
  }
}
