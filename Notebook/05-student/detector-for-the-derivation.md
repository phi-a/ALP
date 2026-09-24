---
type: note
tags: [darkness, alp, student, detector, skipper-ccd]
created: 2026-09-24
updated: 2026-09-24
status: active
audience: student
---

# The detector, for your derivation

> Your derivation ends in one number: how many X-ray photons DarkNESS
> records. This page tells you what the detector does to the photons on
> the way, and which numbers you need for each step.

## The idea in one picture

Follow one photon made by an ALP converting in the Earth's magnetic
field. To be counted it has to:

1. **arrive from inside the field of view**
2. **land on the sensor**
3. **get through the thin metal window**
4. **be absorbed in the silicon**
5. **survive the event cuts**
6. **have its energy measured**

Each step keeps only a fraction of the photons. Your count is the
incoming brightness multiplied by all six fractions, then by the
observing time.

## Step by step

### 1. Field of view: which directions count

DarkNESS has no mirrors. Circular holes in front of the sensors let in
light from a cone **20° across** (10° from the centre line to the edge).
That cone covers a solid angle of **Ω ≈ 0.096 sr**.

The cone is fixed to the spacecraft. The mission chooses where to
point it, not how wide it is.

*Not known yet:* whether the sensitivity drops off toward the edge of
the cone. For now, assume every direction inside counts fully and every
direction outside counts zero. Say in your write-up that this is an
upper bound.

### 2. Area: how big the bucket is

Four sensors, each 1058 × 1278 pixels (1.35 million) of 15 µm, give a total
**area of 12 cm²**.

Area times solid angle is the **grasp**: 12 cm² × 0.096 sr ≈
**1.15 cm² sr**. For a signal that fills the sky, like ours, grasp is
the number that matters. A telescope with a huge mirror but a tiny field
of view can have less grasp than DarkNESS.

### 3. Window: a thin aluminium coat

A 50 nm aluminium layer blocks visible light. X-rays pass through: more
than **98 % get through above 1 keV**.

### 4. Silicon: does the photon stop?

The flight sensors are **500 µm** of silicon. A photon only counts if it
is absorbed there. Low-energy X-rays stop easily; high-energy ones can
pass straight through. At 10 keV about **98 %** are absorbed.

Steps 3 and 4 together are the **quantum efficiency**, QE(E), and it
depends on energy.

*Not known yet:* the thin inactive layer on the front of the sensor,
which lowers QE at 1–2 keV.

### 5. Event cuts: what we throw away

Charged particles in orbit leave long tracks on the image. We mask the
pixels around them, which leaves about **50 % of the area live**.

Radiation damage over the mission also smears X-ray hits into shapes
the software rejects, so a further fraction is lost. That fraction
grows with time and is not set yet.

**Important:** the particle rate depends on where the spacecraft is in
the Earth's magnetic field, and so does the ALP signal. So these losses
are not fixed numbers. Keep them as separate factors you can vary.

### 6. Energy: how well we measure it

The detector measures each photon's energy with a spread of about
**170 eV** (full width at half maximum) at 6 keV, possibly **200 eV**
after three years of radiation damage. The best silicon can ever do is
about **120 eV**, set by the Fano formula

$$
\sigma_E=\sqrt{F\,w\,E},\qquad F\approx0.12,\quad w\approx3.7\ {\rm eV}.
$$

The science band is **1–10 keV**.

For the smooth, extragalactic part of the ALP signal the exact
resolution hardly matters. For the narrow Milky Way line it sets how
much background sits under the line.

### Time

One observation lasts **15 minutes**, and one spectrum per observation
comes down to the ground. That is the finest time step you can use.
The mission plans **0.5–1 million seconds** in total.

Whether we only observe in the Earth's shadow is **still undecided**.
Keep observing time as a variable.

## Putting it together

$$
N = \underbrace{I}_{\rm brightness}\times
\underbrace{A\,\Omega}_{1.15\ {\rm cm^2\,sr}}\times
\underbrace{{\rm QE}(E)}_{\rm steps\ 3,4}\times
\underbrace{f_{\rm live}\,\epsilon_{\rm cuts}}_{\rm step\ 5}\times
\underbrace{T}_{\rm time}
$$

then spread over energy bins by step 6. In the real calculation $I$
changes with direction and time, so the multiplication becomes an
integral over the cone and over the observations.

**Check your work:** feed in a sky of constant brightness. Your formula
must give back exactly brightness × 1.15 cm² sr × QE × live fraction ×
time.

## Three rules

1. Keep every factor separate. Don't merge them into one "effective
   area" until the very end.
2. Apply each loss once. It is easy to count the 50 % twice.
3. When a number is marked *not known yet*, write it as a symbol and
   say so. Don't invent a value.

## Where these numbers come from

- Alpine et al. 2025, *DarkNESS: a skipper-CCD nanosatellite for dark
  matter searches*, Advances in Space Research 76, 4793
- The DarkNESS X-ray sensors paper (in preparation): silicon thickness,
  measured resolution, radiation damage

The full table with page numbers is [[../00-baseline/skipper-ccd]].
