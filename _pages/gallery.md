---
layout: single
permalink: /gallery/
title: "Gallery"
author_profile: false
---

<div class="gallery-grid">
  <div class="gallery-item large">
    <img src="/images/photo17.png" alt="Photo 17" loading="lazy">
  </div>
  
  <div class="gallery-item medium">
    <img src="/images/photo3.png" alt="Photo 3" loading="lazy">
  </div>
  
  <div class="gallery-item large">
    <img src="/images/photo8.png" alt="Photo 8" loading="lazy">
  </div>
  
  <div class="gallery-item medium">
    <img src="/images/photo12.png" alt="Photo 12" loading="lazy">
  </div>
  
  <div class="gallery-item large">
    <img src="/images/photo1.jpg" alt="Photo 1" loading="lazy">
  </div>
  
  <div class="gallery-item large">
    <img src="/images/photo15.png" alt="Photo 15" loading="lazy">
  </div>
  
  <div class="gallery-item medium">
    <img src="/images/photo6.png" alt="Photo 6" loading="lazy">
  </div>
  
  <div class="gallery-item large">
    <img src="/images/photo19.png" alt="Photo 19" loading="lazy">
  </div>
  
  <div class="gallery-item medium">
    <img src="/images/photo4.png" alt="Photo 4" loading="lazy">
  </div>
  
  <div class="gallery-item large">
    <img src="/images/photo10.png" alt="Photo 10" loading="lazy">
  </div>
  
  <div class="gallery-item medium">
    <img src="/images/photo20.png" alt="Photo 20" loading="lazy">
  </div>
  
  <div class="gallery-item medium">
    <img src="/images/photo7.png" alt="Photo 7" loading="lazy">
  </div>
  
  <div class="gallery-item large">
    <img src="/images/photo2.png" alt="Photo 2" loading="lazy">
  </div>
  
  <div class="gallery-item large">
    <img src="/images/photo13.png" alt="Photo 13" loading="lazy">
  </div>
  
  <div class="gallery-item medium">
    <img src="/images/photo9.png" alt="Photo 9" loading="lazy">
  </div>
  
  <div class="gallery-item large">
    <img src="/images/photo16.png" alt="Photo 16" loading="lazy">
  </div>
  
  <div class="gallery-item large">
    <img src="/images/photo5.png" alt="Photo 5" loading="lazy">
  </div>
  
  <div class="gallery-item medium">
    <img src="/images/photo11.png" alt="Photo 11" loading="lazy">
  </div>
  
  <div class="gallery-item wide">
    <img src="/images/photo14.png" alt="Photo 14" loading="lazy">
  </div>
  
  <div class="gallery-item large">
    <img src="/images/photo18.png" alt="Photo 18" loading="lazy">
  </div>
</div>

---

<style>
/* Override page width constraints for gallery */
.page__content {
  max-width: none !important;
  width: 100% !important;
  padding: 0 !important;
  margin-left: 0 !important;
}

.page__inner-wrap {
  max-width: none !important;
  width: 100% !important;
  margin-left: 0 !important;
  padding-left: 0 !important;
}

#main {
  max-width: none !important;
  width: 100% !important;
  margin-left: 0 !important;
  padding-left: 0 !important;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: 200px;
  gap: 8px;
  margin: 1em 0;
  grid-auto-flow: dense;
  max-width: 100%;
  width: 100%;
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

/* Rotate photo 20 to correct orientation */
.gallery-item:nth-child(13) img {
  transform: rotate(90deg);
}

.gallery-item:nth-child(13):hover img {
  transform: rotate(90deg) scale(1.05);
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
@media (max-width: 1600px) {
  .gallery-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 6px;
  }
}

@media (max-width: 1400px) {
  .gallery-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 6px;
  }
}

@media (max-width: 1200px) {
  .gallery-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 6px;
  }
}

@media (max-width: 768px) {
  .gallery-grid {
    grid-template-columns: repeat(2, 1fr);
    grid-auto-rows: 150px;
    gap: 6px;
  }
  
  .gallery-item.large {
    grid-column: span 1;
    grid-row: span 2;
  }
  
  .gallery-item.wide {
    grid-column: span 2;
    grid-row: span 1;
  }
}

@media (max-width: 480px) {
  .gallery-grid {
    grid-template-columns: 1fr;
    grid-auto-rows: 200px;
    gap: 6px;
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

[← Back to About](/)
