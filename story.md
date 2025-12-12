---
layout: default
title: Vibe-Coding with Gemini Ultra
permalink: /story/
---
<div style="max-width: 800px; margin: 0 auto; padding: 20px;">
  
  <!-- Header -->
  <div style="text-align: center; margin-bottom: 40px;">
    <h1 style="color: #ff79c6; font-size: 2.5em; margin-bottom: 10px;">The Daily Clamour & Fishwrap 1.1.0</h1>
    <h2 style="color: #bd93f9; font-size: 1.5em; font-weight: normal; margin-top: 0;">"Vibe-Coding" a News Engine with Gemini Ultra</h2>
    <div style="height: 4px; width: 60px; background-color: #50fa7b; margin: 20px auto; border-radius: 2px;"></div>
  </div>

  <div style="font-size: 1.1em; line-height: 1.8; color: #f8f8f2;">
    <p>I am thrilled to announce the release of <strong>Fishwrap 1.1.0</strong> and the launch of its flagship instance, <strong><a href="https://dailyclamour.com" style="color: #8be9fd;">The Daily Clamour</a></strong>.</p>

    <p>For my nerdy friends who care about the "how" as much as the "what," here is the real story.</p>

    <p>This entire stack—the Python ingestion engine, the "Glass-Box" auditing architecture, the HTML/CSS rendering pipelines, and the CI/CD scripts—was built entirely with <strong>Gemini Ultra</strong>.</p>

    <p style="font-size: 1.2em; font-weight: bold; color: #f1fa8c; text-align: center; margin: 30px 0;">I wrote almost zero code. Instead, I "vibe-coded" it.</p>

    <h3 style="color: #ff79c6; margin-top: 40px;">The "Team"</h3>
    <p>My role wasn't "Software Engineer" but <strong>Engineering Manager (EM)</strong> and <strong>Product Manager (PM)</strong>.</p>
    <p>I treated Gemini Ultra like a team of high-performing L5 engineers and designers. My "manual labor" wasn't typing syntax; it was rigorous personality management. I was the stickler EM refusing to merge PRs with ambiguous variable names, and the fanatical PM rejecting features because mobile padding was 2px off.</p>
    <p>When I needed to configure Cloudflare DNS or GitHub Pages, I didn't open a tutorial. I told the model: <em>"I need this live at this domain. Tell me exactly which buttons to click."</em> And it did.</p>

    <h3 style="color: #ff79c6; margin-top: 40px;">The "Impossible" Velocity</h3>
    <p>If I had to build this the "old way," I simply wouldn't have done it. In a professional setting, delivering this scope requires:</p>
    <ul style="list-style-type: disc; margin-left: 20px; color: #bd93f9;">
      <li><strong style="color: #f8f8f2;">1 L6 Product Manager</strong></li>
      <li><strong style="color: #f8f8f2;">1 Senior Designer</strong></li>
      <li><strong style="color: #f8f8f2;">2-3 L5 SDEs</strong></li>
    </ul>

    <div style="background-color: #44475a; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 5px solid #ff5555;">
      <p style="margin: 0;"><strong>Traditional Timeline:</strong> 4-6 months from brainstorming to v1.0.</p>
      <p style="margin: 10px 0 0 0;"><strong>Reality:</strong> I vibe-coded the entire thing in about <strong>50 hours</strong> over a few weeks.</p>
    </div>

    <h3 style="color: #ff79c6; margin-top: 40px;">The "Nerdy" Stuff (Fishwrap 1.1.0)</h3>
    <p>Fishwrap is a robust, concurrent content engine. Version 1.1.0 ("Speed & Stability") includes engineering wins that would usually take weeks of investigation, solved in hours:</p>
    
    <ol style="list-style-type: decimal; margin-left: 20px;">
      <li style="margin-bottom: 15px;"><strong>Concurrency Refactor:</strong> We hit an I/O wall with sequential fetching. I told Gemini to "make it fast but safe." It refactored <code>fetcher.py</code> and <code>enhancer.py</code> to use <code>ThreadPoolExecutor</code>, reducing I/O time from ~51s to ~7s (<strong style="color: #50fa7b;">7.5x speedup</strong>) in <em>one hour</em>.</li>
      <li style="margin-bottom: 15px;"><strong>Polite Scraping:</strong> We were accidentally DDoS-ing Reddit (HTTP 429). Gemini implemented a "Token Bucket" rate limiter in <code>utils.py</code> without me explaining the algorithm. We are now fast <em>and</em> polite.</li>
      <li style="margin-bottom: 15px;"><strong>Zombie Defense:</strong> Old articles were resurfacing. Gemini architected a "Memento" pattern: we decoupled database retention (48h) from publication (24h) and merged state updates, achieving a <strong style="color: #50fa7b;">100% cache hit rate</strong> on scraped metadata.</li>
    </ol>

    <h3 style="color: #ff79c6; margin-top: 40px;">The Conclusion</h3>
    <p>The meta-story is the future of software. I didn't need to know <em>how</em> to implement a Jaccard Index for deduplication; I just needed to know it was the <em>right tool</em> to ask for. I didn't need to memorize <code>tar</code> flags; I just needed to define safety constraints.</p>
    <p>This is what a 100x multiplier feels like.</p>

    <div style="text-align: center; margin-top: 50px; padding: 30px; border: 1px solid #6272a4; border-radius: 12px;">
      <h4 style="color: #8be9fd; margin-top: 0;">Explore the Ecosystem</h4>
      <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; margin-top: 20px;">
        <a href="https://dailyclamour.com" style="background-color: #ff79c6; color: #282a36; padding: 10px 20px; border-radius: 20px; text-decoration: none; font-weight: bold;">Live Product</a>
        <a href="https://fishwrap.org" style="background-color: #bd93f9; color: #282a36; padding: 10px 20px; border-radius: 20px; text-decoration: none; font-weight: bold;">The Engine</a>
        <a href="https://github.com/maxspevack/fishwrap" style="background-color: #50fa7b; color: #282a36; padding: 10px 20px; border-radius: 20px; text-decoration: none; font-weight: bold;">The Code</a>
      </div>
    </div>
    
    <div style="text-align: center; margin-top: 40px;">
      <a href="/" style="color: #f8f8f2; text-decoration: none; border-bottom: 1px dotted #f8f8f2;">← Back to Max Spevack</a>
    </div>

  </div>
</div>
