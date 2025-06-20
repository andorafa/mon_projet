import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:test_app/pages/product_list_page.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

// MOCK OVERRIDE
class MockClient extends http.BaseClient {
  final http.Client _inner = http.Client();

  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) {
    if (request.url.path.contains('/api/revendeurs/products')) {
      final productsJson = json.encode([
        {'id': 1, 'name': 'Café Moka', 'description': 'Doux et fruité', 'price': 6.5, 'model_url': 'https://test.glb'},
        {'id': 2, 'name': 'Café Robusta', 'description': 'Corsé', 'price': 4.2, 'model_url': 'https://test.glb'}
      ]);

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
    // Pré-remplir la clé API simulée
    const testApiKey = 'mock-api-key';
    //final storage = const FlutterSecureStorage();
    //await storage.write(key: 'api_key', value: testApiKey);

    // Lancer la page avec un mock client
    http.Client originalClient = http.Client();
    http.Client mockClient = MockClient();
    http.Client? overrideClient = http.Client();

    overrideClient = mockClient;

    //await tester.pumpWidget(
      //MaterialApp(
        //home: ProductListPage(httpClient: MockClient()),
      //),
    //);

    await tester.pumpWidget(
      MaterialApp(
        onGenerateRoute: (_) => MaterialPageRoute(
          builder: (_) => ProductListPage(httpClient: MockClient()),
          settings: const RouteSettings(arguments: 'mock-api-key'),
        ),
      ),
    );



    await tester.pumpAndSettle();

    // Vérifier que les produits mockés sont visibles
    expect(find.text('Café Moka'), findsOneWidget);
    expect(find.text('Café Robusta'), findsOneWidget);
  });
}
