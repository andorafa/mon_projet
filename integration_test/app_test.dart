import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:test_app/main.dart' as app;
import 'package:http/http.dart' as http;
import 'dart:convert';

/// 🧪 MockClient qui intercepte les appels HTTP du front
class MockClient extends http.BaseClient {
  final http.Client _inner = http.Client();

  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) async {
    // 🔹 Mock POST /api/revendeurs/authenticate
    if (request.url.path.endsWith('/api/revendeurs/authenticate')) {
      final mockResponse = json.encode({'message': 'Authentification réussie'});
      final encoded = utf8.encode(mockResponse);
      return http.StreamedResponse(
        Stream.value(encoded),
        200,
        headers: {
          'content-type': 'application/json; charset=utf-8',
          'content-length': encoded.length.toString(),
        },
      );
    }

    // 🔹 Mock GET /api/revendeurs/products
    if (request.url.path.endsWith('/api/revendeurs/products')) {
      final productsJson = json.encode([
        {
          'id': 1,
          'name': 'Produit Mock 1',
          'description': 'Description produit 1',
          'price': 5.0,
          'model_url': 'https://mock.glb'
        },
        {
          'id': 2,
          'name': 'Produit Mock 2',
          'description': 'Description produit 2',
          'price': 7.5,
          'model_url': 'https://mock.glb'
        }
      ]);
      final encoded = utf8.encode(productsJson);
      return http.StreamedResponse(
        Stream.value(encoded),
        200,
        headers: {
          'content-type': 'application/json; charset=utf-8',
          'content-length': encoded.length.toString(),
        },
      );
    }

    return _inner.send(request);
  }
}

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('Flow complet: accueil -> inscription -> navigation scanner', (WidgetTester tester) async {
    print('🔍 DÉBUT DU TEST');

    final mockClient = MockClient();
    app.main(httpClient: mockClient); // ⬅️ Lance l’app avec le MockClient
    await tester.pumpAndSettle();

    // Vérifie la page d'accueil
    expect(find.text('Commencer'), findsOneWidget);
    await tester.tap(find.text('Commencer'));
    await tester.pumpAndSettle();

    // Vérifie la page d'inscription
    expect(find.text("Inscription / Connexion"), findsOneWidget);

    // Remplit le formulaire
    await tester.enterText(find.byKey(const Key('emailField')), 'testuser+${DateTime.now().millisecondsSinceEpoch}@example.com');
    await tester.enterText(find.bySemanticsLabel('Prénom'), 'Test');
    await tester.enterText(find.bySemanticsLabel('Nom'), 'User');

    // Clique sur "S'inscrire"
    await tester.tap(find.text("S'inscrire et recevoir le QR Code"));
    await tester.pumpAndSettle(const Duration(seconds: 2));

    // Clique sur "Se connecter"
    await tester.tap(find.text("Se connecter (scanner QR Code)"));
    await tester.pumpAndSettle();

    // Attente pour la navigation
    await tester.pumpAndSettle(const Duration(seconds: 5));

    // ✅ Vérifie que la page des produits mockés est affichée
    expect(
      find.byKey(const Key('productListPage')),
      findsOneWidget,
      reason: 'La page Liste des produits devrait être affichée',
    );

    // Vérifie qu’au moins un produit mocké est affiché
    expect(find.textContaining('Produit Mock'), findsWidgets);
  });
}
