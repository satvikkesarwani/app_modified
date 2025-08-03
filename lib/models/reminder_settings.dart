class ReminderSettings {
  final bool localNotifications;
  final bool whatsappEnabled;
  final bool callEnabled;
  final int daysBefore;
  final String preferredTime;
  final bool smsEnabled;

  ReminderSettings({
    this.localNotifications = true,
    this.whatsappEnabled = false,
    this.callEnabled = false,
    this.daysBefore = 3,
    this.preferredTime = '09:00',
    this.smsEnabled = false,
  });

  factory ReminderSettings.fromJson(Map<String, dynamic> json) {
    return ReminderSettings(
      localNotifications: json['local_notifications'] ?? true,
      whatsappEnabled: json['whatsapp_enabled'] ?? false,
      callEnabled: json['call_enabled'] ?? false,
      daysBefore: json['days_before'] ?? 3,
      preferredTime: json['preferred_time'] ?? '09:00',
      smsEnabled: json['sms_enabled'] ?? false,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'local_notifications': localNotifications,
      'whatsapp_enabled': whatsappEnabled,
      'call_enabled': callEnabled,
      'days_before': daysBefore,
      'preferred_time': preferredTime,
      'sms_enabled': smsEnabled,
    };
  }

  ReminderSettings copyWith({
    bool? localNotifications,
    bool? whatsappEnabled,
    bool? callEnabled,
    int? daysBefore,
    String? preferredTime,
    bool? smsEnabled,
  }) {
    return ReminderSettings(
      localNotifications: localNotifications ?? this.localNotifications,
      whatsappEnabled: whatsappEnabled ?? this.whatsappEnabled,
      callEnabled: callEnabled ?? this.callEnabled,
      daysBefore: daysBefore ?? this.daysBefore,
      preferredTime: preferredTime ?? this.preferredTime,
      smsEnabled: smsEnabled ?? this.smsEnabled,
    );
  }
}