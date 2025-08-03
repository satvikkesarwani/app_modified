class Bill {
  final String? id;
  final String name;
  final double amount;
  final DateTime dueDate;
  final BillCategory category;
  final BillFrequency frequency;
  final bool isPaid;
  final String? notes;
  final DateTime? createdAt;
  final ReminderPreferences? reminderPreferences;

  Bill({
    this.id,
    required this.name,
    required this.amount,
    required this.dueDate,
    required this.category,
    required this.frequency,
    this.isPaid = false,
    this.notes,
    this.createdAt,
    this.reminderPreferences,
  });

  factory Bill.fromJson(Map<String, dynamic> json) {
    return Bill(
      id: json['id'],
      name: json['name'],
      amount: json['amount'].toDouble(),
      dueDate: DateTime.parse(json['due_date']),
      category: BillCategory.values.firstWhere(
        (e) => e.toString().split('.').last == json['category'],
      ),
      frequency: BillFrequency.values.firstWhere(
        (e) => e.toString().split('.').last == json['frequency'],
      ),
      isPaid: json['is_paid'] ?? false,
      notes: json['notes'],
      createdAt: json['created_at'] != null 
          ? DateTime.parse(json['created_at']) 
          : null,
      reminderPreferences: json['reminder_preferences'] != null
          ? ReminderPreferences.fromJson(json['reminder_preferences'])
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'amount': amount,
      'due_date': dueDate.toIso8601String(),
      'category': category.toString().split('.').last,
      'frequency': frequency.toString().split('.').last,
      'is_paid': isPaid,
      'notes': notes,
      'created_at': createdAt?.toIso8601String(),
      'reminder_preferences': reminderPreferences?.toJson(),
    };
  }

  Bill copyWith({
    String? id,
    String? name,
    double? amount,
    DateTime? dueDate,
    BillCategory? category,
    BillFrequency? frequency,
    bool? isPaid,
    String? notes,
    DateTime? createdAt,
    ReminderPreferences? reminderPreferences,
  }) {
    return Bill(
      id: id ?? this.id,
      name: name ?? this.name,
      amount: amount ?? this.amount,
      dueDate: dueDate ?? this.dueDate,
      category: category ?? this.category,
      frequency: frequency ?? this.frequency,
      isPaid: isPaid ?? this.isPaid,
      notes: notes ?? this.notes,
      createdAt: createdAt ?? this.createdAt,
      reminderPreferences: reminderPreferences ?? this.reminderPreferences,
    );
  }
}

enum BillCategory { utilities, rent, insurance, subscription, other }
enum BillFrequency { once, weekly, monthly, quarterly, yearly }

class ReminderPreferences {
  final bool enableWhatsApp;
  final bool enableCall;
  final bool enableSMS;
  final bool enableLocalNotification;

  ReminderPreferences({
    this.enableWhatsApp = true,
    this.enableCall = false,
    this.enableSMS = false,
    this.enableLocalNotification = true,
  });

  factory ReminderPreferences.fromJson(Map<String, dynamic> json) {
    return ReminderPreferences(
      enableWhatsApp: json['enable_whatsapp'] ?? true,
      enableCall: json['enable_call'] ?? false,
      enableSMS: json['enable_sms'] ?? false,
      enableLocalNotification: json['enable_local_notification'] ?? true,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'enable_whatsapp': enableWhatsApp,
      'enable_call': enableCall,
      'enable_sms': enableSMS,
      'enable_local_notification': enableLocalNotification,
    };
  }
}