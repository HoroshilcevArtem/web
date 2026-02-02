// Service Pages Animations
document.addEventListener('DOMContentLoaded', function() {
  console.log('🚀 Service Page loaded');
  initializeAnimations();
  setupInteractions();
});

function initializeAnimations() {
  // Animate text appearance with staggered effect
  const textElements = document.querySelectorAll('.service-hero-text h1, .service-hero-text p');
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

  document.querySelectorAll('.feature-card, .benefit-item, .guarantee-item').forEach(card => {
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

  // Benefit items hover effect
  const benefitItems = document.querySelectorAll('.benefit-item');
  benefitItems.forEach(item => {
    item.addEventListener('mouseenter', function() {
      this.style.transform = 'translateX(5px)';
    });
    item.addEventListener('mouseleave', function() {
      this.style.transform = 'translateX(0)';
    });
  });

  // Guarantee items animation
  const guaranteeItems = document.querySelectorAll('.guarantee-item');
  guaranteeItems.forEach((item) => {
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
