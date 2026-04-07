---
layout: single
permalink: /gallery/
title: ""
author_profile: false
---

<div class="gallery-mosaic">

  <div class="gm-item gm-landscape">
    <img src="/images/photo11.png" alt="Precision Medicine 2024 panel" loading="lazy">
    <div class="gm-caption">Precision Medicine 2024 -- Education in the AI Era</div>
  </div>

  <div class="gm-item gm-portrait">
    <img src="/images/photo2.png" alt="Poster presentation on VLMs" loading="lazy">
    <div class="gm-caption">Presenting VLM work at a poster session</div>
  </div>

  <div class="gm-item gm-portrait">
    <img src="/images/photo9.png" alt="Poster on reducing racial bias in PFTs" loading="lazy">
    <div class="gm-caption">Poster: Reducing racial bias in PFTs via ML</div>
  </div>

  <div class="gm-item gm-portrait">
    <img src="/images/photo8.png" alt="Certificate with advisor" loading="lazy">
    <div class="gm-caption">Award day with my advisor</div>
  </div>

  <div class="gm-item gm-wide">
    <img src="/images/photo12.png" alt="DBMI cohort photo" loading="lazy">
    <div class="gm-caption">DBMI cohort</div>
  </div>

  <div class="gm-item gm-landscape">
    <img src="/images/photo3.png" alt="Lab life with the pup" loading="lazy">
    <div class="gm-caption">Lab life (+ lab dog)</div>
  </div>

  <div class="gm-item gm-portrait">
    <img src="/images/photo10.png" alt="Lab dog in lecture hall" loading="lazy">
    <div class="gm-caption">Our unofficial lab mascot in lecture</div>
  </div>

  <div class="gm-item gm-landscape">
    <img src="/images/photo13.png" alt="Lab selfie with friends and dog" loading="lazy">
    <div class="gm-caption">Lab crew</div>
  </div>

  <div class="gm-item gm-landscape">
    <img src="/images/photo7.png" alt="Lab lunch outing" loading="lazy">
    <div class="gm-caption">Lab lunch</div>
  </div>

  <div class="gm-item gm-landscape">
    <img src="/images/photo6.png" alt="Bowling with the cohort" loading="lazy">
    <div class="gm-caption">Bowling night with the cohort</div>
  </div>

  <div class="gm-item gm-landscape">
    <img src="/images/photo19.png" alt="SSQB group meeting" loading="lazy">
    <div class="gm-caption">SSQB group</div>
  </div>

  <div class="gm-item gm-landscape">
    <img src="/images/photo4.png" alt="Dinner with friends" loading="lazy">
    <div class="gm-caption">Dinner with the crew</div>
  </div>

  <div class="gm-item gm-landscape">
    <img src="/images/photo5.png" alt="Group selfie at Harvard" loading="lazy">
    <div class="gm-caption">Harvard crew out and about</div>
  </div>

  <div class="gm-item gm-landscape">
    <img src="/images/photo17.png" alt="Group selfie outdoors" loading="lazy">
    <div class="gm-caption">Cohort outing</div>
  </div>

  <div class="gm-item gm-portrait">
    <img src="/images/photo1.jpg" alt="Group photo on lifeguard chair" loading="lazy">
    <div class="gm-caption">Retreat vibes</div>
  </div>

  <div class="gm-item gm-landscape">
    <img src="/images/photo18.png" alt="Dinner at retreat" loading="lazy">
    <div class="gm-caption">Retreat dinner</div>
  </div>

  <div class="gm-item gm-portrait">
    <img src="/images/photo16.png" alt="SSQB matching sweatshirts" loading="lazy">
    <div class="gm-caption">SSQB crew</div>
  </div>

  <div class="gm-item gm-landscape">
    <img src="/images/photo15.png" alt="NYC selfie" loading="lazy">
    <div class="gm-caption">NYC</div>
  </div>

  <div class="gm-item gm-portrait">
    <img src="/images/photo20.png" alt="Aquarium with friends" loading="lazy">
    <div class="gm-caption">Aquarium day</div>
  </div>

  <div class="gm-item gm-landscape">
    <img src="/images/photo14.png" alt="FaceTime selfie with friends" loading="lazy">
    <div class="gm-caption">Near and far</div>
  </div>

</div>

<style>
/* Override page width constraints for gallery */
.page__content {
  max-width: none !important;
  width: 100% !important;
  padding: 0 3em !important;
  margin-left: 6em !important;
}

.page__inner-wrap,
#main,
.page,
article {
  max-width: none !important;
  width: 100% !important;
  margin-left: 0 !important;
  padding-left: 0 !important;
}

/* --- Mosaic Gallery --- */
.gallery-mosaic {
  columns: 3;
  column-gap: 10px;
  margin: 1em 0;
}

.gm-item {
  break-inside: avoid;
  margin-bottom: 10px;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
  background: #f4f4f4;
}

.gm-item img {
  width: 100%;
  height: auto;
  display: block;
  transition: transform 0.4s ease;
}

.gm-item:hover img {
  transform: scale(1.03);
}

.gm-caption {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 2em 0.8em 0.6em;
  background: linear-gradient(transparent, rgba(0,0,0,0.5));
  color: white;
  font-size: 0.78em;
  font-weight: 500;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.gm-item:hover .gm-caption {
  opacity: 1;
}

/* Responsive */
@media (max-width: 1100px) {
  .gallery-mosaic {
    columns: 2;
  }
}

@media (max-width: 600px) {
  .gallery-mosaic {
    columns: 1;
  }
  .page__content {
    padding: 0 1em !important;
    margin-left: 0 !important;
  }
}
</style>
