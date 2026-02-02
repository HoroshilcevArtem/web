// Main VPS System Orchestrator
class VPSSystem {
  constructor(config = {}) {
    this.isInitialized = false;
    this.bots = [];
    this.config = {
      encryptionEnabled: true,
      monitoringInterval: 30000, // 30 seconds
      notificationChannelId: config.notificationChannelId || '',
      ...config
    };
    this.initializeBots();
  }

  initializeBots() {
    console.log('🤖 Инициализация системы ботов...');
    
    // Создание экземпляров ботов
    const vpsManager = new VPSManagerBot({
      token: this.config.vpsManagerToken,
      apiUrl: this.config.apiUrl
    });

    const securityMonitor = new SecurityMonitorBot({
      token: this.config.securityToken,
      alertThreshold: this.config.alertThreshold
    });

    const fileManager = new FileManagerBot({
      token: this.config.fileManagerToken,
      rootPath: this.config.rootPath
    });

    this.bots = [vpsManager, securityMonitor, fileManager];
    this.isInitialized = true;
    console.log('✅ Система ботов инициализирована');
  }

  async startMonitoring() {
    if (!this.isInitialized) {
      console.error('❌ Система не инициализирована');
      return;
    }

    console.log('📡 Запуск мониторинга...');
    
    const monitoringLoop = async () => {
      try {
        const vpsManager = this.bots[0];
        const securityMonitor = this.bots[1];

        // Проверка состояния сервера
        const status = await vpsManager.checkServerStatus();
        console.log('📊 Состояние сервера:', status);

        // Проверка безопасности
        const threats = await securityMonitor.monitorIntrusions();
        
        if (threats.failedAttempts > 5) {
          securityMonitor.alertOnIntrusion({
            type: 'multiple_failed_logins',
            attempts: threats.failedAttempts
          });
        }

        // Отправка уведомлений
        if (status.status === 'offline') {
          vpsManager.sendNotification(
            '🚨 Сервер отключился! Требуется немедленное внимание.',
            'critical'
          );
        }

      } catch (error) {
        console.error('Ошибка мониторинга:', error);
      }
    };

    // Запуск периодического мониторинга
    setInterval(monitoringLoop, this.config.monitoringInterval);
    
    // Первая проверка сразу
    await monitoringLoop();
  }

  async encryptData(data) {
    if (!this.config.encryptionEnabled) {
      return data;
    }

    // Симуляция шифрования (в реальной системе используется крипто-библиотека)
    console.log('🔐 Шифрование данных...');
    return {
      encrypted: true,
      data: btoa(JSON.stringify(data)), // Base64 для демонстрации
      timestamp: new Date().toISOString()
    };
  }

  async decryptData(encryptedData) {
    if (!this.config.encryptionEnabled) {
      return encryptedData;
    }

    try {
      console.log('🔓 Расшифровка данных...');
      return JSON.parse(atob(encryptedData.data));
    } catch (error) {
      console.error('Ошибка расшифровки:', error);
      return null;
    }
  }

  async executeCommand(botIndex, command, params) {
    if (botIndex < 0 || botIndex >= this.bots.length) {
      console.error('❌ Неверный индекс бота');
      return;
    }

    const bot = this.bots[botIndex];
    console.log(`⚡ Выполнение команды: ${command} на боте ${bot.name}`);

    try {
      let result;

      if (bot instanceof VPSManagerBot) {
        if (command === 'status') {
          result = await bot.checkServerStatus();
        } else if (command === 'restart') {
          result = await bot.restartServer();
        } else if (command === 'upload') {
          result = await bot.uploadFile(params.path, params.data);
        }
      } else if (bot instanceof SecurityMonitorBot) {
        if (command === 'check-intrusions') {
          result = await bot.monitorIntrusions();
        } else if (command === 'analyze') {
          result = await bot.analyzeThreats(params.log);
        }
      } else if (bot instanceof FileManagerBot) {
        if (command === 'list') {
          result = await bot.listFiles(params.path);
        } else if (command === 'backup') {
          result = await bot.createBackup();
        } else if (command === 'delete') {
          result = await bot.deleteFile(params.path);
        }
      }

      // Шифрование результата перед отправкой
      if (this.config.encryptionEnabled) {
        result = await this.encryptData(result);
      }

      return result;

    } catch (error) {
      console.error('Ошибка выполнения команды:', error);
      return { status: 'error', message: error.message };
    }
  }

  getSystemStatus() {
    return {
      isInitialized: this.isInitialized,
      botsCount: this.bots.length,
      bots: this.bots.map(bot => bot.name),
      encryption: this.config.encryptionEnabled ? '🔐 Включено' : '⚠️ Отключено',
      timestamp: new Date().toISOString()
    };
  }

  printSystemInfo() {
    const status = this.getSystemStatus();
    console.log('═══════════════════════════════════════════');
    console.log('📊 VPS SYSTEM STATUS');
    console.log('═══════════════════════════════════════════');
    console.log(`Инициализирована: ${status.isInitialized ? '✅ Да' : '❌ Нет'}`);
    console.log(`Ботов активно: ${status.botsCount}`);
    console.log(`Шифрование: ${status.encryption}`);
    console.log('───────────────────────────────────────────');
    console.log('Активные боты:');
    status.bots.forEach((bot, i) => console.log(`  ${i + 1}. ${bot}`));
    console.log('═══════════════════════════════════════════');
  }
}

// Export для использования
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { VPSSystem };
}
