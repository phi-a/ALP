---
type: note
tags: [darkness, alp, student, stage-0]
created: 2026-07-28
updated: 2026-07-28
status: active
audience: student
---

# Stage 0 — Orientation

> Before building anything, you need to know exactly what we are looking for, why the Earth is involved,
> and what we are and are not allowed to claim at the end.

No coding in this stage beyond running a notebook that already works. The output is understanding, and a
short document you will reuse in every talk and report you give on this project.

## The sentence to work toward

By the end of this stage you should be able to say something close to this, in your own words, without
notes:

> *We are testing whether dark matter decaying into light particles produces X-rays when those particles
> cross the Earth's magnetic field. One group has looked, using an old satellite's archived data, and saw
> nothing. We are asking how much better DarkNESS could look, and where it should point.*

Everything below is what you need to know to say that sentence honestly.

---

## Goal 1 — Know what we are assuming exists

There is a chain of assumptions here, and each link is a real assumption that could be wrong. You need to
be able to list them.

**The particle.** An axion-like particle, or ALP, is a hypothetical lightweight particle that can turn into
a photon when it passes through a magnetic field, and vice versa. That is the only property we care about.
Its strength is one number, called the coupling, written $g_{a\gamma\gamma}$. That number is the vertical
axis of Figure 7.

**Not the same as "the axion."** The QCD axion is a specific particle proposed to fix a specific problem in
particle physics. Because it was designed to solve that problem, its mass and its coupling are locked
together — it must lie on a line. An ALP is the generic version: same photon behaviour, but mass and
coupling are free and independent. **DarkNESS is looking for ALPs, not the QCD axion.** This distinction
explains most of Figure 7, and it is the first thing people will ask you about.

**Where the ALPs come from.** This is the assumption people forget, and it matters as much as the coupling.
Different experiments assume different sources:

| Source assumption | Who assumes it |
|---|---|
| ALPs produced in the Sun's core, streaming out now | CAST, IAXO |
| ALPs *are* the dark matter, sitting in the galaxy's halo | ADMX |
| Dark matter decays into ALPs, which stream in from all directions | **Us, and Yamamoto 2020** |

Ours is the third. Specifically: some heavy dark matter particle decays into two ALPs, each carrying half
its mass in energy. If that parent is a few keV in mass, the ALPs carry keV energies — which is why this is
an X-ray experiment, and why DarkNESS's 1–10 keV band is the right band.

**The conversion.** When an ALP crosses a magnetic field, it can turn into a photon. This is the same
physics as the Primakoff effect run backwards, which is why you will see it called the inverse or reverse
Primakoff effect. The probability depends on the strength of the field and how far the particle travels
through it.

**You have this goal when you can answer:**
- What is the difference between an axion and an axion-like particle?
- Where do the ALPs we are looking for come from, and what has to be true for them to exist?
- Why is this an X-ray experiment rather than a radio or optical one?

---

## Goal 2 — Know why the Earth is the magnet

**The one formula worth memorising.** The chance an ALP converts into a photon goes as

$$
P \;\propto\; \left(g_{a\gamma\gamma} \, B_\perp L\right)^2
$$

where $B_\perp$ is the magnetic field strength across the particle's path and $L$ is how far it travels
through that field. So what matters is not the field alone — it is **field times length**.

**Now the striking part.** Compare the biggest purpose-built magnet in this field with the Earth:

| | Field | Length | $B \times L$ |
|---|---|---|---|
| CAST magnet | 9 T | 9.3 m | ~84 T m |
| Earth's field from orbit | ~10⁻⁵ T | ~10⁷ m | **~100–140 T m** |

The Earth's field is a million times weaker. Its path is ten million times longer. The product comes out
**comparable or slightly better than the best magnet ever built for this purpose** — and it is free, and it
is already in place.

That is the entire reason this mission concept exists. Make sure you can explain it, because it is the most
compelling thirty seconds of any talk you will give about this project.

**What we give up in exchange.** A laboratory magnet is under your control: you know its field exactly, you
can turn it off, you can run controls. The Earth's field we can only calculate and observe. And CAST knows
its source — the Sun is right there and its ALP output is calculable. Our source is a hypothetical dark
matter decay whose rate we have to assume. **We trade control and a known source for an enormous free
magnet.**

**You have this goal when you can answer:**
- Why does a very weak field still give a competitive experiment?
- What does a lab experiment have that we do not?
- What single quantity should we be trying to maximise when we choose where to point?

---

## Goal 3 — Read Figure 7 correctly

Use the notebook for this. Run it, change things, watch what moves.

**Three kinds of statement share one plot,** and the drawing style is what tells them apart:

- **Filled regions are exclusions.** Someone looked, saw nothing, so couplings above that curve are ruled
  out. Real measurements, already done.
- **Lines are projections.** IAXO and the ADMX prospects have excluded nothing. They show what an
  experiment expects to reach. **Our result will be a line**, because DarkNESS has not flown yet.
- **The green band is a prediction.** It is where the QCD axion would live. Not a measurement, not an
  uncertainty, and *not a floor* — an ALP can sit anywhere on the plot, including below the band.

**Why everything opens upward.** Every curve is an *upper* limit. A stronger coupling means a bigger
signal, so seeing nothing rules out large couplings and says nothing about small ones. That is why no
filled region has a bottom edge.

**Where we live on this plot.** Upper left: masses below about 10⁻⁵ eV, couplings around 10⁻⁷ to 10⁻⁸
GeV⁻¹. The cyan and yellow regions are Yamamoto's result, and our line should land somewhat below them.

**Things to actually do:**
1. Run the notebook. Set `SMOOTH_OSCILLATION = False` and explain the spikes that appear.
2. Set `MATCH_PAPER = False` and explain what changed and why.
3. Change `M_COH_GAL` by a factor of two and explain which way the bend moves.
4. Find where the ADMX region is. Notice it is a narrow vertical sliver — work out why a resonant
   experiment covers only a tiny mass range at a time.

**You have this goal when you can answer:**
- Why is the cyan region flat and then bent?
- Why is being below the green band not a problem?
- If our result is 10⁴ times above the green band, has the project failed?
- Why will our result be drawn as a line and not as a filled region?

---

## Goal 4 — Be honest about what DarkNESS can and cannot do

This goal is as important as the physics. Every honest research project can state its own limits, and
being able to do this is what will make your talks credible.

**What DarkNESS can do:**

- Test a channel almost nobody has tested. Two papers exist on geomagnetic ALP conversion — one claimed a
  signal (XMM-Newton, later disputed on theoretical grounds) and one saw nothing (Yamamoto, Suzaku). That
  is the entire literature.
- Improve on the only clean existing measurement by roughly a factor of three or four in coupling.
- **Choose where to point.** Yamamoto used archived data from a satellite whose operators were not thinking
  about magnetic fields. We can pick geometry deliberately. This is our main advantage and it is your
  research contribution.
- Collect much more diffuse light per exposure than a focusing telescope, because our detector has a very
  wide field of view and this signal comes from everywhere at once rather than from a point.

**What DarkNESS cannot do:**

- **Reach the QCD axion.** We will land about seven orders of magnitude above the green band. Not close.
  Neither was Yamamoto.
- **Extend the mass range.** The upper mass limit comes from the size of the Earth's field and the energy
  of the X-rays. Both are fixed. Our curve will bend in the same place as Yamamoto's.
- **Beat CAST or IAXO on generic coupling limits.** Different source assumption, different channel. We are
  not competing with them, and claiming otherwise will be caught immediately.
- **Say anything unconditionally.** Our limit assumes a dark matter lifetime, a density, and a decay into
  ALPs. If those assumptions are wrong, the limit does not apply. Every number we publish carries them.

**The honest framing, which you should practise saying:** this is the first *purpose-built* test of
geomagnetic ALP conversion, with pointing chosen deliberately and systematic effects controlled — not a
search closing in on the axion.

**You have this goal when you can answer:**
- What is the strongest true claim we could make at the end of this project?
- What is a claim someone might expect us to make that we must not?
- Name one thing that, if it were false, would invalidate our result entirely.

---

## Deliverables for Stage 0

1. **A two-page write-up** covering all four goals, in your own words. Aim it at another undergraduate who
   has never heard of any of this.
2. **One slide** with Figure 7 on it and three sentences: what the plot shows, where we will appear, what
   that will mean. You will reuse this slide constantly.
3. **An oral check.** Sit down with your advisor and answer the twelve questions above without notes. If
   you can, Stage 0 is done.

## Time

Two to three weeks. Do not rush it. Every later stage is easier if this one is solid, and a student who
understands the target can debug their own code far better than one who does not.

## What to read

Only these, in this order:

1. The notebook's own text, which explains the figure as you go.
2. Yamamoto et al. 2020, **section 2 only** — the physics of the conversion. Skip the data analysis.
3. Yamamoto et al. 2020, **section 4.1**, the two paragraphs around equations 4.1 and 4.3 — those are the
   two results our project is trying to beat.

Do not read the whole paper yet. Do not go looking for axion review articles — they will bury you, and
almost none of them cover this specific channel.

## Links

- next: [[project-pathway]] Stage 1
- home: [[../ALP]]
- honest limits, in more depth: [[../01-physics/coherence-and-mass-reach]]
