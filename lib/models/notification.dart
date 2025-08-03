class NotificationModel {
  final String? id;
  final String title;
  final String body;
  final NotificationType type;
  final String? billId;
  final DateTime scheduledTime;
  final bool isRead;
  final DateTime? createdAt;

  NotificationModel({
    this.id,
    required this.title,
    required this.body,
    required this.type,
    this.billId,
    required this.scheduledTime,
    this.isRead = false,
    this.createdAt,
  });

  factory NotificationModel.fromJson(Map<String, dynamic> json) {
    return NotificationModel(
      id: json['id'],
      title: json['title'],
      body: json['body'],
      type: NotificationType.values.firstWhere(
        (e) => e.toString().split('.').last == json['type'],
      ),
      billId: json['bill_id'],
      scheduledTime: DateTime.parse(json['scheduled_time']),
      isRead: json['is_read'] ?? false,
      createdAt: json['created_at'] != null 
          ? DateTime.parse(json['created_at']) 
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'body': body,
      'type': type.toString().split('.').last,
      'bill_id': billId,
      'scheduled_time': scheduledTime.toIso8601String(),
      'is_read': isRead,
      'created_at': createdAt?.toIso8601String(),
    };
  }
}

enum NotificationType { 
  billDue, 
  overdue, 
  paymentConfirmation, 
  weeklyReport, 
  monthlyReport 
}