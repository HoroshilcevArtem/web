// Configuration Template for VPS System
// Скопируйте этот файл и заполните реальные значения

const VPS_CONFIG = {
  // 🤖 Telegram Bot Tokens
  telegram: {
    vpsManagerToken: 'YOUR_VPS_MANAGER_TOKEN_HERE',
    securityMonitorToken: 'YOUR_SECURITY_MONITOR_TOKEN_HERE',
    fileManagerToken: 'YOUR_FILE_MANAGER_TOKEN_HERE',
    chatId: 'YOUR_TELEGRAM_CHAT_ID'
  },

  // 🖥️ Server Configuration
  server: {
    host: 'your-server.com',
    port: 22,
    username: 'admin',
    // Note: Пароль должен храниться в переменных окружения, не в коде!
    passwordEnvVar: 'SERVER_PASSWORD',
    apiUrl: 'https://your-server.com/api',
    apiToken: 'YOUR_API_TOKEN_HERE'
  },

  // 🔐 Security Settings
  security: {
    encryptionEnabled: true,
    encryptionAlgorithm: 'AES-256-GCM',
    useSSL: true,
    verifySSLCertificate: true,
    allowedIPs: [
      '192.168.1.1',
      '10.0.0.1',
      // Добавьте доверенные IP-адреса
    ],
    suspiciousActivityThreshold: 0.8,
    maxFailedLogins: 5,
    sessionTimeout: 3600000 // 1 час в миллисекундах
  },

  // 📊 Monitoring Settings
  monitoring: {
    enabled: true,
    interval: 30000, // 30 секунд
    checkServerHealth: true,
    checkSecurityThreats: true,
    checkDiskSpace: true,
    diskSpaceAlertThreshold: 80, // %
    cpuAlertThreshold: 85, // %
    ramAlertThreshold: 90, // %
    logRetentionDays: 30
  },

  // 📁 File Management Settings
  fileManager: {
    rootPath: '/home',
    maxFileSize: 500, // MB
    maxUploadSize: 1000, // MB
    allowedExtensions: [
      'txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx',
      'jpg', 'png', 'gif', 'zip', 'rar', '7z',
      'log', 'conf', 'json', 'xml', 'sql'
    ],
    autoBackup: true,
    backupInterval: 86400000, // 1 день в миллисекундах
    backupPath: '/backups',
    keepBackupsCount: 10
  },

  // 🔔 Notification Settings
  notifications: {
    enabled: true,
    channels: ['telegram', 'email'], // email requires configuration
    serverDownAlert: true,
    intrusionDetectionAlert: true,
    resourceUsageAlert: true,
    fileChangeAlert: true,
    dailySummary: true,
    summaryTime: '09:00' // HH:MM format
  },

  // 📧 Email Configuration (Optional)
  email: {
    enabled: false,
    service: 'gmail', // или 'smtp'
    from: 'your-email@gmail.com',
    // Используйте переменные окружения для пароля!
    passwordEnvVar: 'EMAIL_PASSWORD',
    recipients: [
      'admin@example.com',
      'support@example.com'
    ]
  },

  // 🌐 API Configuration
  api: {
    baseUrl: 'https://your-api.com',
    version: 'v1',
    timeout: 30000, // ms
    retryAttempts: 3,
    retryDelay: 1000 // ms
  },

  // 🎨 UI Settings
  ui: {
    theme: 'dark', // 'dark' или 'light'
    animationsEnabled: true,
    animationDuration: 0.8, // seconds
    language: 'ru', // 'ru' или 'en'
    dateFormat: 'DD.MM.YYYY',
    timeFormat: 'HH:mm:ss'
  }
};

// ============================================
// 🚀 SETUP INSTRUCTIONS
// ============================================

/*
1. TELEGRAM BOT SETUP:
   - Откройте https://t.me/BotFather
   - Создайте новых ботов для каждой функции
   - Скопируйте токены в соответствующие поля выше
   - Сохраните chat_id вашего Telegram чата

2. SERVER API SETUP:
   - Создайте API эндпоинты на вашем сервере
   - Примеры методов:
     * POST /api/v1/server/restart
     * GET /api/v1/server/status
     * POST /api/v1/files/upload
     * GET /api/v1/files/list
     * POST /api/v1/files/delete
     * GET /api/v1/security/status

3. ENVIRONMENT VARIABLES:
   Создайте .env файл в корне проекта:
   
   SERVER_PASSWORD=your_secure_password
   EMAIL_PASSWORD=your_email_password
   TELEGRAM_BOT_TOKEN=your_bot_token
   API_TOKEN=your_api_token

4. SECURITY RECOMMENDATIONS:
   ✅ Никогда не коммитьте файл .env в Git
   ✅ Используйте HTTPS для всех подключений
   ✅ Регулярно ротируйте токены и пароли
   ✅ Используйте двухфакторную аутентификацию
   ✅ Устанавливайте firewall правила
   ✅ Мониторьте логи на предмет атак

5. DEPLOYMENT:
   - Используйте переменные окружения для чувствительных данных
   - Установите правильные permissions для файлов
   - Используйте HTTPS с валидным сертификатом
   - Включите логирование для аудита
*/

// ============================================
// 💻 EXAMPLE: Initialize System with Config
// ============================================

/*
// В файле vps-animations.js, замените инициализацию на:

const vpsSystem = new VPSSystem({
  encryptionEnabled: VPS_CONFIG.security.encryptionEnabled,
  monitoringInterval: VPS_CONFIG.monitoring.interval,
  vpsManagerToken: VPS_CONFIG.telegram.vpsManagerToken,
  securityToken: VPS_CONFIG.telegram.securityMonitorToken,
  fileManagerToken: VPS_CONFIG.telegram.fileManagerToken,
  apiUrl: VPS_CONFIG.api.baseUrl,
  alertThreshold: VPS_CONFIG.security.suspiciousActivityThreshold
});

// Если используется Node.js/Express:
const express = require('express');
const app = express();

// Загрузка конфига
require('dotenv').config();

const appConfig = {
  ...VPS_CONFIG,
  telegram: {
    ...VPS_CONFIG.telegram,
    vpsManagerToken: process.env.VPS_MANAGER_TOKEN,
    securityMonitorToken: process.env.SECURITY_MONITOR_TOKEN,
    fileManagerToken: process.env.FILE_MANAGER_TOKEN
  },
  server: {
    ...VPS_CONFIG.server,
    password: process.env.SERVER_PASSWORD
  }
};

// Используйте appConfig в вашем приложении
*/

// ============================================
// 📋 API ENDPOINTS EXAMPLES
// ============================================

const API_ENDPOINTS = {
  // Server Management
  'GET /api/v1/server/status': 'Получить статус сервера',
  'POST /api/v1/server/restart': 'Перезагрузить сервер',
  'POST /api/v1/server/shutdown': 'Выключить сервер',
  'GET /api/v1/server/resources': 'Получить использование ресурсов',

  // File Management
  'GET /api/v1/files/list': 'Список файлов в папке',
  'POST /api/v1/files/upload': 'Загрузить файл',
  'DELETE /api/v1/files/:path': 'Удалить файл',
  'GET /api/v1/files/download/:path': 'Скачать файл',

  // Security
  'GET /api/v1/security/status': 'Статус безопасности',
  'GET /api/v1/security/threats': 'Список обнаруженных угроз',
  'GET /api/v1/security/logs': 'Логи безопасности',
  'POST /api/v1/security/scan': 'Запустить сканирование',

  // Backup
  'POST /api/v1/backup/create': 'Создать резервную копию',
  'GET /api/v1/backup/list': 'Список резервных копий',
  'POST /api/v1/backup/restore': 'Восстановить из резервной копии'
};

console.log('VPS Configuration Template loaded');
console.log('⚠️  Заполните все значения перед использованием в production!');

// Export для использования в Node.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { VPS_CONFIG, API_ENDPOINTS };
}
