import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;

import 'pages/ar_view_page.dart';
import 'pages/qr_scanner_page.dart';
import 'pages/authentication_page.dart';
import 'pages/product_list_page.dart';

final secureStorage = FlutterSecureStorage();

void main({http.Client? httpClient}) {
  runApp(PayeTonKawaApp(httpClient: httpClient ?? http.Client()));
}

class PayeTonKawaApp extends StatelessWidget {
  final http.Client httpClient;

  const PayeTonKawaApp({Key? key, required this.httpClient}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'PayeTonKawa',
      theme: ThemeData(primarySwatch: Colors.brown),
      initialRoute: '/',
      onGenerateRoute: (settings) {
        if (settings.name == '/ar') {
          final modelUrl = settings.arguments as String?;
          return MaterialPageRoute(
            builder: (_) => ARViewPage(modelUrl: modelUrl),
          );
        }

        switch (settings.name) {
          case '/':
            return MaterialPageRoute(builder: (_) => const AuthenticationPage());
          case '/products':
          // Transmission correcte du httpClient mocké ici
            return MaterialPageRoute(
              builder: (_) => ProductListPage(httpClient: httpClient),
            );
          case '/scan':
            return MaterialPageRoute(builder: (_) => const QRScannerPage());
          default:
            return null;
        }
      },
    );
  }
}
