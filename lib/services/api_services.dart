import 'dart:convert';
import 'package:http/http.dart' as http;

Future<Map<String, dynamic>?> fetchProductDetail(int productId) async {
  final apiUrl = 'https://payetonkawa-api.onrender.com/api/products/$productId';
  final response = await http.get(Uri.parse(apiUrl));

  if (response.statusCode == 200) {
    return json.decode(response.body) as Map<String, dynamic>;
  } else {
    print('Erreur récupération du produit : ${response.statusCode}');
    return null;
  }
}
