import 'dart:convert';
    import 'package:http/http.dart' as http;
    import 'package:shared_preferences/shared_preferences.dart';
    import '../models/user.dart';
    import '../models/product.dart';
    import '../models/cart.dart';

    class ApiService {
      static const String baseUrl = 'http://localhost:8000/api/';
      static String? _token;

      static Future<void> initializeToken() async {
        final prefs = await SharedPreferences.getInstance();
        _token = prefs.getString('token');
      }

      static Future<User> login(String username, String password) async {
        final tokenResponse = await http.post(
          Uri.parse('${baseUrl}token/'),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({'username': username, 'password': password}),
        );

        if (tokenResponse.statusCode == 200) {
          final tokenData = jsonDecode(tokenResponse.body);
          _token = tokenData['access'];
          final prefs = await SharedPreferences.getInstance();
          await prefs.setString('token', _token!);
          print('Token acquired: $_token');

          final userResponse = await http.get(
            Uri.parse('${baseUrl}users/users/me/'),
            headers: {
              'Authorization': 'Bearer $_token',
              'Content-Type': 'application/json',
            },
          );

          if (userResponse.statusCode == 200) {
            final userData = jsonDecode(userResponse.body);
            return User.fromJson(userData);
          } else {
            print('User fetch error: ${userResponse.body}');
            throw Exception('Failed to fetch user details: ${userResponse.body}');
          }
        } else {
          print('Login error: ${tokenResponse.body}');
          throw Exception('Login failed: ${tokenResponse.body}');
        }
      }

      static Future<List<Product>> getProducts() async {
        final response = await http.get(
          Uri.parse('${baseUrl}products/products/'),
          headers: {'Authorization': 'Bearer $_token'},
        );
        if (response.statusCode == 200) {
          final data = jsonDecode(response.body) as List;
          return data.map((json) => Product.fromJson(json)).toList();
        } else {
          throw Exception('Failed to load products: ${response.body}');
        }
      }

      static Future<Cart> getCart() async {
        final response = await http.get(
          Uri.parse('${baseUrl}orders/carts/'),
          headers: {'Authorization': 'Bearer $_token'},
        );
        if (response.statusCode == 200) {
          final data = jsonDecode(response.body)[0]; // Assuming single cart per user
          return Cart.fromJson(data);
        } else {
          throw Exception('Failed to load cart: ${response.body}');
        }
      }

      static Future<void> addToCart(int productId, int quantity) async {
        final response = await http.post(
          Uri.parse('${baseUrl}orders/carts/add_item/'),
          headers: {
            'Authorization': 'Bearer $_token',
            'Content-Type': 'application/json',
          },
          body: jsonEncode({'product': productId, 'quantity': quantity}),
        );
        if (response.statusCode != 201) {
          throw Exception('Failed to add to cart: ${response.body}');
        }
      }

      static Future<void> checkout(String deliveryType, String deliveryAddress) async {
        final cart = await getCart();
        final response = await http.post(
          Uri.parse('${baseUrl}orders/carts/${cart.id}/checkout/'),
          headers: {
            'Authorization': 'Bearer $_token',
            'Content-Type': 'application/json',
          },
          body: jsonEncode({'delivery_type': deliveryType, 'delivery_address': deliveryAddress}),
        );
        if (response.statusCode != 201) {
          throw Exception('Checkout failed: ${response.body}');
        }
      }
    }