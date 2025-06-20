import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:test_app/pages/product_list_page.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

/// 🧪 Client HTTP mocké — remplace l’appel à l’API produits
class MockClient extends http.BaseClient {
  final http.Client _inner = http.Client();

  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) {
    if (request.url.path.contains('/api/revendeurs/products')) {
      // 🔹 JSON mocké avec caractères accentués
      final productsJson = json.encode([
        {
          'id': 1,
          'name': 'Café Moka',
          'description': 'Doux et fruité',
          'price': 6.5,
          'model_url': 'https://test.glb'
        },
        {
          'id': 2,
          'name': 'Café Robusta',
          'description': 'Corsé',
          'price': 4.2,
          'model_url': 'https://test.glb'
        }
      ]);

      print('📦 Mock API appelée. Réponse : $productsJson');

      // ✅ Encodage UTF-8 explicite pour éviter l’affichage "CafÃ©"
      final encodedBody = utf8.encode(productsJson);
      return Future.value(http.StreamedResponse(
        Stream.value(encodedBody),
        200,
        headers: {
          'content-type': 'application/json; charset=utf-8',
          'content-length': encodedBody.length.toString(),
        },
      ));
    }

    // Sinon, comportement par défaut
    return _inner.send(request);
  }
}

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('Liste des produits mockée s’affiche', (WidgetTester tester) async {
    print('🔍 DÉBUT DU TEST');

    // 🗝️ Simule la clé d’authentification
    const testApiKey = 'mock-api-key';
    final storage = const FlutterSecureStorage();
    await storage.write(key: 'api_key', value: testApiKey);

    print('✅ MockClient créé.');

    final mockClient = MockClient();

    // 🧪 Injection du MockClient dans ProductListPage
    await tester.pumpWidget(
      MaterialApp(
        home: ProductListPage(httpClient: mockClient),
      ),
    );

    print('✅ Widget initial pompé.');
    await tester.pumpAndSettle();
    print('✅ pumpAndSettle terminé.');

    // 🔍 Debug : afficher tous les textes visibles
    final allTexts = find.byType(Text);
    for (final element in allTexts.evaluate()) {
      final widget = element.widget as Text;
      print('🧐 TEXTE RENDU: "${widget.data}"');
    }

    // ✅ Test avec Predicate plus souple (évite les soucis d’accents, style, etc.)
    expect(
      find.byWidgetPredicate(
            (widget) => widget is Text && widget.data?.contains('Café Moka') == true,
      ),
      findsOneWidget,
      reason: 'Le produit "Café Moka" devrait apparaître',
    );

    expect(
      find.byWidgetPredicate(
            (widget) => widget is Text && widget.data?.contains('Café Robusta') == true,
      ),
      findsOneWidget,
      reason: 'Le produit "Café Robusta" devrait apparaître',
    );
  });
}
