---
layout: single
title: "Research"
permalink: /research/
author_profile: true
---

### Adaptive Modeling to Personalize Laboratory Reference Intervals 
**Routine blood tests** — from complete blood counts (CBC) to metabolic and lipid panels — are vital for detecting and managing a wide range of conditions. But their interpretation depends on **population-based reference intervals** — the "normal ranges" against which results are compared.

While useful, these population-based norms often overlook **individual variation** and fail to leverage a person's own medical history. That means early, subtle shifts in someone's health can be missed - especially if results still fall within the population range.

My work develops **adaptive, hybrid models** that blend the broad applicability of population-based intervals with the precision of personal baselines. Using over **20 years** of longitudinal records from **Clalit Health Services** (4.9M+ members), I apply statistical and generative models to dynamically update reference intervals as more individual data becomes available.

I compare three approaches:

- **Population-based**: the traditional standard.
- **Personalized setpoints**: individual-specific baselines.
- **Hybrid adaptive**: population priors refined with each patient's data.

The goal: improve **sensitivity** and **specificity** for predicting disease progression, especially when data is sparse or noisy, without overdiagnosis.

### Replacing Course Demographic Stratification in Reference Equations  
**Developing equitable PFT reference equations using sitting height and body morphology**

Pulmonary function tests (PFTs) have long relied on race-based reference equations, a practice that lacks biological justification and risks perpetuating health disparities. To address this, we developed **ARC**, a framework that identifies individual-level anatomical proxies to explain group-level differences in lung function. Using large-scale data from NHANES and the UK Biobank (**n ≈ 160,000**), we found that **sitting height** consistently outperforms race in explaining lung function variance, while socioeconomic variables contribute minimally.

Building on this, we introduced **ARCPFT**, a new reference equation that replaces race with sitting height and waist circumference. ARCPFT improves prediction accuracy — reducing error by up to **24% in Black individuals** — and generalizes more effectively across Asian and Hispanic populations. This work illustrates how physiologically grounded, data-driven models can advance both **clinical precision** and **equity** in respiratory care.

---

### Shortcuts in Image-Based Anomaly Detection  
**Prompt sensitivity and subgroup performance in Gemini Pro and GPT-4 Vision**

As vision-language models (VLMs) like **Gemini Pro** and **GPT-4 Vision** gain traction in clinical imaging tasks, questions remain about their reliability in detecting anomalies. In this project, I systematically benchmark these models across three diagnostic settings: **skin cancer classification**, **chest X-ray abnormality detection**, and **histopathological diagnosis**. While both models are designed with safety constraints, I show that minor changes in prompt phrasing — such as reframing tasks as "spot-the-difference" or "matching" — elicit **confident diagnostic outputs**, often without appropriate safeguards.

I further examine how **prompt structure**, **image modality**, and **patient subgroup characteristics** (e.g., skin tone, age) influence model performance. While Gemini Pro outperforms GPT-4 overall, both models demonstrate **shortcut learning behaviors** and reduced accuracy on underrepresented subgroups. These findings highlight critical vulnerabilities in current VLM deployment and emphasize the need for **prompt-robustness** and **subgroup fairness** in medical image analysis.

---
<!-- 
### Demographic Inference and Shortcut Learning in Chest X-Rays  
**Understanding how deep models infer sensitive attributes from medical images**

Deep learning models can infer demographic attributes — such as age, sex, and race — from chest X-rays with surprising accuracy, even when these features are not visibly encoded. This raises fundamental questions about what cues models rely on. We present **TRACE**, a framework for dissecting the **shortcuts** underlying demographic inference in medical imaging.

TRACE combines **image distortion tests**, **proxy variable modeling** (e.g., BMI, lung size, device use), and **embedding-level transfer analysis** to identify which features contribute to model predictions. Our results show that models often exploit indirect signals: **view position (AP/PA)**, **pixel intensity patterns**, and co-occurring clinical markers — rather than meaningful anatomy. These findings expose hidden pathways for bias and raise concerns about the **fairness and transparency** of deep models used in clinical workflows. -->
