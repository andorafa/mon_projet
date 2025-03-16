import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'qr_scanner_page.dart';

class AuthenticationPage extends StatefulWidget {
  const AuthenticationPage({Key? key}) : super(key: key);

  @override
  State<AuthenticationPage> createState() => _AuthenticationPageState();
}

class _AuthenticationPageState extends State<AuthenticationPage> {
  final TextEditingController emailController = TextEditingController();
  String message = '';
  bool isLoading = false;

  // Inscription : envoi du mail à l'API et réception de la clé d'authentification et du QR Code (envoyé par mail ou inclus dans la réponse)
  Future<void> _registerAndSendQRCode() async {
    final email = emailController.text.trim();
    if (email.isEmpty) {
      setState(() {
        message = "Veuillez entrer un email.";
      });
      return;
    }
    setState(() {
      isLoading = true;
    });
    final url = Uri.parse('https://38cf-2001-861-3a02-a880-5dfd-14ce-366c-f1f1.ngrok-free.app/api/users');
    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'email': email}),
      );
      if (response.statusCode == 201) {
        final data = json.decode(response.body);
        final apiKey = data['api_key'];
        setState(() {
          message = "Inscription réussie ! Un email a été envoyé avec votre QR Code.";
        });
        // Vous pouvez sauvegarder la clé si nécessaire.
      } else {
        setState(() {
          message = "Erreur d'inscription : ${response.statusCode}";
        });
      }
    } catch (e) {
      setState(() {
        message = "Erreur lors de la connexion à l'API: $e";
      });
    }
    setState(() {
      isLoading = false;
    });
  }

  // Connexion via scan du QR Code : on lance le scanner et on envoie la clé scannée à l'API d'authentification.
  Future<void> _scanQRCodeAndAuthenticate() async {
    final scannedKey = await Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => const QRScannerPage()),
    );
    if (scannedKey != null && scannedKey is String) {
      _authenticateUser(scannedKey);
    }
  }

  Future<void> _authenticateUser(String key) async {
    final url = Uri.parse('https://38cf-2001-861-3a02-a880-5dfd-14ce-366c-f1f1.ngrok-free.app/api/revendeurs/authenticate');
    try {
      final response = await http.post(
        url,
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': key,
        },
      );
      if (response.statusCode == 200) {
        setState(() {
          message = 'Authentification réussie !';
        });
        Navigator.pushReplacementNamed(context, '/products', arguments: key);
      } else {
        setState(() {
          message = 'Erreur d’authentification : ${response.statusCode}';
        });
      }
    } catch (e) {
      setState(() {
        message = 'Erreur lors de la connexion à l’API : $e';
      });
    }
  }

  @override
  void dispose() {
    emailController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Inscription / Connexion')),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              TextField(
                controller: emailController,
                decoration: const InputDecoration(labelText: 'Email'),
              ),
              const SizedBox(height: 20),
              isLoading
                  ? const CircularProgressIndicator()
                  : ElevatedButton(
                onPressed: _registerAndSendQRCode,
                child: const Text("S'inscrire et recevoir votre QR Code"),
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: _scanQRCodeAndAuthenticate,
                child: const Text('Se connecter (scanner QR Code)'),
              ),
              const SizedBox(height: 20),
              Text(message),
            ],
          ),
        ),
      ),
    );
  }
}