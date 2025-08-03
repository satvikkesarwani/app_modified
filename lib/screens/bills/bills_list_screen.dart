        ],
      ),
      body: Column(
        children: [
          // Search bar
          Padding(
            padding: EdgeInsets.all(16),
            child: TextField(
              controller: _searchController,
              decoration: InputDecoration(
                hintText: 'Search bills...',
                prefixIcon: Icon(Icons.search),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
                contentPadding: EdgeInsets.symmetric(horizontal: 16),
              ),
              onChanged: (value) {
                billProvider.setSearchQuery(value);
              },
            ),
          ),

          // Category filters
          Container(
            height: 50,
            child: ListView(
              scrollDirection: Axis.horizontal,
              padding: EdgeInsets.symmetric(horizontal: 16),
              children: [
                BillFilterChip(
                  label: 'All',
                  isSelected: billProvider._selectedCategory == null,
                  onSelected: () {
                    billProvider.setSelectedCategory(null);
                  },
                ),
                ...BillCategory.values.map((category) => Padding(
                  padding: EdgeInsets.only(left: 8),
                  child: BillFilterChip(
                    label: category.toString().split('.').last.capitalize(),
                    isSelected: billProvider._selectedCategory == category,
                    onSelected: () {
                      billProvider.setSelectedCategory(category);
                    },
                  ),
                )),
              ],
            ),
          ),
          SizedBox(height: 16),

          // Bills list
          Expanded(
            child: billProvider.isLoading
                ? Center(child: CircularProgressIndicator())
                : billProvider.filteredBills.isEmpty
                    ? Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(
                              Icons.receipt_long,
                              size: 64,
                              color: Colors.grey,
                            ),
                            SizedBox(height: 16),
                            Text(
                              'No bills found',
                              style: TextStyle(
                                fontSize: 18,
                                color: Colors.grey,
                              ),
                            ),
                            SizedBox(height: 8),
                            ElevatedButton(
                              onPressed: () {
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder: (context) => AddEditBillScreen(),
                                  ),
                                );
                              },
                              child: Text('Add Your First Bill'),
                            ),
                          ],
                        ),
                      )
                    : RefreshIndicator(
                        onRefresh: () => billProvider.fetchBills(),
                        child: ListView.builder(
                          padding: EdgeInsets.all(16),
                          itemCount: billProvider.filteredBills.length,
                          itemBuilder: (context, index) {
                            final bill = billProvider.filteredBills[index];
                            return Padding(
                              padding: EdgeInsets.only(bottom: 8),
                              child: BillListItem(
                                bill: bill,
                                onTap: () {
                                  Navigator.push(
                                    context,
                                    MaterialPageRoute(
                                      builder: (context) => AddEditBillScreen(
                                        bill: bill,
                                      ),
                                    ),
                                  );
                                },
                                onDelete: () async {
                                  final confirmed = await showDialog<bool>(
                                    context: context,
                                    builder: (context) => AlertDialog(
                                      title: Text('Delete Bill'),
                                      content: Text('Are you sure you want to delete this bill?'),
                                      actions: [
                                        TextButton(
                                          onPressed: () => Navigator.pop(context, false),
                                          child: Text('Cancel'),
                                        ),
                                        TextButton(
                                          onPressed: () => Navigator.pop(context, true),
                                          child: Text('Delete'),
                                          style: TextButton.styleFrom(
                                            foregroundColor: Colors.red,
                                          ),
                                        ),
                                      ],
                                    ),
                                  );

                                  if (confirmed == true) {
                                    await billProvider.deleteBill(bill.id!);
                                  }
                                },
                                onMarkPaid: () async {
                                  await billProvider.markAsPaid(bill.id!);
                                  ScaffoldMessenger.of(context).showSnackBar(
                                    SnackBar(
                                      content: Text('Bill marked as paid'),
                                      backgroundColor: Colors.green,
                                    ),
                                  );
                                },
                              ),
                            );
                          },
                        ),
                      ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => AddEditBillScreen(),
            ),
          );
        },
        child: Icon(Icons.add),
      ),
    );
  }
}

extension StringExtension on String {
  String capitalize() {
    return "${this[0].toUpperCase()}${this.substring(1)}";
  }
}import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../models/bill.dart';
import '../../providers/bill_provider.dart';
import '../../widgets/bills/bill_list_item.dart';
import '../../widgets/bills/bill_filter_chip.dart';
import 'add_edit_bill_screen.dart';

class BillsListScreen extends StatefulWidget {
  @override
  _BillsListScreenState createState() => _BillsListScreenState();
}

class _BillsListScreenState extends State<BillsListScreen> {
  final _searchController = TextEditingController();

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final billProvider = context.watch<BillProvider>();

    return Scaffold(
      appBar: AppBar(
        title: Text('My Bills'),
        actions: [
          IconButton(
            icon: Icon(Icons.search),
            onPressed: () {
              // Toggle search
            },
          ),
        ],