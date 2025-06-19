import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:test_app/pages/product_list_page.dart';

void main() {
  testWidgets('Affiche le titre de la page produit', (WidgetTester tester) async {
    await tester.pumpWidget(MaterialApp(home: ProductListPage()));

    expect(find.text('Liste des produits'), findsOneWidget);
  });
}