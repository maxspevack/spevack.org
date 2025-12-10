---
layout: default
title: Max Spevack
---
<!-- Favicons -->
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="shortcut icon" href="/favicon.ico">

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">

<style>
  .profile-container {
    text-align: center;
    margin-top: 50px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  }
  .profile-photo {
    width: 180px;
    height: 180px;
    border-radius: 50%;
    object-fit: cover;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    margin-bottom: 20px;
  }
  .name {
    font-size: 2.5em;
    font-weight: 700;
    margin-bottom: 5px;
    color: #333;
  }
  .subtitle {
    font-size: 1.2em;
    color: #666;
    margin-bottom: 30px;
  }
  .icon-row {
    display: flex;
    justify-content: center;
    gap: 30px;
    font-size: 2em;
  }
  .icon-link {
    color: #555;
    transition: color 0.2s, transform 0.2s;
  }
  .icon-link:hover {
    color: #000;
    transform: translateY(-3px);
  }
  /* Specific brand colors on hover */
  .icon-link.linkedin:hover { color: #0077b5; }
  .icon-link.email:hover { color: #ea4335; }
  .icon-link.resume:hover { color: #2ecc71; }
</style>

<div class="profile-container">
  <img src="max.jpg" alt="Max Spevack" class="profile-photo">
  
  <div class="name">Max Spevack</div>
  
  <div class="icon-row">
    <!-- LinkedIn -->
    <a href="https://www.linkedin.com/in/maxspevack/" class="icon-link linkedin" title="LinkedIn" target="_blank">
      <i class="fab fa-linkedin"></i>
    </a>
    
    <!-- Email -->
    <a href="mailto:max.spevack@gmail.com" class="icon-link email" title="Email">
      <i class="fas fa-envelope"></i>
    </a>

    <!-- Resume -->
    <a href="resume.md" class="icon-link resume" title="Resume">
      <i class="fas fa-file-alt"></i>
    </a>
  </div>
</div>