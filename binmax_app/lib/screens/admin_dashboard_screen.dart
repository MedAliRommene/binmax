import 'package:flutter/material.dart';

class AdminDashboardScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Admin Dashboard')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Admin Panel'),
            ElevatedButton(
              onPressed: () {
                // Add navigation to user/product management screens
              },
              child: Text('Manage Users'),
            ),
            ElevatedButton(
              onPressed: () {
                // Add navigation to product management
              },
              child: Text('Manage Products'),
            ),
          ],
        ),
      ),
    );
  }
}