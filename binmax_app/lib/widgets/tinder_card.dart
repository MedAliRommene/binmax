import 'package:flutter_tindercard/flutter_tindercard.dart';

class TinderCard extends StatelessWidget {
  final Product product;
  final VoidCallback onSwipedRight;

  const TinderCard({
    required this.product,
    required this.onSwipedRight,
  });

  @override
  Widget build(BuildContext context) {
    return TinderSwapCard(
      orientation: AmassOrientation.BOTTOM,
      totalNum: 1,
      swipeCompleteCallback: (orientation) {
        if (orientation == AmassSwipeOrientation.RIGHT) {
          onSwipedRight();
        }
      },
      cardBuilder: (context, index) => Card(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
        child: Column(
          children: [
            Expanded(
              child: CachedNetworkImage(
                imageUrl: product.imageUrl,
                fit: BoxFit.cover,
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(product.name, style: TextStyle(fontSize: 20)),
                  Text('${product.price} €', style: TextStyle(fontSize: 18)),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}