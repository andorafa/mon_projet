import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:test_app/pages/product_list_page.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

/// ✅ MockClient personnalisé pour intercepter l'appel API
class MockClient extends http.BaseClient {
  final http.Client _inner = http.Client();

  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) {
    if (request.url.path.contains('/api/revendeurs/products')) {
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

      final mockResponse = http.Response(productsJson, 200);
      return Future.value(http.StreamedResponse(
        Stream.value(utf8.encode(mockResponse.body)),
        mockResponse.statusCode,
        headers: mockResponse.headers,
      ));
    }
    return _inner.send(request);
  }
}

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('Liste des produits mockée s’affiche', (WidgetTester tester) async {
    print('🔍 DÉBUT DU TEST');

    const testApiKey = 'mock-api-key';
    final storage = const FlutterSecureStorage();
    await storage.write(key: 'api_key', value: testApiKey);

    print('✅ MockClient créé.');

    final mockClient = MockClient();

    /// ✅ Lancement de la page avec injection du client mocké
    await tester.pumpWidget(
      MaterialApp(
        home: ProductListPage(httpClient: mockClient),
      ),
    );

    print('✅ Widget initial pompé.');

    await tester.pumpAndSettle();
    print('✅ pumpAndSettle terminé.');

    // 🧪 Étape de debug — Affiche tous les widgets Text visibles
    final allTexts = find.byType(Text);
    for (final element in allTexts.evaluate()) {
      final widget = element.widget as Text;
      print('🧐 TEXTE RENDU: "${widget.data}"');
    }

    // ✅ Remplace find.text() par une méthode plus robuste (qui ignore les petits écarts)
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
