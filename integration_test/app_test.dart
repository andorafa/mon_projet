import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:test_app/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  const useMockScanner = bool.fromEnvironment('USE_MOCK_SCANNER', defaultValue: false);

  testWidgets('Flow complet: inscription + navigation scanner', (WidgetTester tester) async {
    app.main();
    await tester.pumpAndSettle();

    // Vérifie l’accueil
    expect(find.text('Inscription / Connexion'), findsOneWidget);
    expect(find.text("S'inscrire et recevoir le QR Code"), findsOneWidget);

    // Remplit le formulaire
    await tester.enterText(find.bySemanticsLabel('Prénom'), 'Test');
    await tester.enterText(find.bySemanticsLabel('Nom'), 'User');
    await tester.enterText(
      find.bySemanticsLabel('Email'),
      'testuser+${DateTime.now().millisecondsSinceEpoch}@example.com',
    );

    // Clique sur le bouton d’inscription
    await tester.tap(find.text("S'inscrire et recevoir le QR Code"));
    await tester.pumpAndSettle(const Duration(seconds: 2));

    expect(find.textContaining("Inscription réussie"), findsOneWidget);

    // Appuie sur le bouton de connexion
    await tester.tap(find.text("Se connecter (scanner QR Code)"));
    await tester.pumpAndSettle();

    if (useMockScanner) {
      // ✅ En mode mock : le scanner n'est pas affiché
      expect(find.text("Scanner QR Code"), findsNothing);
      expect(find.textContaining("Clé mockée"), findsNothing);
    } else {
      // ✅ En mode réel : on vérifie la page scanner
      expect(find.text("Scanner QR Code"), findsOneWidget);
      expect(find.byKey(const Key('testBackButton')), findsOneWidget);

      // Retour arrière
      await tester.tap(find.byKey(const Key('testBackButton')));
      await tester.pumpAndSettle();
    }

    // Vérifie qu'on est de retour sur l’accueil
    expect(find.text("S'inscrire et recevoir le QR Code"), findsOneWidget);
  });
}
