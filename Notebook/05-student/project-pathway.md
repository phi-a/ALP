---
type: plan
tags: [darkness, alp, student, pathway]
created: 2026-07-28
updated: 2026-09-17
status: active
audience: student
---

# Project pathway

> Written for you, the student. Read this one first, then start at Stage 0.

## What we are trying to find out

A hypothetical particle called an axion-like particle (ALP) might turn into an X-ray photon when it
passes through a magnetic field. The Earth has a magnetic field. So a satellite in orbit, looking outward,
might see a faint extra X-ray glow caused by ALPs converting in the Earth's field on their way in.

In 2020 a group looked for exactly this in old data from a Japanese satellite called Suzaku. They saw
nothing, which let them say "if ALPs existed with a strong enough coupling, we would have seen them — so
the coupling must be smaller than X." That is their published limit.

**Our question: could DarkNESS do better, and where should it point?**

The second half matters more than it sounds. The strength of the signal depends on how much magnetic field
lies along the direction the satellite is looking. Suzaku's operators were not thinking about magnetic
fields at all, so they got whatever they happened to get. We can choose. That choice is the research.

## How this project is built

Seven stages. Each stage is **one question, one script, one figure, one number you can check.**

The checking part is the important part. At every stage there is a number you should get, from a paper or
from a hand calculation. If you get it, move on. If you don't, something is wrong and you find it before
building anything on top. This is how you make progress without needing someone to tell you whether you
are right.

**Rules that will save you a lot of pain:**

1. Finish a stage before starting the next one. A finished stage means the figure exists and the check
   passes. Half-finished stages that all get built at once is the single most common way these projects die.
2. Save your output to a file at the end of each stage. The next stage reads that file. Do not build one
   enormous script.
3. Use libraries for hard things. Do not write your own magnetic field model.
4. If you are stuck for two hours, stop and ask. Bring: what you expected, what you got, and the smallest
   piece of code that shows the problem.

---

## Stage 0 — Orientation

**Question:** what exactly are we looking for, why is the Earth involved, and what may we honestly claim?

Full instructions are in their own note: **[[stage-0-orientation]]**. Four goals — know what we assume
exists, know why the Earth works as our magnet, read Figure 7 correctly, and be able to state what
DarkNESS can and cannot do.

**Hand in:** a two-page write-up, one reusable slide, and an oral check with your advisor.

**You'll know it's right when:** you can answer the twelve questions in that note without notes.

**Time:** 2–3 weeks. Do not rush it — every later stage is easier if this one is solid.

---

## Stage 1 — Where is the satellite?

**Question:** where is DarkNESS at any given moment?

**What you do:** write a script that computes the satellite's position over one day for a circular orbit
at 500 km. Write this one yourself — it is about fifteen lines of trigonometry and it teaches you the
coordinate systems you will need later. Plot the ground track (the path traced on a map of the Earth).

**Hand in:** a ground track plot for one day.

**You'll know it's right when:**
- your orbital period is about **94 minutes** at 500 km, or about **93 minutes** at the ISS altitude of
  420 km
- the ground track looks like a sine wave that shifts westward on each orbit
- the highest and lowest latitudes it reaches equal the orbit's inclination

**The trap:** there are several different ways to describe a position near Earth — one fixed to the stars,
one that rotates with the Earth, and one in latitude/longitude/altitude. Mixing them up is the most common
bug in this entire project, and it usually looks like a ground track that drifts wrong or a magnetic field
that comes out at the wrong place. Write down which one you are using at every step.

**Time:** 2 weeks.

---

## Stage 2 — How strong is the field there?

**Question:** what is the Earth's magnetic field at the satellite?

**What you do:** use the field model in the repo (`load_igrf` and `igrf_field` in `src/darknessalp/` —
two function calls; `lmax=1` gives the simple dipole). For each point along your orbit from Stage 1, get
the magnetic field vector. Plot its strength over one day.

**Hand in:** a plot of field strength versus time for one day, and the same values plotted on a world map.

**You'll know it's right when:**
- the field strength is roughly **20,000 to 50,000 nanotesla**
- it is *weakest* over the South Atlantic, off the coast of Brazil. This is the South Atlantic Anomaly, and
  seeing it appear in your own plot is the confirmation that your coordinates are right
- it is strongest near the magnetic poles

**Time:** 1–2 weeks.

---

## Stage 3 — How much field is along our line of sight?

**Question:** if the satellite looks in a particular direction, how much magnetic field does an incoming
ALP travel through?

This is the first real physics result, and there is a beautiful check for it.

**Do this on paper first.** The Earth's field falls off as one over distance cubed. If you integrate that
from the Earth's surface outward to infinity, you get roughly

$$
B_0 \times \frac{R_E}{2} = 3\times10^{-5}\ {\rm T} \times \frac{6.4\times10^{6}\ {\rm m}}{2} \approx 100\ {\rm T\,m}
$$

So before writing any code, you already know the answer should be around **100 tesla-metres**. Now write
code that gets it.

**What you do:** pick a moment and a direction. Step outward from the satellite along that direction in
small steps, out to about ten Earth radii. At each step get the field, take the part of it that is
perpendicular to your viewing direction, and add it up.

**Hand in:** one number, in tesla-metres, plus a plot showing how the running total builds up as you go
outward.

**You'll know it's right when:**
- looking straight up from the magnetic equator at 420 km gives **83 T m** (the hand calculation above,
  times $(R_E/r)^2$); other directions give anything from 5 to 340 T m
- squaring the typical values gives 10⁴–10⁵ T²m², which is what the 2020 paper reports
- the running total *flattens out* — almost all the contribution comes from close to Earth, so extending
  from 10 to 20 Earth radii should barely change the answer. Check this.

**One subtlety worth understanding:** the field changes direction along the path. When it flips, the
contributions partly cancel. That cancellation is real and it *reduces* the signal. If you take absolute
values inside your sum, you will remove the cancellation and get an answer that is too big. This is an easy
mistake and a good one to deliberately test.

**Time:** 2–3 weeks. This is the hardest stage.

---

## Stage 4 — Where should we point?

**Question:** which direction gives the strongest signal, and how does it change as the satellite orbits?

This is where you stop reproducing and start producing. Nobody has this plot.

**What you do:** take Stage 3 and run it for many directions instead of one. Make a map over the whole sky
of the field integral, for one moment. Then do it for several moments around one orbit and see how the map
changes.

**Hand in:** a sky map of the field integral, and a short description of where the good directions are and
whether they move as the satellite goes around.

**You'll know it's right when:** the pattern makes physical sense — and it is less obvious than it
sounds. The biggest values are always just above the Earth's limb (the longest path through strong
field). From the magnetic equator, straight up is the *smallest* sky direction, not looking along the
field: a straight line leaves a curved field line. Only at high magnetic latitude, where the field lines
are nearly straight, does looking along them give a small answer (about 5 T m). Check the equator case by
hand: straight up should be 83 T m and along the axis should be twice that.

**The idea that makes this research rather than a calculation:** we do not only want the strongest possible
pointing. We want *both* strong-field and weak-field pointings, taken under otherwise identical conditions.
The weak-field pointings act as a control group — the ALP signal is only in the strong ones, but the
background is in both, so comparing the two is how you tell them apart. A campaign that only ever looks at
maximum field cannot distinguish an ALP signal from a slightly wrong background estimate.

So the real output here is a **pair** of pointing directions: one across the field, one along it, as
similar as possible in every other respect.

**Time:** 3 weeks.

---

## Stage 5 — What could we detect?

**Question:** how small a coupling could DarkNESS rule out?

**What you do:** there is an existing sensitivity calculation for a different DarkNESS science goal. You
will reuse it and swap in this signal. Before trusting it, use it to reproduce the 2020 paper's published
limit using *their* satellite's numbers.

**Hand in:** the reproduced Suzaku limit, then the DarkNESS number.

**You'll know it's right when:** feeding in Suzaku's numbers gives back roughly their published values of
3.3×10⁻⁷ and 8.4×10⁻⁸ GeV⁻¹. If you cannot reproduce a published result with published inputs, the
pipeline is wrong and any new number it produces is meaningless.

**Set your expectations now:** we think the honest answer is an improvement of about a factor of three or
four. Not a hundred. If you get a hundred, something is wrong, and finding out what is more valuable than
the number was.

**Time:** 3 weeks.

---

## Stage 6 — Put it on the picture

**Question:** what does our result look like next to everyone else's?

**What you do:** add a DarkNESS curve to the Figure 7 notebook from Stage 0. Draw it as a **line**, not a
filled region — filled means "excluded by a measurement," and ours is a projection of what a future
mission could do.

**Hand in:** the final figure, and a short report: what we assumed, what we calculated, what we found, and
what we are unsure about.

**Time:** 2 weeks.

---

## What you will have at the end

- A figure nobody has made before (Stage 4)
- A sensitivity projection for a real mission (Stages 5–6)
- A written report and a conference-poster-worth of material

Stages 0–4 alone are a complete, presentable semester of work. If Stages 5–6 slip to a second semester,
that is normal and fine.

## What not to do yet

Not because these are bad ideas, but because they will swallow you before the foundation exists:

- Do not try to optimise the pointing automatically. Look at maps by eye first.
- Do not model the backgrounds from scratch. Use what exists.
- Do not add the external magnetic field model, atmospheric absorption, or spacecraft thermal constraints.
  All real, all later.
- Do not read the whole 2020 paper at once. Section 2 for Stage 0, section 3 for Stage 3.

## Links

- mentor's version: [[mentor-guide]]
- home: [[../ALP]]
- the deep version of the same plan: [[../04-plan/research-plan]]
