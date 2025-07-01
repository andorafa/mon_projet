import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:test_app/pages/authentication_page.dart';

void main() {
  testWidgets('Affiche le champ email et les boutons', (WidgetTester tester) async {
    await tester.pumpWidget(const MaterialApp(home: AuthenticationPage()));

    expect(find.bySemanticsLabel('Prénom'), findsOneWidget);
    expect(find.bySemanticsLabel('Nom'), findsOneWidget);
    expect(find.bySemanticsLabel('Email'), findsOneWidget); // ✅ corrigé ici
    expect(find.text("S'inscrire et recevoir le QR Code"), findsOneWidget);
    expect(find.text('Se connecter (scanner QR Code)'), findsOneWidget);
  });
}
