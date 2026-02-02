// VPS System Usage Examples
// Примеры использования системы управления VPS

// ============================================
// 1️⃣ BASIC INITIALIZATION
// ============================================

console.log('='.repeat(50));
console.log('📚 VPS System Usage Examples');
console.log('='.repeat(50));

// Пример 1: Базовая инициализация
function example_basicInit() {
  const vpsSystem = new VPSSystem({
    encryptionEnabled: true,
    monitoringInterval: 30000,
    apiUrl: 'https://your-server.com/api'
  });

  console.log('\n✅ Пример 1: Базовая инициализация');
  vpsSystem.printSystemInfo();
}

// ============================================
// 2️⃣ VPS MANAGER BOT USAGE
// ============================================

async function example_vpsManagerBot() {
  console.log('\n✅ Пример 2: Использование VPS Manager Bot');

  const vpsManager = new VPSManagerBot({
    token: 'YOUR_BOT_TOKEN',
    apiUrl: 'https://your-server.com/api'
  });

  // 2.1 Подключение к серверу
  console.log('\n📡 Подключение к серверу...');
  const connected = await vpsManager.connectToServer({
    ip: '192.168.1.100',
    port: 22,
    username: 'admin'
  });
  console.log('Результат подключения:', connected);

  // 2.2 Проверка состояния сервера
  console.log('\n📊 Проверка состояния сервера...');
  const status = await vpsManager.checkServerStatus();
  console.log('Состояние:', status);
  console.log(`CPU: ${status.cpu} | RAM: ${status.memory} | Disk: ${status.disk}`);

  // 2.3 Загрузка файла
  console.log('\n📁 Загрузка файла...');
  const uploaded = await vpsManager.uploadFile(
    '/var/www/myapp/config.json',
    '{"apiKey": "secret", "debug": false}'
  );
  console.log('Файл загружен:', uploaded);

  // 2.4 Перезагрузка сервера
  console.log('\n🔄 Запрос на перезагрузку сервера...');
  const restart = await vpsManager.restartServer();
  console.log('Статус перезагрузки:', restart);

  // 2.5 Отправка уведомления
  console.log('\n🔔 Отправка уведомлений...');
  vpsManager.sendNotification('Server is running smoothly', 'success');
  vpsManager.sendNotification('Unexpected behavior detected', 'warning');
}

// ============================================
// 3️⃣ SECURITY MONITOR BOT USAGE
// ============================================

async function example_securityMonitorBot() {
  console.log('\n✅ Пример 3: Использование Security Monitor Bot');

  const securityMonitor = new SecurityMonitorBot({
    token: 'YOUR_SECURITY_TOKEN',
    alertThreshold: 0.8
  });

  // 3.1 Мониторинг попыток вторжения
  console.log('\n🛡️ Мониторинг попыток вторжения...');
  const intrusions = await securityMonitor.monitorIntrusions();
  console.log('Результаты мониторинга:', intrusions);

  // 3.2 Логирование действий
  console.log('\n📝 Логирование действий пользователя...');
  const logged = await securityMonitor.logActivity(
    'file_access',
    'admin',
    '192.168.1.50'
  );
  console.log('Действие залогировано:', logged);

  // 3.3 Анализ угроз
  console.log('\n🔍 Анализ угроз...');
  const threats = await securityMonitor.analyzeThreats([
    { action: 'failed_login', timestamp: Date.now() },
    { action: 'failed_login', timestamp: Date.now() },
    { action: 'failed_login', timestamp: Date.now() }
  ]);
  console.log('Анализ угроз:', threats);

  // 3.4 Критическое оповещение
  console.log('\n⚠️ Отправка критического оповещения...');
  securityMonitor.alertOnIntrusion({
    type: 'brute_force_attack',
    attempts: 10,
    ip: '203.0.113.42',
    timestamp: new Date()
  });
}

// ============================================
// 4️⃣ FILE MANAGER BOT USAGE
// ============================================

async function example_fileManagerBot() {
  console.log('\n✅ Пример 4: Использование File Manager Bot');

  const fileManager = new FileManagerBot({
    token: 'YOUR_FILE_TOKEN',
    rootPath: '/home',
    maxFileSize: 500
  });

  // 4.1 Список файлов в папке
  console.log('\n📂 Получение списка файлов...');
  const fileList = await fileManager.listFiles('/var/www');
  console.log('Файлы в папке:', fileList);

  // 4.2 Создание резервной копии
  console.log('\n💾 Создание резервной копии...');
  const backup = await fileManager.createBackup();
  console.log('Резервная копия:', backup);

  // 4.3 Удаление файла
  console.log('\n🗑️ Удаление файла...');
  const deleted = await fileManager.deleteFile('/var/www/old_file.txt');
  console.log('Файл удалён:', deleted);

  // 4.4 Организация папки
  console.log('\n📊 Организация папки...');
  const organized = await fileManager.organizeFolder('/downloads');
  console.log('Результаты организации:', organized);
}

// ============================================
// 5️⃣ VPS SYSTEM INTEGRATION
// ============================================

async function example_vpsSystemIntegration() {
  console.log('\n✅ Пример 5: Интеграция VPS System');

  const vpsSystem = new VPSSystem({
    encryptionEnabled: true,
    monitoringInterval: 30000,
    vpsManagerToken: 'token_1',
    securityToken: 'token_2',
    fileManagerToken: 'token_3'
  });

  // 5.1 Выполнение команды на VPS Manager Bot (индекс 0)
  console.log('\n⚙️ Выполнение команды на VPS Manager Bot...');
  const statusResult = await vpsSystem.executeCommand(0, 'status');
  console.log('Результат команды status:', statusResult);

  // 5.2 Выполнение команды на Security Monitor Bot (индекс 1)
  console.log('\n⚙️ Выполнение команды на Security Monitor Bot...');
  const intrustionResult = await vpsSystem.executeCommand(
    1,
    'check-intrusions'
  );
  console.log('Результат команды check-intrusions:', intrustionResult);

  // 5.3 Выполнение команды на File Manager Bot (индекс 2)
  console.log('\n⚙️ Выполнение команды на File Manager Bot...');
  const listResult = await vpsSystem.executeCommand(2, 'list', {
    path: '/home'
  });
  console.log('Результат команды list:', listResult);

  // 5.4 Шифрование и расшифровка данных
  console.log('\n🔐 Шифрование и расшифровка данных...');
  const originalData = { token: 'secret123', key: 'value' };
  
  const encrypted = await vpsSystem.encryptData(originalData);
  console.log('Зашифрованные данные:', encrypted);

  const decrypted = await vpsSystem.decryptData(encrypted);
  console.log('Расшифрованные данные:', decrypted);
}

// ============================================
// 6️⃣ MONITORING AND ALERTS
// ============================================

async function example_monitoringAndAlerts() {
  console.log('\n✅ Пример 6: Мониторинг и уведомления');

  const vpsSystem = new VPSSystem({
    encryptionEnabled: true,
    monitoringInterval: 10000 // 10 секунд для примера
  });

  // 6.1 Запуск мониторинга (запускает фоновый процесс)
  console.log('\n📡 Запуск мониторинга системы...');
  console.log('💡 Мониторинг будет работать каждые 10 секунд');
  // vpsSystem.startMonitoring(); // Раскомментируйте для активного мониторинга

  // 6.2 Получение статуса системы
  const systemStatus = vpsSystem.getSystemStatus();
  console.log('\n📊 Статус системы:', systemStatus);
}

// ============================================
// 7️⃣ COMMAND LINE INTERFACE EXAMPLE
// ============================================

function example_cli() {
  console.log('\n✅ Пример 7: Интерфейс командной строки');
  console.log('\nДоступные команды:');
  console.log('  status              - Проверить состояние сервера');
  console.log('  upload <path>       - Загрузить файл');
  console.log('  restart             - Перезагрузить сервер');
  console.log('  list <path>         - Список файлов');
  console.log('  backup              - Создать резервную копию');
  console.log('  security            - Проверить безопасность');
  console.log('  help                - Справка');

  // Пример обработки команды
  function handleCommand(command, args) {
    const vpsSystem = new VPSSystem({
      encryptionEnabled: true
    });

    switch (command.toLowerCase()) {
      case 'status':
        console.log('\n📊 Выполнение: status');
        vpsSystem.executeCommand(0, 'status');
        break;

      case 'backup':
        console.log('\n💾 Выполнение: backup');
        vpsSystem.executeCommand(2, 'backup');
        break;

      case 'security':
        console.log('\n🛡️ Выполнение: security');
        vpsSystem.executeCommand(1, 'check-intrusions');
        break;

      default:
        console.log('❌ Команда не распознана');
    }
  }

  // Пример вызова
  handleCommand('status');
}

// ============================================
// 8️⃣ ERROR HANDLING EXAMPLE
// ============================================

async function example_errorHandling() {
  console.log('\n✅ Пример 8: Обработка ошибок');

  try {
    const vpsManager = new VPSManagerBot({
      token: '', // Неверный токен
      apiUrl: 'invalid_url'
    });

    const result = await vpsManager.connectToServer({
      ip: 'invalid_ip',
      port: 'invalid_port'
    });

    if (result.status === 'error') {
      console.log('❌ Ошибка при подключении:', result.message);
    }
  } catch (error) {
    console.error('💥 Критическая ошибка:', error.message);
  }
}

// ============================================
// 9️⃣ REAL-WORLD SCENARIO
// ============================================

async function example_realWorldScenario() {
  console.log('\n✅ Пример 9: Реальный сценарий использования');
  console.log('\nСценарий: Автоматизированный мониторинг и отклик на инциденты');

  const vpsSystem = new VPSSystem({
    encryptionEnabled: true,
    monitoringInterval: 60000 // 1 минута
  });

  // Симуляция реального сценария
  async function incidentResponse() {
    console.log('\n🔔 Обнаружен инцидент: высокое использование CPU');

    // 1. Проверить состояние
    const status = await vpsSystem.executeCommand(0, 'status');
    console.log('1️⃣  Проверили состояние:', status);

    // 2. Проверить безопасность
    const security = await vpsSystem.executeCommand(1, 'check-intrusions');
    console.log('2️⃣  Проверили безопасность:', security);

    // 3. Создать резервную копию
    const backup = await vpsSystem.executeCommand(2, 'backup');
    console.log('3️⃣  Создали резервную копию:', backup);

    // 4. Перезагрузить сервер
    const restart = await vpsSystem.executeCommand(0, 'restart');
    console.log('4️⃣  Перезагружаем сервер:', restart);
  }

  await incidentResponse();
}

// ============================================
// 🔟 RUN ALL EXAMPLES
// ============================================

async function runAllExamples() {
  try {
    // Раскомментируйте нужные примеры:
    
    // example_basicInit();
    // await example_vpsManagerBot();
    // await example_securityMonitorBot();
    // await example_fileManagerBot();
    // await example_vpsSystemIntegration();
    // await example_monitoringAndAlerts();
    // example_cli();
    // await example_errorHandling();
    // await example_realWorldScenario();

    console.log('\n' + '='.repeat(50));
    console.log('✅ Примеры подготовлены к использованию');
    console.log('='.repeat(50));

  } catch (error) {
    console.error('❌ Ошибка при выполнении примеров:', error);
  }
}

// Запуск примеров при загрузке файла
if (typeof document !== 'undefined') {
  document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 VPS System Examples готовы к использованию');
  });
}

// Export для использования в Node.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    example_basicInit,
    example_vpsManagerBot,
    example_securityMonitorBot,
    example_fileManagerBot,
    example_vpsSystemIntegration,
    example_monitoringAndAlerts,
    example_cli,
    example_errorHandling,
    example_realWorldScenario,
    runAllExamples
  };
}
