/* ============================================
   Particle Background System
   ============================================ */
(function() {
  const canvas = document.getElementById('particle-canvas');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  let particles = [];
  let animationId = null;
  let isActive = true;
  
  const COLORS = [
    'rgba(147, 51, 234, 0.5)',
    'rgba(168, 85, 247, 0.4)',
    'rgba(192, 132, 252, 0.3)',
    'rgba(216, 180, 254, 0.2)',
  ];
  
  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  
  class Particle {
    constructor() {
      this.reset();
    }
    
    reset() {
      this.x = Math.random() * canvas.width;
      this.y = Math.random() * canvas.height;
      this.size = Math.random() * 2 + 0.5;
      this.speedX = (Math.random() - 0.5) * 0.5;
      this.speedY = (Math.random() - 0.5) * 0.5;
      this.color = COLORS[Math.floor(Math.random() * COLORS.length)];
      this.opacity = Math.random() * 0.5 + 0.2;
      this.life = 0;
      this.maxLife = Math.random() * 300 + 200;
    }
    
    update() {
      this.x += this.speedX;
      this.y += this.speedY;
      this.life++;
      
      if (this.life > this.maxLife || 
          this.x < 0 || this.x > canvas.width || 
          this.y < 0 || this.y > canvas.height) {
        this.reset();
      }
    }
    
    draw() {
      const fade = 1 - Math.abs(this.life / this.maxLife - 0.5) * 2;
      ctx.globalAlpha = this.opacity * fade;
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fillStyle = this.color;
      ctx.fill();
      ctx.globalAlpha = 1;
    }
  }
  
  function init() {
    resize();
    const count = Math.min(80, Math.floor((canvas.width * canvas.height) / 15000));
    particles = [];
    for (let i = 0; i < count; i++) {
      particles.push(new Particle());
    }
  }
  
  function drawLines() {
    const maxDistance = 120;
    const maxConnections = 3;
    
    for (let i = 0; i < particles.length; i++) {
      let connections = 0;
      for (let j = i + 1; j < particles.length; j++) {
        if (connections >= maxConnections) break;
        
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < maxDistance) {
          const opacity = (1 - distance / maxDistance) * 0.15;
          ctx.globalAlpha = opacity;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = 'rgba(168, 85, 247, 0.5)';
          ctx.lineWidth = 0.5;
          ctx.stroke();
          ctx.globalAlpha = 1;
          connections++;
        }
      }
    }
  }
  
  function animate() {
    if (!isActive) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    for (const p of particles) {
      p.update();
      p.draw();
    }
    drawLines();
    
    animationId = requestAnimationFrame(animate);
  }
  
  // Visibility check
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      isActive = false;
      if (animationId) cancelAnimationFrame(animationId);
    } else {
      isActive = true;
      animate();
    }
  });
  
  window.addEventListener('resize', () => {
    resize();
    init();
  });
  
  init();
  animate();
})();
