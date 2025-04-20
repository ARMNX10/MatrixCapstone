// Matrix digital rain effect
const matrixRain = () => {
  // Get the canvas element
  const canvas = document.getElementById('matrixCanvas');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  
  // Make canvas full screen
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  
  // Characters to display
  const chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';
  const charArray = chars.split('');
  
  // Font size
  const fontSize = 14;
  const columns = canvas.width / fontSize;
  
  // Array to track the y position of each column
  const drops = [];
  
  // Initialize drops array
  for (let i = 0; i < columns; i++) {
    drops[i] = 1;
  }
  
  // Draw the matrix rain
  const draw = () => {
    // Set a semi-transparent black background
    ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Set the text color and font
    ctx.fillStyle = '#0F0';
    ctx.font = fontSize + 'px monospace';
    
    // Draw each character
    for (let i = 0; i < drops.length; i++) {
      // Get a random character
      const text = charArray[Math.floor(Math.random() * charArray.length)];
      
      // Draw the character
      ctx.fillText(text, i * fontSize, drops[i] * fontSize);
      
      // Move the drop down
      if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
        drops[i] = 0;
      }
      
      drops[i]++;
    }
  };
  
  // Run the animation
  setInterval(draw, 33);
};

// Initialize the matrix rain effect when the page loads
window.addEventListener('DOMContentLoaded', () => {
  // Create the canvas element
  const canvas = document.createElement('canvas');
  canvas.id = 'matrixCanvas';
  canvas.style.position = 'fixed';
  canvas.style.top = '0';
  canvas.style.left = '0';
  canvas.style.width = '100%';
  canvas.style.height = '100%';
  canvas.style.zIndex = '-1';
  canvas.style.pointerEvents = 'none';
  
  // Add the canvas to the page
  document.body.appendChild(canvas);
  
  // Start the matrix rain
  matrixRain();
});
