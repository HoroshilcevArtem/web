// VPS Page Animations and Interactions
document.addEventListener('DOMContentLoaded', function() {
  console.log('🚀 VPS Page loaded');
  initializeAnimations();
  setupInteractions();
});

function initializeAnimations() {
  // Animate text appearance with staggered effect
  const textElements = document.querySelectorAll('.vps-hero-text h1, .vps-hero-text p');
  textElements.forEach((el, index) => {
    el.style.animation = `slide-in-left 0.8s ease ${0.2 + index * 0.2}s backwards`;
  });

  // Animate feature cards on scroll
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.animation = `slide-in-up 0.6s ease forwards`;
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  document.querySelectorAll('.feature-card, .bot-card, .guarantee-item').forEach(card => {
    observer.observe(card);
  });
}

function setupInteractions() {
  // Feature cards hover effect
  const featureCards = document.querySelectorAll('.feature-card');
  featureCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-10px)';
    });
    card.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0)';
    });
  });

  // Guarantee items animation
  const guaranteeItems = document.querySelectorAll('.guarantee-item');
  guaranteeItems.forEach((item, index) => {
    item.addEventListener('mouseenter', function() {
      this.style.transform = 'scale(1.05)';
    });
    item.addEventListener('mouseleave', function() {
      this.style.transform = 'scale(1)';
    });
  });

  // Smooth scroll
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
}

// Инициализация VPS System при загрузке страницы
function initializeVPSSystem() {
  console.log('🔧 Инициализация VPS System...');
  
  const vpsSystem = new VPSSystem({
    encryptionEnabled: true,
    monitoringInterval: 30000,
    vpsManagerToken: 'YOUR_TOKEN_HERE',
    securityToken: 'YOUR_TOKEN_HERE',
    fileManagerToken: 'YOUR_TOKEN_HERE',
    apiUrl: 'https://api.example.com'
  });

  vpsSystem.printSystemInfo();
  // Раскомментируйте для активного мониторинга:
  // vpsSystem.startMonitoring();

  return vpsSystem;
}

// Запуск системы при загрузке
let globalVPSSystem;
window.addEventListener('load', () => {
  globalVPSSystem = initializeVPSSystem();
});
