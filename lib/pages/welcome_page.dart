import 'package:flutter/material.dart';

class WelcomePage extends StatelessWidget {
  final bool hideLogo; // ➕ Flag pour désactiver l'image en test

  const WelcomePage({Key? key, this.hideLogo = false}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        color: Colors.brown[800],
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              if (!hideLogo) // ➕ Affiche l'image seulement si hideLogo est faux
                Image.asset(
                  'assets/images/logo.png',
                  width: 200,
                  fit: BoxFit.contain,
                ),
              const SizedBox(height: 40),
              ElevatedButton(
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
                ),
                onPressed: () => Navigator.pushReplacementNamed(context, '/auth'),
                child: const Text(
                  'Commencer',
                  style: TextStyle(fontSize: 20),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
