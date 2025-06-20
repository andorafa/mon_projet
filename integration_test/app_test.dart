import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:test_app/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  const useMockScanner = bool.fromEnvironment('USE_MOCK_SCANNER');

  testWidgets('Flow complet: chargement page + navigation', (WidgetTester tester) async {
    // Lance l’application
    app.main();
    await tester.pumpAndSettle();

    // Vérifie qu’on est sur la page d’authentification
    expect(find.text('Inscription / Connexion'), findsOneWidget);
    expect(find.text("S'inscrire et recevoir le QR Code"), findsOneWidget);
    expect(find.text("Se connecter (scanner QR Code)"), findsOneWidget);

    // Simule le clic sur le bouton de scan
    await tester.tap(find.text('Se connecter (scanner QR Code)'));
    await tester.pumpAndSettle();

    // 🔎 Vérifie que le texte d’aide est bien visible dans la page scanner
    if (useMockScanner) {
      expect(find.textContaining("Clé mockée de test"), findsOneWidget);
    } else {
      expect(find.textContaining("Scannez votre QR Code"), findsOneWidget);
    }

    // Simule retour arrière
    await tester.pageBack();
    await tester.pumpAndSettle();

    // Vérifie qu’on est bien revenu à la page d’accueil
    expect(find.text("S'inscrire et recevoir le QR Code"), findsOneWidget);
  });
}
