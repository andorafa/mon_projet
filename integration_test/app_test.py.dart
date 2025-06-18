import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

import 'package:test_app/main.dart' as app;


void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('Flow complet: chargement page + navigation', (WidgetTester tester) async {
    app.main();
    await tester.pumpAndSettle();

    // Vérifie que la page d'authentification s'affiche
    expect(find.text('Inscription / Connexion'), findsOneWidget);
    expect(find.text("S'inscrire et recevoir le QR Code"), findsOneWidget);

    // Simule une navigation vers le scanner QR
    await tester.tap(find.text('Se connecter (scanner QR Code)'));
    await tester.pumpAndSettle();

    // Le texte d'aide du scanner devrait apparaître
    expect(find.textContaining("clé d'authentification"), findsOneWidget);

    // Retour arrière (simulateur)
    await tester.pageBack();
    await tester.pumpAndSettle();

    // Toujours sur la page de connexion
    expect(find.text("S'inscrire et recevoir le QR Code"), findsOneWidget);
  });
}
