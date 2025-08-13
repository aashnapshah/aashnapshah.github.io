---
permalink: /gallery/
title: "Gallery"
author_profile: true
---


<div class="gallery-grid">
  <div class="gallery-item large">
    <img src="/images/photo1.jpg" alt="Research Screenshot 1" loading="lazy">
  </div>
  
  <div class="gallery-item medium">
    <img src="/images/photo2.png" alt="Research Screenshot 2" loading="lazy">
  </div>
  
  <div class="gallery-item wide">
    <img src="/images/photo3.png" alt="Research Screenshot 3" loading="lazy">
  </div>
  
  <div class="gallery-item large">
    <img src="/images/photo4.png" alt="Research Screenshot 4" loading="lazy">
  </div>
  
  <div class="gallery-item medium">
    <img src="/images/photo5.png" alt="Research Screenshot 5" loading="lazy">
  </div>
  
  <div class="gallery-item wide">
    <img src="/images/photo6.png" alt="Research Screenshot 6" loading="lazy">
  </div>
  
  <div class="gallery-item large">
    <img src="/images/photo7.png" alt="Research Screenshot 7" loading="lazy">
  </div>
  
  <div class="gallery-item medium">
    <img src="/images/photo8.png" alt="Personal Photo" loading="lazy">
  </div>
  
  <div class="gallery-item wide">
    <img src="/images/photo9.png" alt="Research Screenshot 9" loading="lazy">
  </div>
  
  <div class="gallery-item large">
    <img src="/images/photo10.png" alt="Research Screenshot 10" loading="lazy">
  </div>
  
  <div class="gallery-item medium">
    <img src="/images/photo11.png" alt="Research Screenshot 11" loading="lazy">
  </div>
</div>

---

## Gallery Styling

<style>
.gallery-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  grid-auto-rows: 200px;
  gap: 15px;
  margin: 2em 0;
  grid-auto-flow: dense;
}

.gallery-item {
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  border-radius: 8px;
  background: #f8f9fa;
}

.gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.3s ease;
}

.gallery-item:hover img {
  transform: scale(1.05);
}

/* Size variations for fun, random layout */
.gallery-item.small {
  grid-column: span 1;
  grid-row: span 1;
}

.gallery-item.medium {
  grid-column: span 2;
  grid-row: span 2;
}

.gallery-item.large {
  grid-column: span 2;
  grid-row: span 3;
}

.gallery-item.wide {
  grid-column: span 2;
  grid-row: span 1;
}

/* Responsive adjustments */
@media (max-width: 1400px) {
  .gallery-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 1200px) {
  .gallery-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .gallery-grid {
    grid-template-columns: repeat(2, 1fr);
    grid-auto-rows: 150px;
    gap: 10px;
  }
  
  .gallery-item.large {
    grid-column: span 1;
    grid-row: span 2;
  }
  
  .gallery-item.large {
    grid-column: span 2;
    grid-row: span 1;
  }
}

@media (max-width: 480px) {
  .gallery-grid {
    grid-template-columns: 1fr;
    grid-auto-rows: 200px;
  }
  
  .gallery-item.medium,
  .gallery-item.large,
  .gallery-item.wide {
    grid-column: span 1;
    grid-row: span 1;
  }
}
</style>

---

---

[← Back to About](/)
