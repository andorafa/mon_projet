import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:test_app/pages/welcome_page.dart'; // importe WelcomePage directement
import 'package:test_app/main.dart' as app;
import 'package:http/http.dart' as http;
import 'dart:convert';

class MockClient extends http.BaseClient {
  final http.Client _inner = http.Client();

  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) async {
    if (request.url.path.endsWith('/api/revendeurs/authenticate')) {
      final mockResponse = json.encode({'message': 'Authentification réussie'});
      final encoded = utf8.encode(mockResponse);
      return http.StreamedResponse(Stream.value(encoded), 200);
    }

    if (request.url.path.endsWith('/api/revendeurs/products')) {
      final productsJson = json.encode([
        {'id': 1, 'name': 'Produit Mock 1', 'description': 'Description 1', 'price': 5.0, 'model_url': 'https://mock.glb'},
        {'id': 2, 'name': 'Produit Mock 2', 'description': 'Description 2', 'price': 7.5, 'model_url': 'https://mock.glb'}
      ]);
      final encoded = utf8.encode(productsJson);
      return http.StreamedResponse(Stream.value(encoded), 200);
    }

    return _inner.send(request);
  }
}

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('Flow complet: accueil -> inscription -> navigation scanner', (WidgetTester tester) async {
    print('🔍 DÉBUT DU TEST');

    final mockClient = MockClient();

    // ➕ Ici on injecte WelcomePage en root avec hideLogo: true
    await tester.pumpWidget(
      MaterialApp(
        home: const WelcomePage(hideLogo: true),
        routes: {
          '/auth': (_) => const Placeholder(), // Fake auth pour le test
          '/products': (_) => const Placeholder(), // Fake page produit pour le test
        },
      ),
    );

    await tester.pumpAndSettle();

    expect(find.text('Commencer'), findsOneWidget);
    await tester.tap(find.text('Commencer'));
    await tester.pumpAndSettle();

    // ➕ Ajoute ici tes étapes suivantes, par ex. simulateur d'inscription, etc.
  });
}
