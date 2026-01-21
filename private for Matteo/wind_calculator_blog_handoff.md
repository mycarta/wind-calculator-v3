# Wind Calculator Blog Post: Comprehensive Handoff Document

**Date:** January 20, 2026  
**Project:** Offshore Wind Calculator  
**Repository:** https://github.com/mycarta/wind-calculator  
**Purpose:** Blog post about adapting Ginsberg's Swept Area Method into open-source calculator

---

## Table of Contents

1. [Blog Post Overview](#1-blog-post-overview)
2. [Voice & Style Analysis](#2-voice-style-analysis)
3. [Writing Instructions](#3-writing-instructions)
4. [Detailed Outline](#4-detailed-outline)
5. [Draft Opening (Sections 1-3)](#5-draft-opening-sections-1-3)
6. [Remaining Sections Guide](#6-remaining-sections-guide)
7. [Content Sources & Attribution](#7-content-sources-attribution)
8. [Questions to Resolve](#8-questions-to-resolve)
9. [Publication Checklist](#9-publication-checklist)

---

## 1. Blog Post Overview

### Primary Focus
Write about **adapting Ginsberg's Swept Area Method into a useable, open-source calculator** for quick back-of-envelope offshore wind assessment.

### Secondary Elements
- Touch on intuitions (v³ relationship, EPF correction) - interesting but not primary
- Clarify terminology error (cubic vs. "exponential" misuse) - lightly, briefly

### Target Audience
- Geoscientists/geophysicists interested in energy applications
- Data scientists working on renewable energy projects
- Technical readers familiar with Python
- Energy professionals doing preliminary assessments

### Tone
Conversational but rigorous, enthusiastic but grounded, showing iterative improvement mindset

### Length Target
~2,500-3,500 words (substantial technical blog post)

---

## 2. Voice & Style Analysis

### Analysis of MyCarta Blog Posts

Based on detailed reading of:
- "Be a geoscience and data science detective" (2020)
- "Data exploration in Python: distance correlation and variable clustering" (2019)

### Opening Characteristics

**Conversational hook:**
- Opens with question or observation
- Direct address to reader ("if you are a geoscientist, and like me...")
- Personal context (mentions conferences, projects, inspirations)
- Sets expectations clearly ("Today I will walk you through...")

**Example opening pattern:**
```
These days everyone talks about data science. But here's a question: 
if you are a geoscientist, and like me you have some interest in data 
science (that is, doing more quantitative and statistical analyses 
with data), why choose between the two? Do both… always!
```

### Structural Approach

**Clear signposting:**
- Numbered/labeled sections ("First example", "Second example")
- Transparent transitions ("Now I am going to take a bit of a detour...")
- Playful markers ("Get ready for a ride!", "Before moving to the final fireworks...")

**Methodical progression:**
- Visual → quantitative → deeper statistical analysis
- Shows evolution of thinking ("But I was not satisfied yet")
- "Let's dig a bit deeper" as transition phrase

**Honest about process:**
- Mentions iterations and improvements
- Shows validation steps ("let's calculate a couple of values directly, to be sure")
- Acknowledges limitations/caveats at end of sections

### Code Presentation Style

**Inline with prose:**
- Code blocks shown directly in text flow
- Explains *why* code is improved, not just what it does
- Shows results (tables, figures) immediately after code
- Validates claims with direct calculations

**Example pattern:**
```python
# Show code block
def error_flag(pred, actual, stat, dev = 1.0, method = 1):
    """docstring..."""
    # implementation

# Then immediately: "I believe this new version is greatly improved because:"
# - Bullet point explanations
# - Show usage
# - Show results
```

### Figure/Table Presentation

**Detailed captions:**
- Full context in caption
- Source attribution
- Interpretation guidance

**Progressive revelation:**
- Show simple version first
- Then enhanced version
- Compare side-by-side when relevant

### Tone Markers

**Enthusiasm (grounded):**
- "Very cool!"
- "I am very pleased with these results"
- "That's very nice"
- "Excellent, it checks!"

**Self-aware humor:**
- "ha ha!"
- "putting the cart before the horses"
- "darn" (when fixing code errors)

**Critical but constructive:**
- "Please notice that I am not picking on this paper in particular, which in fact I rather quite liked, but I am critical of the lack of supporting statistics"
- Focuses on methodology, not people

**Iterative improvement:**
- "keep on improving your geo-computing projects"
- Shows updates to earlier work
- References previous posts naturally

### Pacing

**Paragraph length:**
- Typically 2-4 sentences
- Break up long technical explanations
- One idea per paragraph

**Sentence structure:**
- Active voice preferred
- Mix of short punchy sentences and longer explanatory ones
- Rhetorical questions to engage reader

**Section length:**
- Introduction: 3-4 paragraphs
- Main sections: 4-6 paragraphs each
- Transitions: 1-2 sentences
- Conclusions: 2-3 paragraphs

---

## 3. Writing Instructions

### Core Constraints

**DO NOT invent:**
- Wind resource data for Scotian Shelf beyond von Krauland proxy
- Claims about Ginsberg's work beyond what's in his book (pp. 56-62)
- Performance comparisons with other calculators
- Specific offshore wind projects or case studies
- Research findings not already verified

**OK to include:**
- Standard wind energy physics (P = ½ρAv³, Betz limit)
- Textbook explanations of EPF, efficiency factors
- von Krauland et al. (2023) data as stated (Northeast Atlantic US as proxy)
- Your own analogies from wind_power_intuition.md (coal trucks, firehose)
- Your implementation choices and rationale
- Screenshots of actual calculator interface

**If uncertain:**
- Ask before including
- Mark for fact-check
- Provide source reference

### Attribution Rules

**Specific claims:**
- Ginsberg (2019) for: Swept Area Method, EPF = 1.91, overall efficiency = 20%, worked example
- von Krauland et al. (2023) for: wind speeds, air density, turbine spacing factor
- Your documents (wind_power_intuition.md, etc.) for: framework, analogies, explanations

**General knowledge (no citation needed):**
- P = ½ρAv³ derivation
- Betz limit = 59.3%
- Jensen's inequality
- Basic calculus/physics

**Terminology error:**
- Cite "wind energy literature" generally
- Don't call out specific papers
- Focus on educational correction

### Voice & Style Guidelines

**Opening:**
- Start conversational, with hook question or observation
- Direct address ("if you're working on offshore wind...")
- Personal context (why I built this, what inspired it)
- Set clear expectations ("Today I'll walk you through...")

**Structure:**
- Clear signposting between sections
- Show evolution of thinking ("But then I realized..." "This led me to...")
- Methodical progression: problem → solution → validation
- Honest about limitations/caveats

**Tone:**
- Enthusiastic but grounded
- Use "I" voice naturally ("I really like this result")
- Self-aware humor when appropriate
- Show iteration/improvement ("keep on improving")
- Critical but constructive (about terminology error)

**Technical content:**
- Code blocks inline with prose when showing implementation
- Explain *why* choices were made, not just what
- Show results (calculator screenshots, validation checks) immediately
- Validate claims ("let's check this against Ginsberg's worked example")
- Don't shy away from equations, but build intuition first

**Pacing:**
- Short paragraphs (2-4 sentences typically)
- Active voice
- Clear transitions ("Now let's..." "But there's more to it...")
- Playful signposting okay ("Get ready for..." "Here's where it gets interesting")

**Figures/Code:**
- Detailed, informative captions
- Show before/after comparisons when relevant
- Screenshots of actual calculator interface
- GitHub links for full code
- Validate outputs against known values

### Avoid

**Over-formatting:**
- Excessive bold, italics, bullet lists
- Listicle style ("5 reasons why...")
- Wikipedia-style encyclopedic voice

**Defensive language:**
- "this is just my opinion"
- Apologetic tone about complexity
- Over-caveating (one limitation statement is enough)

**Jargon without definition:**
- Define technical terms on first use
- Explain acronyms (EPF = Energy Pattern Factor)
- Build from intuition to formalism

---

## 4. Detailed Outline

### Section 1: Hook - The Back-of-Envelope Problem (250 words)

**Key points:**
- Opening question: "How much power could we get from offshore wind here?"
- Why preliminary assessment matters (before $$ on measurements)
- The gap: rigorous methods exist, tools scarce/proprietary
- What this post covers: Ginsberg → open-source calculator

**Tone:** Conversational, problem-focused, sets stage

**Transitions:** "Today I'll walk you through..."

---

### Section 2: The Ginsberg Swept Area Method (400 words)

**Key points:**
- Formula: P = ½ρAv³
- Two key innovations:
  1. Energy Pattern Factor (EPF) = 1.91
  2. Overall Conversion Efficiency = 20%
- Worked example validation (D=50m case)
- Unit test implementation

**Technical content:**
- Show full worked example with numbers
- Explain EPF briefly (why ⟨v³⟩ ≠ ⟨v⟩³)
- List what efficiency includes
- Mention test guards against regressions

**Tone:** Pedagogical, building trust through validation

**Code snippet:** Possibly show test_ginsberg_worked_example structure

---

### Section 3: Adapting for the Scotian Shelf (450 words)

**Key points:**
- Data challenge: no Scotian Shelf offshore wind atlas
- Solution: NE Atlantic US proxy (von Krauland et al. 2023)
- Why it works: latitude, oceanography, meteorology
- Limitations upfront: proxy for planning, not finance
- Lookup table structure

**Critical statements:**
- "I'm explicit about this in the calculator's documentation: **this is a proxy**"
- "For actual project development... you need 1-3 years of site-specific measurements"
- Clear scope: "Is this promising?" not "Should we invest $2B?"

**Tone:** Honest, transparent about limitations

**Code snippet:** Show lookup table structure

---

### Section 4: Building the Calculator (500 words)

**Key points:**
- Why Panel: reactive, browser-based, no server
- Architecture: wind_calculations.py + Panel_app_pkg.ipynb
- Single turbine section walkthrough
- Site section walkthrough
- Unit conversions (kW/MW/GW, MWh/GWh/TWh)

**Screenshots needed:**
- Full calculator interface
- Single turbine section with example inputs
- Site section with turbine count calculation
- Unit selector dropdowns

**Tone:** Practical walkthrough, showing tool in action

**Code snippets:** Key function signatures, reactive decorator pattern

---

### Section 5: A Bit About the Physics (400 words)

**Key points:**
- Why v³ (briefly - "carrier is the cargo")
- Mass flow rate × energy density
- EPF correction: ⟨v³⟩/⟨v⟩³ ≈ 1.91
- Without it: 50% underestimate
- Link to deeper explanation (wind_power_intuition.md in repo)

**Analogies:**
- Coal trucks (delivery rate independent of cargo energy)
- Wind (air motion IS the energy)
- Firehose (one dial, two consequences)

**Tone:** Intuition-building, accessible physics

**Math level:** Show key formulas, explain conceptually

---

### Section 6: What "Efficiency" Really Means (350 words)

**Key points:**
- Ginsberg's "Overall Conversion Efficiency" = 20%
- What it includes:
  - Betz limit (59.3% max → ~40% real Cp)
  - Availability (~95%)
  - Wake losses (~10-15%)
  - Electrical losses (~3%)
  - Power curve effects (cut-in, rated, cut-out)
- Why 20-30% range
- Calculator warning on tight spacing + high efficiency

**Example calculation:**
```
0.593 × 0.42 × 0.96 × 0.90 × 0.97 ≈ 0.20
```

**Tone:** Demystifying, showing what's "under the hood"

---

### Section 7: A Terminology Note (200 words)

**Key points:**
- Light touch: "exponential" misuse in literature
- Correct: P ∝ v³ is cubic (polynomial)
- True exponential: P ∝ 2^v (variable in exponent)
- Why precision matters

**Approach:**
- Educational, not polemical
- "Widely used colloquially but technically incorrect"
- Link to wind_turbine_power_analysis_summary_2.md

**Tone:** Gentle correction, focus on clarity

**Length:** Keep brief (150-200 words max)

---

### Section 8: Limitations & When to Use This (400 words)

**Key points:**
- **Good for:**
  - Preliminary feasibility studies
  - Scenario comparisons
  - Technology screening
  - Educational purposes
  
- **NOT for:**
  - Project financing decisions
  - Environmental permitting
  - Turbine procurement
  - Grid interconnection studies

- **Scotian Shelf next steps:**
  - 1-3 year measurement campaign
  - Floating lidar or met mast
  - Measure-correlate-predict (MCP)
  - Site-specific Weibull parameters
  - Wake modeling

**Tone:** Responsible, clear boundaries

**Format:** Two columns or clear subsections

---

### Section 9: Try It Yourself (150 words)

**Key points:**
- GitHub repository link
- How to run:
  - Clone repo
  - Conda environment (wind-panel-app)
  - Open Panel_app_pkg.ipynb
  - Run all cells
- Test suite (pytest)
- Invitation for feedback/contributions

**Calls to action:**
- Try the calculator
- Report issues
- Suggest improvements
- Share use cases

**Tone:** Welcoming, community-oriented

---

**Total estimated length: ~3,100 words**

---

## 5. Draft Opening (Sections 1-3)

```markdown
## Building an Open-Source Offshore Wind Calculator: From Ginsberg's Method to a Working Tool

### The Back-of-Envelope Problem

If you're working on offshore wind development, sooner or later someone asks: "How much power could we get from wind farms here?" Maybe it's a stakeholder meeting about the Scotian Shelf. Maybe you're scoping a new region. Maybe you just want to understand if the numbers in a proposal make sense.

You need an answer, but you don't yet have the budget for a full wind resource assessment. Those cost hundreds of thousands of dollars and take 2-3 years. What you need is a **back-of-envelope** calculation—something quick, defensible, and transparent. Rigorous enough to guide decisions, but honest about its limitations.

The problem? Most preliminary assessment tools are either proprietary, buried in consulting reports, or don't clearly show their assumptions. I wanted something different: an open-source calculator that implements a well-documented methodology, makes its data sources explicit, and can be run in a browser.

Today I'll walk you through how I adapted **Michael Ginsberg's Swept Area Method** (from his 2019 book *Harness It*) into a working Panel calculator for offshore wind. Along the way, I'll show how I validated the implementation, where the data comes from, and why certain physics details—like the Energy Pattern Factor and that v³ relationship—actually matter for getting reasonable answers.

### The Ginsberg Swept Area Method

Ginsberg's approach is refreshingly direct. Wind power available in a turbine's swept area is:

**P = ½ρAv³**

Where ρ is air density, A is the rotor's swept area (πD²/4), and v is wind velocity. From this, you can calculate annual energy production if you know the average wind speed and account for two things:

1. **The Energy Pattern Factor (EPF)**: Wind speed varies constantly. Because power depends on v³, you can't just cube the average wind speed—you'd underestimate by about 50%. For a typical offshore wind distribution (Rayleigh, or Weibull shape parameter k=2), the correction factor is EPF ≈ 1.91. This gives you the mean power density:

   **P̄ₐ = ½ρ · EPF · v̄³  [W/m²]**

2. **Overall Conversion Efficiency**: Not all wind kinetic energy becomes electricity. Ginsberg uses 20% as a conservative planning value. This accounts for the Betz limit (~59% theoretical max, ~40-45% real turbines), availability (~95%), wake losses (~10-15%), electrical losses (~3%), and power curve effects (cut-in, rated speed capping, cut-out).

To validate my implementation, I reproduced Ginsberg's worked example exactly:

**Inputs:**
- Rotor diameter: 50 m  
- Average wind speed: 4.47 m/s  
- Air density: 1.225 kg/m³ (sea level)  
- EPF: 1.91  
- Efficiency: 20%

**Calculated outputs:**
- Power density: 104 W/m²  
- Swept area: 1,963.5 m²  
- Mean power: 204 kW  
- Annual energy (non-derated): 1,787 MWh/year  
- Annual energy (20% efficiency): 357 MWh/year

I included this as a unit test (`test_ginsberg_worked_example`) in the repository. If the calculation chain is correct, the test passes. This guards against implementation errors as the code evolves—exactly the kind of iterative improvement I wrote about in my [chapter for the Software Underground's *52 Things You Should Know About Geocomputing*](https://curvenote.github.io/testing-jupyter-export-52things/niccoli-keep-on-improving-geocomputing-projects.html).

### Adapting for the Scotian Shelf

Here's where it gets interesting. I wanted to apply this method to offshore Nova Scotia (the Scotian Shelf), but there's a problem: **there's no published offshore wind atlas for the Scotian Shelf**.

Environment and Climate Change Canada has limited offshore data. Most Canadian offshore wind resource assessments are preliminary or proprietary. So I needed a proxy—something published, comprehensive, and from a comparable region.

The solution: **Northeast Atlantic US data** from von Krauland et al. (2023), published in *Applied Energy*. Their "United States offshore wind energy atlas" provides wind speeds and air density at multiple hub heights (100m, 150m, 200m, 250m) for the continental shelf from Massachusetts to Virginia.

Why does this work as a proxy for the Scotian Shelf?

- **Similar latitude**: Both regions sit in the mid-latitude westerlies (40-45°N)  
- **Comparable oceanography**: Both influenced by the Gulf Stream, with similar continental shelf structure  
- **Same weather systems**: Nor'easters, extratropical cyclones, seasonal patterns  
- **Adjacent geography**: Georges Bank straddles the US-Canada boundary

Is it perfect? No. The Scotian Shelf is 3-8 degrees north, experiences seasonal sea ice, and has slightly different ocean currents. But for preliminary assessment—order-of-magnitude energy estimates, scenario comparisons, technology screening—it's the best available published data.

I'm explicit about this in the calculator's documentation: **this is a proxy**. For actual project development on the Scotian Shelf, you need 1-3 years of site-specific measurements (floating lidar or met mast), measure-correlate-predict with long-term reference data, and full wake modeling. The calculator is for the question "Is this promising enough to spend money investigating?" not "Should we invest $2 billion?"

The von Krauland data populates lookup tables in the code:

```python
air_density_lookup = {
    100: <value>,  # kg/m³ at 100m hub height
    150: <value>,
    200: 0.990,    # example value at 200m
    250: <value>
}

wind_speed_lookup = {
    100: <value>,  # m/s average at 100m
    150: <value>,
    200: <value>,
    250: <value>
}
```

Modern offshore turbines typically have hub height approximately equal to rotor diameter, so these lookups index by diameter (100m, 150m, 200m, 250m). Select a turbine size, and the calculator pulls the corresponding wind speed and air density for that height.
```

---

## 6. Remaining Sections Guide

### Section 4: Building the Calculator (500 words)

**Opening:**
"Now let's look at how the calculator actually works."

**Key narrative:**
- Why Panel? (reactive UI, browser-based, no deployment hassle)
- Show architecture diagram or describe flow
- Walk through single turbine section with screenshot
- Walk through site section with screenshot
- Mention unit conversions as UX feature

**Screenshots to prepare:**
1. Full calculator interface
2. Single turbine inputs/outputs
3. Site section showing turbine count calculation
4. Unit selector demonstration

**Code snippets:**
- Show `@pn.depends` decorator for reactivity
- Key function from wind_calculations.py (e.g., annual_power_density)
- Don't show full app code (link to GitHub)

**Transition out:**
"The calculator works, but why does it work? Let's dig a bit into the physics."

---

### Section 5: A Bit About the Physics (400 words)

**Opening:**
"If you're curious about that v³ relationship..."

**Structure:**
1. The fundamental question: why cube?
2. Mass flow rate (ρAv) × energy density (½ρv²)
3. Result: v appears three times
4. The "carrier is the cargo" insight
   - Coal trucks analogy (2 knobs)
   - Wind (1 knob, 2 consequences)
5. EPF correction necessity
6. Link to deeper dive

**Tone:**
- Intuition-building, not rigorous derivation
- "Think about it this way..."
- Keep math minimal (show result, not steps)

**Transition out:**
"That's the physics. But there's another number that matters just as much: efficiency."

---

### Section 6: What "Efficiency" Really Means (350 words)

**Opening:**
"The calculator lets you adjust 'efficiency' from 20-30%. What does that actually mean?"

**Structure:**
1. Ginsberg's "Overall Conversion Efficiency" = 20%
2. The compounding chain:
   ```
   Betz (59.3%) × Cp (42%) × Avail (96%) × Wake (90%) × Elec (97%) ≈ 20%
   ```
3. Why calculator allows 20-30% range
4. Spacing-efficiency warning feature
5. Comparison to capacity factor (different concept)

**Tone:**
- Demystifying
- "Here's what's packed into that single number"
- Practical (helps users make informed choices)

**Transition out:**
"Before we wrap up, a quick note on terminology..."

---

### Section 7: A Terminology Note (150-200 words)

**Opening:**
"You might see wind power described as 'exponentially' increasing with wind speed. That's not quite right."

**Structure:**
1. Common misuse: "power increases exponentially with wind speed"
2. Correct: P ∝ v³ is **cubic** (polynomial)
3. True exponential: P ∝ 2^v (variable in exponent)
4. Why it matters: different growth rates, different implications

**Tone:**
- Educational, not critical
- "It's used colloquially to mean 'grows fast,' but technically..."
- Brief, move on quickly

**Transition out:**
"Now, about when you should (and shouldn't) use this calculator..."

---

### Section 8: Limitations & When to Use This (400 words)

**Opening:**
"This calculator is designed for a specific use case. Let's be clear about what that is."

**Structure:**

**Good for:**
- Preliminary feasibility (is this region promising?)
- Scenario comparison (spacing A vs. B)
- Technology screening (100m vs. 200m turbines)
- Educational exploration (how does efficiency affect output?)

**NOT for:**
- Project financing (lenders need <10% uncertainty)
- Environmental permitting (requires site-specific EIA)
- Turbine procurement (manufacturers need detailed wind data)
- Grid studies (need hourly/sub-hourly profiles)

**For Scotian Shelf projects, next steps:**
1. Deploy floating lidar (1-3 years)
2. Measure-correlate-predict with reference data
3. Site-specific Weibull parameters
4. Wake modeling (Jensen, Larsen, etc.)
5. Foundation design (metocean data)

**Tone:**
- Responsible, transparent
- "Use this for what it's designed for"
- Not apologetic, just clear boundaries

**Transition out:**
"Ready to try it yourself?"

---

### Section 9: Try It Yourself (150 words)

**Opening:**
"The calculator and all the code are on GitHub."

**Structure:**
1. GitHub link: https://github.com/mycarta/wind-calculator
2. Quick start:
   ```bash
   git clone https://github.com/mycarta/wind-calculator.git
   conda env create -f environment.yml
   conda activate wind-panel-app
   jupyter notebook Panel_app_pkg.ipynb
   # Run all cells
   ```
3. Test suite: `python -m pytest -v`
4. Feedback welcome (GitHub issues)

**Calls to action:**
- Try the calculator with your own scenarios
- Report bugs or suggest features
- Share your use cases
- Adapt for your region (if you have better data)

**Closing:**
"I'd love to hear how you use it, or what improvements you'd suggest. Leave a comment below or open an issue on GitHub."

**Tone:**
- Welcoming, collaborative
- Community-oriented
- Open source ethos

---

## 7. Content Sources & Attribution

### Primary Sources

**Ginsberg, M. (2019). *Harness It: Renewable Energy Technologies and Project Development Models Transforming the Grid*. Business Expert Press.**
- Pages 56-62: Swept Area Method
- EPF = 1.91 (Rayleigh distribution)
- Overall Conversion Efficiency = 20%
- Worked example (D=50m, v=4.47 m/s)

**von Krauland, A.-K., Long, Q., Enevoldsen, P., & Jacobson, M. Z. (2023). United States offshore wind energy atlas. *Applied Energy*, 345, 121243.**
- Wind speeds by hub height (100-250m)
- Air density values
- Turbine spacing factor (5.98D)
- Northeast Atlantic US data

### Project Documents (Your Own Work)

**wind_power_intuition.md:**
- "Carrier is the cargo" framework
- Coal trucks vs. wind analogy
- Firehose example
- Cylinder mental model
- EPF explanation

**wind_turbine_power_analysis_summary_2.md:**
- Terminology analysis (exponential vs. cubic)
- Derivation from first principles
- Scaling relationships table

**Panel_app_pkg.ipynb & wind_calculations.py:**
- Implementation details
- Code structure
- Function signatures

### Attribution Format

**In text:**
- "Ginsberg (2019) recommends 20% for conservative planning"
- "von Krauland et al. (2023) provide wind speeds at..."
- "As I explored in my intuition document..."

**In code comments:**
- `# Source: Ginsberg (2019), pp. 56-59`
- `# Data: von Krauland et al. (2023)`

**In captions:**
- "Figure adapted from Ginsberg (2019)"
- "Data: von Krauland et al. (2023), Northeast Atlantic US"

### What NOT to Cite

**General physics (textbook knowledge):**
- P = ½ρAv³ derivation
- Betz limit = 59.3%
- Jensen's inequality
- Basic calculus

**Your own analysis/synthesis:**
- Proxy rationale (your argument)
- Implementation choices
- Calculator UX decisions
- Limitations discussion

---

## 8. Questions to Resolve

### From Initial Discussion

1. **Opening tone**: Does the draft match your voice? Too formal? Not enough personal touch?
   - Current: Conversational, problem-focused
   - Alternative: More personal ("I was frustrated by..." "I wanted...")

2. **Technical depth in Section 2**: Should I explain the derivation of P = ½ρAv³ (from KE = ½mv² and mass flow rate), or is stating it sufficient?
   - Current: State formula, explain components
   - Alternative: Full derivation in 2-3 paragraphs

3. **Section 3 length**: The proxy data explanation is ~450 words. Keep it, or condense to focus more on the calculator itself?
   - Current: Detailed justification for proxy choice
   - Alternative: Brief mention, link to docs/scotian_shelf_proxy.md

4. **Screenshots**: For Section 4 (Building the Calculator), what screenshots do you have/need?
   - Full calculator interface
   - Specific section close-ups
   - Results with example values
   - Before/after unit conversion

5. **Terminology section**: You said "lightly" on the exponential vs. cubic issue. Should this be:
   - Current plan: Brief section (150-200 words)
   - Alternative A: Brief aside in physics section (50 words)
   - Alternative B: Footnote with link to detailed analysis

6. **Code examples**: How much code to show inline vs. "see GitHub"?
   - Current: Key snippets (lookup tables, function signatures)
   - Alternative: More extensive (full functions with docstrings)

7. **Math formatting**: Use LaTeX/rendered equations or plain text?
   - Current: Plain text with Unicode (P̄ₐ = ½ρ · EPF · v̄³)
   - Alternative: Rendered LaTeX if blog supports it

8. **Personal touches**: Should opening mention specific inspiration moments?
   - Examples: "While reviewing Ginsberg's book for a course..."
   - Examples: "After seeing proprietary tools at conferences..."

### Additional Questions

9. **Target publication**: MyCarta blog, or elsewhere?
   - Affects: formatting, figure sizing, code syntax highlighting

10. **Companion materials**: Should blog post link to:
    - Live calculator demo (if deployed)
    - Video walkthrough
    - Jupyter notebook viewer (nbviewer)

11. **Acknowledgments**: Credit anyone who helped?
    - Reviewers
    - Software Underground community
    - Others

12. **License statement**: Include in post or just in repo?
    - Code: Apache 2.0
    - Text: CC-BY or similar

---

## 9. Publication Checklist

### Pre-Writing

- [ ] Resolve questions in Section 8
- [ ] Gather screenshots from calculator
- [ ] Test all code snippets in fresh environment
- [ ] Verify Ginsberg page numbers (56-62)
- [ ] Confirm von Krauland DOI link works

### Drafting

- [ ] Complete sections 4-9 following outline
- [ ] Match voice/tone from sections 1-3
- [ ] Add transitions between all sections
- [ ] Insert placeholder tags for screenshots
- [ ] Check all code snippets for accuracy

### Technical Review

- [ ] Validate all formulas against sources
- [ ] Run calculator with examples shown in post
- [ ] Test GitHub links (clone, environment setup)
- [ ] Verify pytest runs and Ginsberg test passes
- [ ] Check all numerical examples

### Content Review

- [ ] Read entire draft aloud (pacing check)
- [ ] Verify no invented claims
- [ ] Confirm all attributions present
- [ ] Check transitions flow naturally
- [ ] Ensure limitations clearly stated

### Figures & Code

- [ ] All screenshots captured at consistent resolution
- [ ] Figure captions written and detailed
- [ ] Code syntax highlighting applied
- [ ] All GitHub links tested and working
- [ ] Relative vs. absolute paths correct

### Final Polish

- [ ] Spell check
- [ ] Grammar check
- [ ] Link check (all URLs active)
- [ ] Formatting consistency (headers, code blocks)
- [ ] Meta description written (SEO)
- [ ] Tags/categories selected

### Pre-Publication

- [ ] Fact-check all technical claims one more time
- [ ] Have someone else read it (if possible)
- [ ] Verify blog platform formatting renders correctly
- [ ] Test code examples in clean environment
- [ ] Schedule publication time

### Post-Publication

- [ ] Share on appropriate channels (Twitter/X, LinkedIn, Software Underground)
- [ ] Monitor comments for questions
- [ ] Update post if errors found
- [ ] Track feedback for future improvements
- [ ] Consider follow-up posts based on interest

---

## Appendix: Key Formulas Reference

### Wind Power Fundamentals

```
P = ½ρAv³                          [instantaneous power]
P̄ₐ = ½ρ · EPF · v̄³                [mean power density]
A = πD²/4                          [swept area]
EPF ≈ 1.91                         [Rayleigh distribution]
```

### Energy Calculations

```
AEP_nd = P̄ × 8,760 hours          [non-derated annual energy]
AEP_d = η × AEP_nd                 [derated annual energy]
η = 0.20 to 0.30                   [overall efficiency]
```

### Site Calculations

```
Spacing = F × D                    [turbine center-to-center]
F = 5.98                           [default spacing factor]
N = Available_Area / (Spacing)²    [number of turbines]
Site_Power = N × P̄                 [total site power]
Site_AEP = N × AEP                 [total site energy]
```

### Ginsberg Worked Example

```
Given:
  D = 50 m
  v̄ = 4.47 m/s
  ρ = 1.225 kg/m³
  EPF = 1.91
  η = 0.20

Results:
  A = 1,963.5 m²
  P̄ₐ = 104 W/m²
  P̄ = 204 kW
  AEP_nd = 1,787 MWh/year
  AEP_d = 357 MWh/year
```

---

## Appendix: Voice Examples from MyCarta Blog

### Conversational Openings

**From "Be a geoscience detective":**
> "These days everyone talks about data science. But here's a question: if you are a geoscientist, and like me you have some interest in data science (that is, doing more quantitative and statistical analyses with data), why choose between the two? Do both… always!"

**From "Distance correlation":**
> "I learned about distance correlation from Thomas when we were starting to work on our 2018 CSEG/CASP Geoconvention talk..."

### Showing Process/Iteration

**From "Be a geoscience detective":**
> "But I was not satisfied yet. I was inspired to probe even deeper after a number of conversations with my friend Thomas Speidel..."

**From "Distance correlation":**
> "I really like the result in Figure 2. However, I want to have more control on how the pairwise plots are arranged..."

### Technical Validation

**From "Be a geoscience detective":**
> "So, the first thing I did then, was to look at the Root Mean Square Error in the upper and lower zone obtained using the fake top. They are summarized in the table below:"

**From "Distance correlation":**
> "That's very nice, but let's calculate a couple of values directly, to be sure:"

### Honest About Limitations

**From "Be a geoscience detective":**
> "Of course, there are some caveats to keep in mind, mainly that:
> * I may have introduced small, but perhaps significant errors with hand digitizing
> * I chose a statistical measure (the median and median absolute deviation) over a number of possible ones
> * I chose an arbitrary geologic reference horizon..."

### Enthusiasm Markers

- "Very cool!"
- "Excellent, it checks!"
- "That's very nice"
- "I am very pleased with these results"
- "Get ready for a ride!"

### Transitions

- "But let's dig a bit deeper"
- "Now I am going to take a bit of a detour"
- "Before moving to the final fireworks"
- "Here's where it gets interesting"

---

**End of Blog Post Handoff Document**

*Created: January 20, 2026*  
*For: Wind Calculator Blog Post*  
*Next session: Review questions, complete sections 4-9*
