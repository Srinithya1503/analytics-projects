# PharmaBrand-IQ: Model Interpretation & Business Recommendations

This document translates the outputs of `analytical_pipeline.py` into plain
business language for brand managers, marketing leads, and other
non-technical stakeholders. No coding or statistics background required.

---

## Part 1: What Are the 3 Physician Segments?

The clustering model (KMeans) grouped physicians into three segments based
on how much marketing activity they receive across three channels: digital
ads, sales rep visits, and free samples. Below is what each segment
represents and how a marketing team should treat it.

### 🟢 Segment 1: High-Touch Advocates
**Who they are:** Physicians who receive the highest overall marketing
investment — frequent sales rep visits, strong sample distribution, and
strong digital exposure.

**What it means for marketing:** These are your most "courted" physicians,
and it shows in the results — this segment has the highest average
prescription volume of the three. They are likely key opinion leaders or
high-potential prescribers already receiving a well-rounded commercial
effort.

**Recommended action:** Protect this investment. These relationships took
time to build and are currently paying off. Don't cut their touchpoints to
fund other segments — instead, look for ways to deepen engagement (e.g.
medical education invitations, peer-to-peer speaker programs).

---

### 🔵 Segment 2: Digital-First Responders
**Who they are:** Physicians whose engagement leans heavily toward digital
channels, with comparatively lighter in-person contact (fewer rep visits
and samples relative to their digital exposure).

**What it means for marketing:** This group is being reached, but mostly
through low-cost, scalable channels rather than expensive field resources.
Their prescription volume is moderate — there may be room to grow it with
smarter targeting rather than simply spending more.

**Recommended action:** Test whether a small, targeted increase in
in-person touchpoints (rather than more digital volume) lifts their
prescribing. This segment is a good candidate for cost-efficient pilot
programs before committing field resources broadly.

---

### 🟠 Segment 3: Low Engagement Profiles
**Who they are:** Physicians currently receiving the least overall
marketing attention across all three channels.

**What it means for marketing:** This is a "whitespace" segment — either
deliberately deprioritized, or simply overlooked. Some physicians in this
group still show decent prescribing behavior, which suggests untapped
potential if given more attention.

**Recommended action:** Don't assume low engagement means low value. Use
this list to identify physicians worth a low-cost outreach test (e.g. a
digital campaign or a single rep visit) before deciding whether they
deserve more investment.

---

## Part 2: Marketing Mix Model (MMM) Results

The regression model estimates how much each marketing channel contributes
to a physician's prescription volume (TRx), while holding the other
channels constant. Below is the template of what the console output looks
like when you run `analytical_pipeline.py`:

```
============================================================
MARKETING MIX MODEL RESULTS
============================================================

Model Fit (R-squared): 0.444
(This tells us what % of prescription variation is explained
 by our three marketing channels.)

Channel                         Coefficient     P-Value
-------------------------------------------------------
Baseline (Intercept)                48.4186      0.0000
Digital Ads (per impression)         0.0104      0.0000
Sales Rep Visits (per visit)         2.8983      0.0000
Samples Dropped (per sample)         1.4061      0.0000
```

*(Exact numbers will vary slightly each time the synthetic dataset is
regenerated, since it includes random real-world-style noise.)*

### How to Read This Table (No Stats Degree Needed)

- **Baseline (Intercept) — 48.4:** This is the "starting point" — roughly
  how many prescriptions a physician writes even with zero marketing
  activity, driven by other factors like patient volume or specialty.

- **Coefficient:** This is the estimated number of *extra* prescriptions
  gained per one additional unit of that channel.
  - Every **1 additional sales rep visit** is associated with about
    **2.9 more prescriptions**.
  - Every **1 additional sample dropped** is associated with about
    **1.4 more prescriptions**.
  - Every **1 additional digital ad impression** is associated with about
    **0.01 more prescriptions** — which sounds tiny, but digital
    impressions are typically delivered in the thousands, so the total
    impact can still be meaningful at scale.

- **P-Value:** This tells us whether we can trust the coefficient. A value
  below 0.05 means the result is statistically significant — i.e., it's
  very unlikely to be due to random chance. All three channels in this
  model are statistically significant.

- **R-squared (0.44):** This tells us that roughly 44% of the variation in
  prescriptions is explained by these three marketing channels alone. The
  rest is influenced by other factors not captured in this model (patient
  panel size, competitor activity, formulary access, etc.). For a
  three-variable commercial model, this is a solid, usable fit.

### Which Channel Has the Best ROI?

ROI isn't just about the coefficient size — it also depends on **cost per
unit**. A useful way to think about it:

| Channel | Est. Rx Lift per Unit | Typical Relative Cost per Unit | Efficiency Takeaway |
|---|---|---|---|
| Sales Rep Visit | ~2.9 Rx | High (rep time, travel, salary) | Powerful, but expensive — best reserved for high-potential physicians |
| Sample Dropped | ~1.4 Rx | Low–Medium (unit cost + logistics) | Strong, low-friction way to reinforce trial and prescribing habits |
| Digital Impression | ~0.01 Rx | Very Low (pennies per impression) | Individually small, but scales cheaply across thousands of physicians |

**Bottom line for a brand manager:** Sales rep visits generate the
strongest *per-touchpoint* impact, but they are also the most expensive
channel to scale. Digital has the smallest per-unit impact but the lowest
cost, making it efficient for reaching the long tail of physicians (like
the "Low Engagement Profiles" segment) cheaply. Samples sit in between —
a cost-effective way to reinforce messaging alongside rep visits.

---

## Part 3: Three Commercial Recommendations

1. **Reallocate rep time toward "Low Engagement Profiles" with real growth
   potential.** Rather than spreading rep visits evenly, use the
   segmentation output to identify low-engagement physicians whose
   specialty and past prescribing suggest upside, and pilot a small
   increase in visits to test the lift.

2. **Use digital channels to maintain "Digital-First Responders" cheaply,
   and free up rep capacity for higher-value segments.** Since this group
   already responds to lower-cost digital engagement, there's little need
   to add expensive field resources here — protect their prescribing with
   digital touchpoints and reserve reps for physicians who need it more.

3. **Set a minimum sample-drop threshold for high-potential physicians.**
   Since samples show a solid, statistically significant lift at a lower
   cost than rep visits, ensure no high-potential physician (regardless of
   segment) falls below a baseline sample allocation before cutting their
   marketing spend.

---

*Note: This interpretation is based on the model's statistical output. As
with any marketing mix model, these coefficients describe correlation and
estimated association, not guaranteed causation. Real-world decisions
should combine this analysis with field team judgment and market context.*
