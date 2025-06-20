import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:test_app/pages/product_list_page.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

// 🔧 MOCK HTTP CLIENT
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
    debugPrint('🔍 DÉBUT DU TEST');

    // 🧪 Injecter le mock HTTP client
    final mockClient = MockClient();
    debugPrint('✅ MockClient créé.');

    // 🧱 pumpWidget avec mock et clé API simulée
    await tester.pumpWidget(
      MaterialApp(
        onGenerateRoute: (_) => MaterialPageRoute(
          builder: (_) => ProductListPage(httpClient: mockClient),
          settings: const RouteSettings(arguments: 'mock-api-key'),
        ),
      ),
    );
    debugPrint('✅ Widget initial pompé.');

    // 🔄 Attendre rendu complet
    await tester.pumpAndSettle();
    debugPrint('✅ pumpAndSettle terminé.');

    // 🔎 Afficher arbre du widget principal
    final scaffoldFinder = find.byType(Scaffold);
    if (scaffoldFinder.evaluate().isEmpty) {
      debugPrint('❌ Aucun Scaffold trouvé dans l’arbre.');
    } else {
      debugPrint('🧱 Scaffold trouvé. Arbre des widgets :');
      debugPrint(tester.element(scaffoldFinder).toStringDeep());
    }

    // 🔍 Vérifier les composants structurels
    expect(find.byType(ListView), findsOneWidget, reason: '📋 Un ListView est attendu.');
    expect(find.byType(Card), findsWidgets, reason: '🃏 Des Cards sont attendues.');

    // ✅ Vérifier que les textes mockés sont bien présents
    expect(find.text('Café Moka'), findsOneWidget, reason: '🔎 "Café Moka" doit être visible.');
    expect(find.text('Café Robusta'), findsOneWidget, reason: '🔎 "Café Robusta" doit être visible.');
    expect(find.text('Doux et fruité'), findsOneWidget, reason: '🔎 Description "Doux et fruité" manquante.');
    expect(find.text('Corsé'), findsOneWidget, reason: '🔎 Description "Corsé" manquante.');

    debugPrint('✅ FIN DU TEST avec succès.');
  });
}
