import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:test_app/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  const useMockScanner = bool.fromEnvironment('USE_MOCK_SCANNER', defaultValue: false);

  testWidgets('Flow complet: inscription + navigation scanner', (WidgetTester tester) async {
    // Lance l’application
    app.main();
    await tester.pumpAndSettle();

    // Vérifie la page d’accueil
    expect(find.text('Inscription / Connexion'), findsOneWidget);
    expect(find.text("S'inscrire et recevoir le QR Code"), findsOneWidget);

    // Remplit les champs d’inscription
    await tester.enterText(find.bySemanticsLabel('Prénom'), 'Test');
    await tester.enterText(find.bySemanticsLabel('Nom'), 'User');
    await tester.enterText(find.bySemanticsLabel('Email'), 'testuser+${DateTime.now().millisecondsSinceEpoch}@example.com');

    // Clique sur "S'inscrire"
    await tester.tap(find.text("S'inscrire et recevoir le QR Code"));
    await tester.pumpAndSettle(const Duration(seconds: 2));

    // Vérifie message de confirmation
    expect(
      find.textContaining("Inscription réussie"),
      findsOneWidget,
      reason: 'Le message de succès doit s’afficher',
    );

    // Appuie sur "Se connecter (scanner QR Code)"
    await tester.tap(find.text("Se connecter (scanner QR Code)"));
    await tester.pumpAndSettle();

    if (useMockScanner) {
      expect(
        find.textContaining("Clé mockée"),
        findsNothing,
        reason: "Avec mock, il ne devrait pas y avoir de scan réel",
      );
    } else {
      expect(
        find.textContaining("Scannez votre QR Code"),
        findsOneWidget,
        reason: "Avec scan réel, le texte d’aide doit être visible",
      );
    }

    // Retour à l’écran précédent
    await tester.tap(find.byType(BackButton));
    await tester.pumpAndSettle();

    // Reviens à l’accueil
    expect(find.text("S'inscrire et recevoir le QR Code"), findsOneWidget);
  });
}
