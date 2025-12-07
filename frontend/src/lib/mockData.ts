import { Project, FileNode, Variant, StylePreset, DeviceFrame, ConsoleLog } from '@/types';

export const mockProjects: Project[] = [
  {
    id: '1',
    name: 'E-Commerce App',
    description: 'Modern shopping experience with Flutter',
    template: 'material',
    createdAt: new Date('2024-01-15'),
    updatedAt: new Date('2024-01-20'),
  },
  {
    id: '2',
    name: 'Social Media Dashboard',
    description: 'Analytics and content management',
    template: 'minimal',
    createdAt: new Date('2024-01-10'),
    updatedAt: new Date('2024-01-18'),
  },
  {
    id: '3',
    name: 'Fitness Tracker',
    description: 'Health and workout companion app',
    template: 'lovable',
    createdAt: new Date('2024-01-05'),
    updatedAt: new Date('2024-01-16'),
  },
];

export const defaultFileTree: FileNode[] = [
  {
    id: '1',
    name: 'lib',
    type: 'folder',
    children: [
      {
        id: '2',
        name: 'main.dart',
        type: 'file',
        language: 'dart',
        content: `import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'FlutterAI App',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Welcome'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(
              Icons.flutter_dash,
              size: 100,
              color: Colors.deepPurple,
            ),
            const SizedBox(height: 24),
            Text(
              'Hello, FlutterAI!',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
          ],
        ),
      ),
    );
  }
}`,
      },
      {
        id: '3',
        name: 'widgets',
        type: 'folder',
        children: [
          { id: '4', name: 'custom_button.dart', type: 'file', language: 'dart', content: '// Custom button widget' },
          { id: '5', name: 'app_card.dart', type: 'file', language: 'dart', content: '// App card widget' },
        ],
      },
      {
        id: '6',
        name: 'screens',
        type: 'folder',
        children: [
          { id: '7', name: 'home_screen.dart', type: 'file', language: 'dart', content: '// Home screen' },
          { id: '8', name: 'settings_screen.dart', type: 'file', language: 'dart', content: '// Settings screen' },
        ],
      },
    ],
  },
  {
    id: '9',
    name: 'pubspec.yaml',
    type: 'file',
    language: 'yaml',
    content: `name: flutterai_app
description: A new Flutter project.
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.2

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0

flutter:
  uses-material-design: true`,
  },
  {
    id: '10',
    name: 'README.md',
    type: 'file',
    language: 'markdown',
    content: '# FlutterAI Generated App\n\nThis app was generated using FlutterAI Playground.',
  },
];

export const stylePresets: StylePreset[] = [
  { id: 'lovable', name: 'Lovable', description: 'Modern, elegant with smooth animations', icon: '💜' },
  { id: 'material', name: 'Material 3', description: 'Google Material Design guidelines', icon: '🎨' },
  { id: 'minimal', name: 'Minimal', description: 'Clean, simple, distraction-free', icon: '✨' },
  { id: 'playful', name: 'Playful', description: 'Fun, colorful, animated', icon: '🎮' },
];

export const deviceFrames: DeviceFrame[] = [
  { id: 'iphone14', name: 'iPhone 14 Pro', width: 393, height: 852, type: 'phone' },
  { id: 'pixel7', name: 'Pixel 7', width: 412, height: 915, type: 'phone' },
  { id: 'ipadpro', name: 'iPad Pro 11"', width: 834, height: 1194, type: 'tablet' },
  { id: 'galaxy', name: 'Galaxy S23', width: 360, height: 780, type: 'phone' },
];

export const generateMockVariants = (prompt: string): Variant[] => {
  return [
    {
      id: '1',
      code: `// Generated from: "${prompt}"\nimport 'package:flutter/material.dart';\n\nclass GeneratedWidget extends StatelessWidget {\n  @override\n  Widget build(BuildContext context) {\n    return Container(\n      padding: EdgeInsets.all(16),\n      child: Column(\n        children: [\n          Text('Variant A'),\n        ],\n      ),\n    );\n  }\n}`,
      thumbnail: 'variant-a',
      confidence: 0.95,
    },
    {
      id: '2',
      code: `// Generated from: "${prompt}"\nimport 'package:flutter/material.dart';\n\nclass GeneratedWidget extends StatelessWidget {\n  @override\n  Widget build(BuildContext context) {\n    return Card(\n      child: Padding(\n        padding: EdgeInsets.all(20),\n        child: Column(\n          children: [\n            Text('Variant B'),\n          ],\n        ),\n      ),\n    );\n  }\n}`,
      thumbnail: 'variant-b',
      confidence: 0.89,
    },
    {
      id: '3',
      code: `// Generated from: "${prompt}"\nimport 'package:flutter/material.dart';\n\nclass GeneratedWidget extends StatelessWidget {\n  @override\n  Widget build(BuildContext context) {\n    return Material(\n      elevation: 4,\n      borderRadius: BorderRadius.circular(12),\n      child: Container(\n        padding: EdgeInsets.all(24),\n        child: Column(\n          children: [\n            Text('Variant C'),\n          ],\n        ),\n      ),\n    );\n  }\n}`,
      thumbnail: 'variant-c',
      confidence: 0.82,
    },
  ];
};

export const mockConsoleLogs: ConsoleLog[] = [
  { id: '1', type: 'info', message: 'App initialized successfully', timestamp: new Date() },
  { id: '2', type: 'info', message: 'Hot reload triggered', timestamp: new Date() },
  { id: '3', type: 'warning', message: 'Image asset not found, using placeholder', timestamp: new Date() },
];
