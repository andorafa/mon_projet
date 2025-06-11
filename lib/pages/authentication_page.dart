import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'qr_scanner_page.dart';
// Instance SecureStorage pour garder la clé API en local
final FlutterSecureStorage _secureStorage = FlutterSecureStorage();

class AuthenticationPage extends StatefulWidget {
  const AuthenticationPage({Key? key}) : super(key: key);

  @override
  State<AuthenticationPage> createState() => _AuthenticationPageState();
}

class _AuthenticationPageState extends State<AuthenticationPage> {
  final TextEditingController emailController = TextEditingController();
  String message = '';
  bool isLoading = false;
  bool _initialized = false;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    if (!_initialized) {
      // Récupère l'argument de déconnexion réussie si présent
      final arg = ModalRoute.of(context)?.settings.arguments as String?;
      if (arg != null && arg.isNotEmpty) {
        message = arg;
      }
      _initialized = true;
    }
  }

  @override
  void dispose() {
    emailController.dispose();
    super.dispose();
  }

  /// Inscription : envoi du mail pour générer le QR Code
  Future<void> _registerAndSendQRCode() async {
    final email = emailController.text.trim();
    if (email.isEmpty) {
      setState(() => message = "Veuillez entrer un email.");
      return;
    }
    setState(() {
      isLoading = true;
      message = '';
    });
    final url = Uri.parse('https://payetonkawa-api.onrender.com/api/users');
    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'email': email}),
      );
      if (response.statusCode == 201) {
        setState(() => message = "Inscription réussie ! Vérifiez votre email pour le QR Code.");
      } else {
        setState(() => message = "Erreur d'inscription : ${response.statusCode}");
      }
    } catch (e) {
      setState(() => message = "Erreur de connexion à l'API : $e");
    } finally {
      setState(() => isLoading = false);
    }
  }

  /// Connexion : scan du QR Code et authentification
  Future<void> _scanQRCodeAndAuthenticate() async {
    final scannedKey = await Navigator.push<String?>(
      context,
      MaterialPageRoute(builder: (_) => const QRScannerPage()),
    );
    if (scannedKey != null && scannedKey.isNotEmpty) {
      await _authenticateUser(scannedKey);
    }
  }

  /// Authentification via l'API
  Future<void> _authenticateUser(String apiKey) async {
    setState(() {
      isLoading = true;
      message = '';
    });
    final url = Uri.parse('https://payetonkawa-api.onrender.com/api/revendeurs/authenticate');
    try {
      final response = await http.post(
        url,
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': apiKey,
        },
      );
      if (response.statusCode == 200) {
        // Sauvegarde sécurisée de la clé
        await _secureStorage.write(key: 'api_key', value: apiKey);
        setState(() => message = 'Authentification réussie !');
        Navigator.pushReplacementNamed(
          context,
          '/products',
          arguments: apiKey,
        );
      } else {
        // Lecture du message d'erreur du serveur
        String errMsg;
        try {
          final body = json.decode(response.body) as Map<String, dynamic>;
          errMsg = body['message'] ?? '';
        } catch (_) {
          errMsg = '';
        }
        if (response.statusCode == 401) {
          errMsg = 'Erreur d\'authentification : clé invalide ou manquante, veuillez vous inscrire et recevoir un nouveau QR code.';
        }
        setState(() => message = errMsg.isNotEmpty ? errMsg : 'Erreur d\'authentification : ${response.statusCode}');
      }
    } catch (e) {
      setState(() => message = "Erreur réseau : $e");
    } finally {
      setState(() => isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Inscription / Connexion')),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              if (message.isNotEmpty) ...[
                Text(
                  message,
                  style: TextStyle(
                    color: message.contains('réussie') ? Colors.green : Colors.red,
                    fontSize: 16,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 20),
              ],
              TextField(
                controller: emailController,
                decoration: const InputDecoration(labelText: 'Email'),
                keyboardType: TextInputType.emailAddress,
              ),
              const SizedBox(height: 20),
              if (isLoading)
                const CircularProgressIndicator()
              else ...[
                ElevatedButton(
                  onPressed: _registerAndSendQRCode,
                  child: const Text("S'inscrire et recevoir le QR Code"),
                ),
                const SizedBox(height: 12),
                ElevatedButton(
                  onPressed: _scanQRCodeAndAuthenticate,
                  child: const Text('Se connecter (scanner QR Code)'),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}
