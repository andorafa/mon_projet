import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

import 'package:test_app/main.dart' as app;

void main() {
  // 🔁 Initialise le binding pour les tests d’intégration
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('Flow complet: chargement page + navigation', (WidgetTester tester) async {
    print('🔍 DÉMARRAGE DU TEST');

    // 🚀 Lance l'application complète
    app.main();
    await tester.pumpAndSettle();
    print('✅ App lancée');

    // ✅ Vérifie la présence des textes initiaux
    expect(find.text('Inscription / Connexion'), findsOneWidget);
    expect(find.text("S'inscrire et recevoir le QR Code"), findsOneWidget);

    print('✅ Page d\'accueil OK');

    // 🧭 Simule un clic vers le scanner
    await tester.tap(find.text('Se connecter (scanner QR Code)'));
    await tester.pumpAndSettle();
    print('✅ Navigation vers la page de scanner terminée');

    // 🔍 Affiche tous les textes visibles pour debug
    final allTexts = find.byType(Text);
    for (final element in allTexts.evaluate()) {
      final widget = element.widget as Text;
      print('🧐 TEXTE VISIBLE: "${widget.data}"');
    }

    // ✅ Vérifie que le texte lié à la clé d'authentification est bien affiché
    expect(
      find.byWidgetPredicate((widget) =>
      widget is Text &&
          widget.data != null &&
          widget.data!.contains("clé d'authentification")),
      findsOneWidget,
      reason: 'La page scanner devrait afficher un texte contenant "clé d\'authentification"',
    );

    print('✅ Texte "clé d\'authentification" trouvé');

    // 🔙 Simule un retour arrière (équivalent bouton Android retour)
    await tester.pageBack();
    await tester.pumpAndSettle();

    // 🧾 Vérifie qu'on est bien revenu à l'écran de départ
    expect(find.text("S'inscrire et recevoir le QR Code"), findsOneWidget);

    print('✅ Retour à l\'écran d\'accueil confirmé');
    print('🎉 TEST TERMINÉ AVEC SUCCÈS');
  });
}
