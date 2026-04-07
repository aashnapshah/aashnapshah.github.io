---
permalink: /
layout: portfolio
title: "Aashna Shah"
author_profile: false
redirect_from:
  - /about/
  - /about.html
---

<!-- ==================== HERO ==================== -->
<section class="pf-hero" id="top">
  <div class="pf-hero-content">
    <div class="pf-hero-text">
      <div class="pf-hero-hello">Hi, I'm</div>
      <h1 class="pf-hero-name">Aashna Shah</h1>
      <p class="pf-hero-tagline">I build <span class="pf-accent">machine learning</span> systems that rethink how medicine defines <span class="pf-accent">"normal"</span></p>
      <p class="pf-hero-sub">PhD Candidate at Harvard Medical School. I train transformers on billions of clinical measurements, build frameworks that replace race with biology in clinical equations, and evaluate foundation models for fairness in medical imaging.</p>
      <p class="pf-hero-seeking">Graduating 2026 -- seeking research scientist and ML engineering roles in healthcare AI.</p>
      <div class="pf-hero-links">
        <a href="mailto:aashnashah@g.harvard.edu" class="pf-btn"><i class="fas fa-envelope"></i> Email</a>
        <a href="https://github.com/aashnapshah" class="pf-btn pf-btn-outline"><i class="fab fa-github"></i> GitHub</a>
        <a href="https://linkedin.com/in/aashna-p-shah" class="pf-btn pf-btn-outline"><i class="fab fa-linkedin"></i> LinkedIn</a>
        <a href="https://scholar.google.com/citations?hl=en&user=7RmZd8QAAAAJ" class="pf-btn pf-btn-outline"><i class="fas fa-graduation-cap"></i> Scholar</a>
        <a href="/CV.pdf" class="pf-btn pf-btn-outline"><i class="fas fa-file-pdf"></i> CV</a>
      </div>
    </div>
    <div class="pf-hero-photo">
      <img src="/images/profile_compressed.png" alt="Aashna Shah">
    </div>
  </div>
</section>

<!-- ==================== ABOUT ==================== -->
<section class="pf-section" id="about">
  <div class="pf-container">
    <h2 class="pf-section-title">About</h2>

    <!-- Education: prominent, first thing -->
    <div class="pf-edu-row">
      <div class="pf-edu-card">
        <div class="pf-edu-icon"><i class="fas fa-graduation-cap"></i></div>
        <div>
          <div class="pf-edu-degree">PhD Candidate</div>
          <div class="pf-edu-detail">Systems, Synthetic & Quantitative Biology</div>
          <div class="pf-edu-school">Harvard Medical School <span class="pf-muted">&middot; 2021 -- 2026</span></div>
        </div>
      </div>
      <div class="pf-edu-card">
        <div class="pf-edu-icon"><i class="fas fa-graduation-cap"></i></div>
        <div>
          <div class="pf-edu-degree">B.S. Mathematics</div>
          <div class="pf-edu-school">Northeastern University <span class="pf-muted">&middot; 2016 -- 2021</span></div>
        </div>
      </div>
    </div>

    <!-- Bio text -->
    <div class="pf-about-bio">
      <p>Co-advised by <a href="https://dbmi.hms.harvard.edu/people/arjun-raj-manrai">Raj Manrai</a> and <a href="https://dbmi.hms.harvard.edu/people/chirag-patel">Chirag Patel</a>, I focus on answering a deceptively simple question: <strong>what does it mean to be "normal" in medicine -- and how do those definitions shape clinical decisions?</strong> Using methods ranging from statistical learning to generative modeling, I unpack assumptions historically embedded in the definition of normal and develop more precise, data-driven definitions that better reflect the diversity and heterogeneity of patients in the era of precision medicine.</p>
      <p>I work across the full stack of clinical ML: from wrangling billions of longitudinal lab measurements across international health systems, to training transformer architectures for sequence prediction, to evaluating foundation models (GPT-4V, Gemini) for fairness in medical imaging. My work spans structured EHR data, medical images, and clinical text -- always with the goal of building systems that are both technically rigorous and clinically deployable.</p>
    </div>

    <!-- Skills: clean horizontal groups -->
    <div class="pf-skills-row">
      <div class="pf-skill-group">
        <div class="pf-chip-label">Scale & Data</div>
        <span class="chip">~2B lab measurements</span>
        <span class="chip">1.5M+ patient cohorts</span>
        <span class="chip">Multi-site international</span>
        <span class="chip">EHR, imaging, text</span>
      </div>
      <div class="pf-skill-group">
        <div class="pf-chip-label">Models & Methods</div>
        <span class="chip">Autoregressive transformers</span>
        <span class="chip">Vision-language models</span>
        <span class="chip">Bayesian inference</span>
        <span class="chip">Causal inference</span>
      </div>
      <div class="pf-skill-group">
        <div class="pf-chip-label">Stack</div>
        <span class="chip">Python</span>
        <span class="chip">PyTorch</span>
        <span class="chip">HuggingFace</span>
        <span class="chip">SQL</span>
        <span class="chip">AWS/GCP</span>
        <span class="chip">Docker</span>
      </div>
    </div>
  </div>
</section>

<!-- ==================== RESEARCH ==================== -->
<section class="pf-section pf-section-alt" id="research">
  <div class="pf-container-wide">
    <h2 class="pf-section-title">Research</h2>

    <div class="pf-research-intro">
      <p>In the nineteenth century, Adolphe Quetelet applied the Gaussian curve to human traits and introduced <em>l'homme moyen</em> -- the "average man." What began as a statistical abstraction became a clinical standard: the average defined the expected, and deviation from it signaled disease. Two centuries later, this logic still governs medicine. Reference ranges, diagnostic thresholds, and risk scores are derived from population aggregates. Patients are evaluated by proximity to a mean. But what is typical for a population is an imperfect guide to what is normal for a given patient. My research revisits this tension -- asking when population norms fail, what happens when we try to personalize them, and what biases emerge when we hand the task to AI.</p>
    </div>

    <!-- ======= NORMA ======= -->
    <div class="pf-research-area">
      <h3 class="pf-area-title">Redefining "Normal" in Laboratory Medicine</h3>

      <!-- Problem visual -->


      <div class="pf-research-text">
        <p>You get bloodwork done every year. Each time, every result comes back "normal." But your values have been slowly creeping upward -- a trajectory that, for <em>you</em>, signals something is wrong. The population-wide reference interval is too broad to notice. By the time a value finally crosses the threshold, the disease has been developing for months or years.</p>
        <p>The obvious fix -- comparing you only to yourself -- overcorrects in the other direction, flagging healthy fluctuations as abnormal. Neither population averages nor purely individual baselines solve the problem alone.</p>
      </div>

      <!-- Approach + impact visual -->


      <div class="pf-research-text">
        <p>We built NORMA, an autoregressive transformer trained on billions of longitudinal lab measurements, that generates reference intervals conditioned on both a patient's own history and population-level expectations for health. It catches disease signals months earlier than population intervals -- without the false-positive burden of purely personalized approaches.</p>
      </div>

      <div class="pf-research-meta">
        <div class="pf-pub-links">
          <a href="https://norma-tpy0.onrender.com/" class="pf-link-btn pf-link-btn-accent"><i class="fas fa-desktop"></i> Interactive Demo</a>
          <a href="https://github.com/aashnapshah/NORMA" class="pf-link-btn"><i class="fab fa-github"></i> GitHub</a>
        </div>
        <div class="pf-rcard-tags">
          <span>Transformers</span><span>Longitudinal EHR</span><span>Reference intervals</span><span>Precision medicine</span>
        </div>
      </div>
    </div>

    <!-- ======= ARC ======= -->
    <div class="pf-research-area">
      <h3 class="pf-area-title">Toward Individual-Level Features in Clinical Reference Equations</h3>

      <!-- Problem visual -->


      <div class="pf-research-text">
        <p>You take a breathing test at your doctor's office. The machine measures how much air you can exhale. But before your doctor interprets the result, the system adjusts your expected lung function based on your race -- using a different equation depending on which box you check. This practice has no clear biological basis and dates to the 1840s.</p>
        <p>Medical societies now recommend removing race, but simply dropping it from the equation -- by averaging or refitting -- doesn't address what race was standing in for. The question isn't whether to remove race. It's what to replace it with.</p>
      </div>

      <!-- Approach + impact visual -->


      <div class="pf-research-text">
        <p>We developed ARC, a framework that identifies the individual-level anatomical features -- sitting height, waist circumference -- that race was crudely proxying for. The resulting equations are built on your body, not your demographic group, and they are both more accurate and more equitable -- generalizing to populations where existing models fail.</p>
      </div>

      <div class="pf-research-meta">
        <div class="pf-pub-links">
          <a href="https://arxiv.org/abs/2512.00905" class="pf-link-btn"><i class="fas fa-file-alt"></i> Shah et al., 2025</a>
          <a href="https://pubmed.ncbi.nlm.nih.gov/41428343/" class="pf-link-btn"><i class="fas fa-file-alt"></i> Diao, Shah et al., JAMA Int Med 2026</a>
          <a href="https://github.com/aashnapshah/ARC" class="pf-link-btn"><i class="fab fa-github"></i> GitHub</a>
        </div>
        <div class="pf-rcard-tags">
          <span>Health equity</span><span>Pulmonary function</span><span>Reference equations</span><span>Spirometry</span>
        </div>
      </div>
    </div>

    <!-- ======= VLM / TRACE ======= -->
    <div class="pf-research-area">
      <h3 class="pf-area-title">Bias and Shortcut Learning in Medical AI</h3>

      <!-- Problem visual -->


      <div class="pf-research-text">
        <p>You upload a photo of a suspicious mole to an AI health tool. The model gives you a confident answer. But how reliable is that answer -- and would it be different if you had a different skin tone, or were older, or if the image were taken with a different camera? Foundation models like GPT-4V and Gemini Pro are increasingly used for medical image interpretation, but their accuracy varies systematically across patient demographics in ways that are invisible to the user.</p>
        <p>These models are designed with safety guardrails to prevent clinical diagnoses -- but we show these guardrails are trivially bypassed through simple prompt rephrasing.</p>
      </div>

      <!-- Approach + impact visual -->


      <div class="pf-research-text">
        <p>We systematically evaluate how vision-language models behave across patient subgroups, prompt strategies, and imaging domains -- and build interpretability frameworks (TRACE) that dissect what these models actually learn from medical images. The finding: models exploit acquisition protocols, pixel intensity patterns, and diagnostic labels as shortcuts, rather than learning meaningful anatomy. We identify what's needed before these models can be safely deployed: subgroup-level auditing and prompt-robustness testing as standard practice.</p>
      </div>

      <div class="pf-research-meta">
        <div class="pf-pub-links">
          <a href="https://openreview.net/forum?id=cO5E57hnfi" class="pf-link-btn"><i class="fas fa-file-alt"></i> Shah et al., ML4H @ NeurIPS</a>
          <a href="https://github.com/aashnapshah" class="pf-link-btn"><i class="fab fa-github"></i> GitHub</a>
        </div>
        <div class="pf-rcard-tags">
          <span>VLMs</span><span>Interpretability</span><span>Fairness</span><span>Chest X-rays</span><span>Shortcut learning</span>
        </div>
      </div>
    </div>

  </div>
</section>

<!-- ==================== PUBLICATIONS ==================== -->
<section class="pf-section" id="publications">
  <div class="pf-container">
    <h2 class="pf-section-title">Selected Publications</h2>

    <div class="pf-pub-list">

      <div class="pf-pub pf-pub-first-author">
        <div class="pf-pub-title">Disentangling Proxies of Demographic Adjustments in Clinical Equations</div>
        <div class="pf-pub-desc">Framework replacing race with measurable anatomy in clinical equations; validated across 147K participants</div>
        <div class="pf-pub-meta"><strong>A.P. Shah</strong>, J.A. Diao, E. Pierson, C.J. Patel, A.K. Manrai</div>
        <div class="pf-pub-venue"><em>In review</em></div>
        <div class="pf-pub-links">
          <a href="https://arxiv.org/abs/2512.00905" class="pf-link-btn"><i class="fas fa-file-alt"></i> arXiv</a>
          <a href="https://github.com/aashnapshah/ARC" class="pf-link-btn"><i class="fab fa-github"></i> Code</a>
        </div>
      </div>

      <div class="pf-pub pf-pub-first-author">
        <div class="pf-pub-title">Directing Generalist Vision-Language Models to Interpret Medical Images Across Populations</div>
        <div class="pf-pub-desc">Evaluating GPT-4V and Gemini Pro for fairness across dermatology, radiology, and pathology</div>
        <div class="pf-pub-meta">L. Sagers<sup>*</sup>, <strong>A.P. Shah</strong><sup>*</sup>, et al. <span class="pf-muted">(*equal contribution)</span></div>
        <div class="pf-pub-venue"><em>NeurIPS 2024 Workshop on GenAI4Health</em></div>
        <div class="pf-pub-links">
          <a href="https://openreview.net/forum?id=cO5E57hnfi" class="pf-link-btn"><i class="fas fa-file-alt"></i> OpenReview</a>
        </div>
      </div>

      <div class="pf-pub pf-pub-first-author">
        <div class="pf-pub-title">TRACE: A Data-Driven Framework for Explaining Subgroup Detection from Medical Imaging</div>
        <div class="pf-pub-desc">Interpretability framework dissecting how deep learning models recover demographics from chest X-rays</div>
        <div class="pf-pub-meta"><strong>A.P. Shah</strong>, J.A. Diao, A.K. Manrai, C.J. Patel</div>
        <div class="pf-pub-venue"><em>Manuscript in preparation</em></div>
      </div>

      <div class="pf-pub">
        <div class="pf-pub-title">A National Survey of Patient Preferences Regarding the Use of Race in Clinical Algorithms</div>
        <div class="pf-pub-desc">National survey of US adults on preferences for race in clinical decision-support</div>
        <div class="pf-pub-meta">J.A. Diao, R. Movva, L. Cheng, K. Kadoma, <strong>A.P. Shah</strong>, K. Ferryman, A.K. Manrai, E. Pierson</div>
        <div class="pf-pub-venue"><em>JAMA Internal Medicine</em>, 2026</div>
        <div class="pf-pub-links">
          <a href="https://pubmed.ncbi.nlm.nih.gov/41428343/" class="pf-link-btn"><i class="fas fa-external-link-alt"></i> PubMed</a>
        </div>
      </div>

      <div class="pf-pub">
        <div class="pf-pub-title">Advancing Medical Artificial Intelligence Using a Century of Cases</div>
        <div class="pf-pub-meta">T.A. Buckley, R. Conci, P.G. Brodeur, ..., <strong>A.P. Shah</strong>, et al.</div>
        <div class="pf-pub-venue"><em>arXiv</em>, 2025</div>
      </div>

      <div class="pf-pub">
        <div class="pf-pub-title">Automated Assessment of Large Language Models in Open-Ended Medical Prompts</div>
        <div class="pf-pub-meta">T.A. Buckley, Z. Kanjee, B. Crowe, A.M. Pettinato, <strong>A.P. Shah</strong><sup>*</sup>, et al.</div>
        <div class="pf-pub-venue"><em>Manuscript in preparation</em></div>
      </div>

      <div class="pf-pub">
        <div class="pf-pub-title">High-Performance Single-Cell Gene Regulatory Network Inference at Scale: the Inferelator 3.0</div>
        <div class="pf-pub-meta">C.S. Gibbs, C.A. Jackson, G. Saldi, <strong>A.P. Shah</strong>, et al.</div>
        <div class="pf-pub-venue"><em>Bioinformatics</em>, 2022</div>
        <div class="pf-pub-links">
          <a href="https://pubmed.ncbi.nlm.nih.gov/35188184/" class="pf-link-btn"><i class="fas fa-external-link-alt"></i> PubMed</a>
        </div>
      </div>

      <div class="pf-pub">
        <div class="pf-pub-title">Chimeric Fatty Acyl-Acyl Carrier Protein Thioesterases Provide Mechanistic Insight into Enzyme Specificity and Expression</div>
        <div class="pf-pub-meta">M. Ziesack, N. Rollins, <strong>A.P. Shah</strong>, et al.</div>
        <div class="pf-pub-venue"><em>Applied and Environmental Microbiology</em>, 2018</div>
      </div>

    </div>

    <p class="pf-muted" style="margin-top: 1.5em; font-size: 0.85em;">
      <a href="https://scholar.google.com/citations?hl=en&user=7RmZd8QAAAAJ"><i class="fas fa-graduation-cap"></i> Full list on Google Scholar</a>
    </p>
  </div>
</section>

<!-- ==================== FOOTER ==================== -->
<footer class="pf-footer">
  <div class="pf-container">
    <div class="pf-footer-inner">
      <div>
        <strong>Aashna Shah</strong><br>
        <span class="pf-muted">PhD Candidate, Harvard Medical School</span>
      </div>
      <div class="pf-footer-links">
        <a href="mailto:aashnashah@g.harvard.edu"><i class="fas fa-envelope"></i></a>
        <a href="https://github.com/aashnapshah"><i class="fab fa-github"></i></a>
        <a href="https://linkedin.com/in/aashna-p-shah"><i class="fab fa-linkedin"></i></a>
      </div>
    </div>
  </div>
</footer>
