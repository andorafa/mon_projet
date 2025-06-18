import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:test_app/pages/qr_scanner_page.dart';

void main() {
  testWidgets('Affiche le scanner QR Code', (WidgetTester tester) async {
    await tester.pumpWidget(const MaterialApp(home: QRScannerPage()));

    expect(find.text("Scanner QR Code"), findsOneWidget);
    expect(find.textContaining("clé d'authentification"), findsOneWidget);
  });
}