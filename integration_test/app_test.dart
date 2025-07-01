import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:test_app/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  const useMockScanner = bool.fromEnvironment('USE_MOCK_SCANNER', defaultValue: false);

  testWidgets('Flow complet: accueil -> inscription -> navigation scanner', (WidgetTester tester) async {
    app.main();
    await tester.pumpAndSettle();

    // 🔎 Vérifie qu’on est bien sur la page d’accueil
    expect(find.byType(Image), findsOneWidget);
    expect(find.text('Commencer'), findsOneWidget);

    // 🟢 Clique sur "Commencer" pour aller à la page d’authentification
    await tester.tap(find.text('Commencer'));
    await tester.pumpAndSettle();

    // 🔎 Vérifie la présence du titre de la page d’authentification
    expect(find.text('Inscription / Connexion'), findsOneWidget);

    // Remplit le formulaire
    await tester.enterText(find.bySemanticsLabel('Prénom'), 'Test');
    await tester.enterText(find.bySemanticsLabel('Nom'), 'User');
    await tester.enterText(
      find.byKey(const Key('emailField')),
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
      // ✅ En mode mock : pas de scanner
      expect(find.text("Scanner QR Code"), findsNothing);
      expect(find.textContaining("Clé mockée"), findsNothing);
    } else {
      // ✅ En mode réel : on doit voir le scanner
      expect(find.text("Scanner QR Code"), findsOneWidget);
      expect(find.byKey(const Key('testBackButton')), findsOneWidget);

      // Retour arrière depuis le scanner
      await tester.tap(find.byKey(const Key('testBackButton')));
      await tester.pumpAndSettle();
    }

    // Vérifie qu’on est revenu sur l’écran d’authentification
    expect(find.text("S'inscrire et recevoir le QR Code"), findsOneWidget);
  });
}
