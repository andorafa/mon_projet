import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:test_app/pages/authentication_page.dart';

void main() {
  testWidgets('Affiche le champ email et les boutons', (WidgetTester tester) async {
    await tester.pumpWidget(const MaterialApp(home: AuthenticationPage()));

    // Cherche le champ email par clé
    expect(find.byKey(const Key('emailField')), findsOneWidget);

    expect(find.text("S'inscrire et recevoir le QR Code"), findsOneWidget);
    expect(find.text('Se connecter (scanner QR Code)'), findsOneWidget);
  });
}
