import 'package:flutter/material.dart';
import '../../models/bill.dart';
import '../../utils/helpers.dart';
import '../../config/theme.dart';

class MonthlySummaryChart extends StatelessWidget {
  final double totalAmount;
  final Map<BillCategory, double> categoryBreakdown;

  const MonthlySummaryChart({
    Key? key,
    required this.totalAmount,
    required this.categoryBreakdown,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Total Due',
                      style: TextStyle(
                        fontSize: 14,
                        color: Colors.grey[600],
                      ),
                    ),
                    SizedBox(height: 4),
                    Text(
                      Helpers.formatCurrency(totalAmount),
                      style: TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
                Icon(
                  Icons.pie_chart,
                  size: 48,
                  color: Theme.of(context).primaryColor.withOpacity(0.3),
                ),
              ],
            ),
            SizedBox(height: 20),
            Text(
              'By Category',
              style: TextStyle(
                fontSize: 12,
                color: Colors.grey[600],
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 12),
            ...categoryBreakdown.entries.map((entry) {
              final percentage = totalAmount > 0
                  ? (entry.value / totalAmount * 100).toStringAsFixed(0)
                  : '0';
              final categoryName = entry.key.toString().split('.').last;
              final color = AppTheme.categoryColors[categoryName]!;

              return Padding(
                padding: EdgeInsets.only(bottom: 8),
                child: Row(
                  children: [
                    Container(
                      width: 12,
                      height: 12,
                      decoration: BoxDecoration(
                        color: color,
                        borderRadius: BorderRadius.circular(3),
                      ),
                    ),
                    SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        categoryName.capitalize(),
                        style: TextStyle(fontSize: 14),
                      ),
                    ),
                    Text(
                      '$percentage%',
                      style: TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    SizedBox(width: 8),
                    Text(
                      Helpers.formatCurrency(entry.value),
                      style: TextStyle(
                        fontSize: 14,
                        color: Colors.grey[600],
                      ),
                    ),
                  ],
                ),
              );
            }),
          ],
        ),
      ),
    );
  }
}

extension StringExtension on String {
  String capitalize() {
    return "${this[0].toUpperCase()}${this.substring(1)}";
  }
}