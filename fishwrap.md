---
layout: default
title: Vibe-Coding with Gemini Ultra
permalink: /fishwrap/
---
<div class="story-container">
  
  <!-- Header -->
  <div style="text-align: center; margin-bottom: 40px;">
    <h1>The Daily Clamour & Fishwrap 1.1.0</h1>
    <div class="story-meta">December 12, 2025 • By Max Spevack</div>
    <h2 style="border: none; font-size: 1.6em; margin-top: 10px;">"Vibe-Coding" a News Engine with Gemini Ultra</h2>
  </div>

  <p>I am thrilled to announce the release of <strong>Fishwrap 1.1.0</strong> and the launch of its flagship instance, <strong><a href="https://dailyclamour.com">The Daily Clamour</a></strong>.</p>

  <p>For my nerdy friends who care about the "how" as much as the "what," here is the real story.</p>

  <p>This entire stack—the Python ingestion engine, the "Glass-Box" auditing architecture, the HTML/CSS rendering pipelines, and the CI/CD scripts—was built entirely with <strong>Gemini Ultra</strong>.</p>

  <blockquote>I wrote almost zero code. Instead, I "vibe-coded" it.</blockquote>

  <h3>The "Team"</h3>
  <p>My role wasn't "Software Engineer" but <strong>Engineering Manager (EM)</strong> and <strong>Product Manager (PM)</strong>.</p>
  <p>I treated Gemini Ultra like a team of high-performing L5 engineers and designers. My "manual labor" wasn't typing syntax; it was rigorous personality management. I was the stickler EM refusing to merge PRs with ambiguous variable names, and the fanatical PM rejecting features because mobile padding was 2px off.</p>
  <p>When I needed to configure Cloudflare DNS or GitHub Pages, I didn't open a tutorial. I told the model: <em>"I need this live at this domain. Tell me exactly which buttons to click."</em> And it did.</p>

  <h3>The "Impossible" Velocity</h3>
  <p>If I had to build this the "old way," I simply wouldn't have done it. In a professional setting, delivering this scope requires:</p>
  <ul>
    <li><strong>1 L6 Product Manager</strong></li>
    <li><strong>1 Senior Designer</strong></li>
    <li><strong>2-3 L5 SDEs</strong></li>
  </ul>

  <div style="background-color: rgba(0,0,0,0.05); padding: 20px; border-left: 4px solid var(--accent-red); margin: 20px 0;">
    <p style="margin: 0; font-family: var(--font-mono);"><strong>Traditional Timeline:</strong> 4-6 months from brainstorming to v1.0.</p>
    <p style="margin: 10px 0 0 0; font-family: var(--font-mono);"><strong>Reality:</strong> I vibe-coded the entire thing in about <strong>50 hours</strong> over a few weeks.</p>
  </div>

  <h3>The "Nerdy" Stuff (Fishwrap 1.1.0)</h3>
  <p>Fishwrap is a robust, concurrent content engine. Version 1.1.0 ("Speed & Stability") includes engineering wins that would usually take weeks of investigation, solved in hours:</p>
  
  <ol>
    <li><strong>Concurrency Refactor:</strong> We hit an I/O wall with sequential fetching. I told Gemini to "make it fast but safe." It refactored <code>fetcher.py</code> and <code>enhancer.py</code> to use <code>ThreadPoolExecutor</code>, reducing I/O time from ~51s to ~7s (<strong>7.5x speedup</strong>) in <em>one hour</em>.</li>
    <li><strong>Polite Scraping:</strong> We were accidentally DDoS-ing Reddit (HTTP 429). Gemini implemented a "Token Bucket" rate limiter in <code>utils.py</code> without me explaining the algorithm. We are now fast <em>and</em> polite.</li>
    <li><strong>Zombie Defense:</strong> Old articles were resurfacing. Gemini architected a "Memento" pattern: we decoupled database retention (48h) from publication (24h) and merged state updates, achieving a <strong>100% cache hit rate</strong> on scraped metadata.</li>
  </ol>

  <h3>The Conclusion</h3>
  <p>The meta-story is the future of software. I didn't need to know <em>how</em> to implement a Jaccard Index for deduplication; I just needed to know it was the <em>right tool</em> to ask for. I didn't need to memorize <code>tar</code> flags; I just needed to define safety constraints.</p>
  <p>This is what a 100x multiplier feels like.</p>

  <div style="text-align: center; margin-top: 50px; padding-top: 30px; border-top: 3px double var(--border-color);">
    <h4 style="margin-top: 0; margin-bottom: 20px;">Explore the Ecosystem</h4>
    <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 15px;">
      <a href="https://dailyclamour.com" class="clamour-btn" style="font-size: 0.9em;">Live Product</a>
      <a href="https://fishwrap.org" class="clamour-btn" style="font-size: 0.9em; background-color: var(--bg-color); color: var(--text-color); border: 1px solid var(--text-color);">The Engine</a>
      <a href="https://github.com/maxspevack/fishwrap" class="clamour-btn" style="font-size: 0.9em; background-color: var(--bg-color); color: var(--text-color); border: 1px solid var(--text-color);">The Code</a>
    </div>
  </div>
  
  <div style="text-align: center; margin-top: 40px;">
    <a href="/" style="font-family: var(--font-mono); font-size: 0.9em;">&larr; Back to Max Spevack</a>
  </div>

  <div class="footer-note">
    <p>
      <i class="fas fa-newspaper"></i> &nbsp;This website (spevack.org) was also re-implemented as a <em>soupçon</em> by the same AI team.
    </p>
  </div>

</div>
