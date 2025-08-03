import 'package:flutter/material.dart';
import '../../models/bill.dart';
import '../../utils/helpers.dart';

class OverdueBillsAlert extends StatelessWidget {
  final List<Bill> bills;

  const OverdueBillsAlert({Key? key, required this.bills}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final totalOverdue = bills.fold(
      0.0,
      (sum, bill) => sum + bill.amount,
    );

    return Container(
      padding: EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.red.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: Colors.red.withOpacity(0.3),
          width: 1,
        ),
      ),
      child: Row(
        children: [
          Icon(
            Icons.warning_rounded,
            color: Colors.red,
            size: 32,
          ),
          SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  '${bills.length} Overdue Bill${bills.length > 1 ? 's' : ''}',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: Colors.red[900],
                  ),
                ),
                SizedBox(height: 4),
                Text(
                  'Total: ${Helpers.formatCurrency(totalOverdue)}',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.red[700],
                  ),
                ),
              ],
            ),
          ),
          TextButton(
            onPressed: () {
              // Navigate to bills list with overdue filter
            },
            child: Text(
              'View',
              style: TextStyle(
                color: Colors.red,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ],
      ),
    );
  }
}