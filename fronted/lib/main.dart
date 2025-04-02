import 'package:flutter/material.dart';
import 'chat_screen.dart';

void main() {
  runApp(const MyApp());  // Add 'const' since MyApp has no mutable state
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});  // Add key parameter

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Vizzhy AI Search',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: const ChatScreen(),  // Add 'const' since HomeScreen has no mutable state
    );
  }
}



