import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/auth_provider.dart';
import '../../providers/bill_provider.dart';
import '../../widgets/home/upcoming_bills_card.dart';
import '../../widgets/home/quick_actions_row.dart';
import '../../widgets/home/monthly_summary_chart.dart';
import '../../widgets/home/overdue_bills_alert.dart';
import '../bills/add_edit_bill_screen.dart';

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  Widget build(BuildContext context) {
    final authProvider = context.watch<AuthProvider>();
    final billProvider = context.watch<BillProvider>();

    return Scaffold(
      appBar: AppBar(
        title: Text('Bills Reminder'),
        actions: [
          IconButton(
            icon: Icon(Icons.notifications),
            onPressed: () {
              // Navigate to notifications screen
            },
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () => billProvider.fetchBills(),
        child: SingleChildScrollView(
          physics: AlwaysScrollableScrollPhysics(),
          padding: EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Welcome message
              Card(
                child: Padding(
                  padding: EdgeInsets.all(16),
                  child: Row(
                    children: [
                      CircleAvatar(
                        child: Text(
                          authProvider.user?.name[0].toUpperCase() ?? 'U',
                          style: TextStyle(fontSize: 20),
                        ),
                      ),
                      SizedBox(width: 16),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Welcome back,',
                              style: TextStyle(
                                fontSize: 14,
                                color: Colors.grey[600],
                              ),
                            ),
                            Text(
                              authProvider.user?.name ?? 'User',
                              style: TextStyle(
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              SizedBox(height: 16),

              // Overdue bills alert
              if (billProvider.overdueBills.isNotEmpty) ...[
                OverdueBillsAlert(bills: billProvider.overdueBills),
                SizedBox(height: 16),
              ],

              // Quick actions
              QuickActionsRow(
                onAddBill: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => AddEditBillScreen(),
                    ),
                  );
                },
                onViewReports: () {
                  // Navigate to analytics
                },
              ),
              SizedBox(height: 24),

              // Monthly summary
              Text(
                'Monthly Summary',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
              SizedBox(height: 16),
              MonthlySummaryChart(
                totalAmount: billProvider.totalMonthlyAmount,
                categoryBreakdown: billProvider.categoryBreakdown,
              ),
              SizedBox(height: 24),

              // Upcoming bills
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Upcoming Bills',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  TextButton(
                    onPressed: () {
                      // Navigate to bills list
                    },
                    child: Text('See All'),
                  ),
                ],
              ),
              SizedBox(height: 16),

              if (billProvider.isLoading)
                Center(child: CircularProgressIndicator())
              else if (billProvider.upcomingBills.isEmpty)
                Card(
                  child: Padding(
                    padding: EdgeInsets.all(32),
                    child: Center(
                      child: Column(
                        children: [
                          Icon(
                            Icons.check_circle,
                            size: 64,
                            color: Colors.green,
                          ),
                          SizedBox(height: 16),
                          Text(
                            'No upcoming bills',
                            style: TextStyle(fontSize: 16),
                          ),
                        ],
                      ),
                    ),
                  ),
                )
              else
                ...billProvider.upcomingBills.map((bill) => Padding(
                      padding: EdgeInsets.only(bottom: 8),
                      child: UpcomingBillCard(bill: bill),
                    )),
            ],
          ),
        ),
      ),
    );
  }
}