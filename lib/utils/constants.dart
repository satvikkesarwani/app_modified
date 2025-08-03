class Constants {
  // App info
  static const String appName = 'Bills Reminder';
  static const String appVersion = '1.0.0';
  
  // Storage keys
  static const String tokenKey = 'auth_token';
  static const String userKey = 'user_data';
  static const String themeKey = 'is_dark_mode';
  
  // Notification channels
  static const String billRemindersChannel = 'bill_reminders';
  static const String instantNotificationsChannel = 'instant_notifications';
  
  // Time constants
  static const int notificationDaysBefore = 3;
  static const int overdueCheckHour = 9; // 9 AM
  
  // UI constants
  static const double borderRadius = 8.0;
  static const double cardElevation = 2.0;
  static const double defaultPadding = 16.0;
  
  // Category icons
  static const Map<String, String> categoryIcons = {
    'utilities': '💡',
    'rent': '🏠',
    'insurance': '🛡️',
    'subscription': '📱',
    'other': '📄',
  };
  
  // Frequency labels
  static const Map<String, String> frequencyLabels = {
    'once': 'One Time',
    'weekly': 'Weekly',
    'monthly': 'Monthly',
    'quarterly': 'Quarterly',
    'yearly': 'Yearly',
  };
}