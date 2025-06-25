import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'qr_scanner_page.dart';

final FlutterSecureStorage _secureStorage = FlutterSecureStorage();


// 👉 Ajout d’un booléen global contrôlé via --dart-define pour les tests
const bool kUseMockScanner =
bool.fromEnvironment('USE_MOCK_SCANNER', defaultValue: false);

class AuthenticationPage extends StatefulWidget {
  const AuthenticationPage({Key? key}) : super(key: key);

  @override
  State<AuthenticationPage> createState() => _AuthenticationPageState();
}

class _AuthenticationPageState extends State<AuthenticationPage> {
  final TextEditingController emailController = TextEditingController();
  final TextEditingController firstNameController = TextEditingController();
  final TextEditingController lastNameController = TextEditingController();

  String message = '';
  bool isLoading = false;
  bool _initialized = false;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    if (!_initialized) {
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

  Future<void> _wakeUpServer() async {
    try {
      final response = await http.get(Uri.parse('https://payetonkawa-api.onrender.com/'));
      debugPrint("Wake-up status: ${response.statusCode}");
    } catch (e) {
      debugPrint("Wake-up failed: $e");
    }
  }

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
        body: json.encode({'email': email,'first_name': firstNameController.text.trim(),
          'last_name': lastNameController.text.trim(),}),
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

  Future<void> _scanQRCodeAndAuthenticate() async {
    // ✅ Réveil du backend
    await _wakeUpServer();

    String? scannedKey;

    // 👉 Utilisation d’un mock si le test le demande
    if (kUseMockScanner) {
      scannedKey = 'mock-api-key';
      debugPrint("✅ Mode test activé : clé mockée injectée");
    } else {
      scannedKey = await Navigator.push<String?>(
        context,
        MaterialPageRoute(builder: (_) => const QRScannerPage()),
      );
    }

    if (scannedKey != null && scannedKey.isNotEmpty) {
      await _authenticateUser(scannedKey);
    }
  }

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
        await _secureStorage.write(key: 'api_key', value: apiKey);
        setState(() => message = 'Authentification réussie !');
        Navigator.pushReplacementNamed(
          context,
          '/products',
          arguments: apiKey,
        );
      } else {
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
                if (kUseMockScanner)
                  const Padding(
                    padding: EdgeInsets.only(top: 8.0),
                    child: Text(
                      '🔧 Mode TEST actif (clé mockée)',
                      style: TextStyle(color: Colors.orange, fontSize: 12),
                    ),
                  ),
                const SizedBox(height: 20),
              ],
              TextField(
                controller: firstNameController,
                decoration: const InputDecoration(labelText: 'Prénom'),
              ),
              TextField(
                controller: lastNameController,
                decoration: const InputDecoration(labelText: 'Nom'),
              ),
              TextField(
                controller: emailController,
                decoration: const InputDecoration(labelText: 'Email'),
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