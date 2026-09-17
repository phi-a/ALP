---
type: note
tags: [darkness, alp, physics]
created: 2026-07-28
updated: 2026-07-28
status: active
---

# Coherence sets the mass reach, and DarkNESS cannot move it

The mass axis of the exclusion plot is not a design variable. It is fixed by geometry that DarkNESS shares
with Suzaku, so a DarkNESS curve will improve on Yamamoto **vertically in coupling, not horizontally in
mass**. Worth internalising before the study starts, because it bounds what can be claimed.

## Where the mass limit comes from

Conversion stays coherent while the accumulated phase $qL$ stays below ~π (Yamamoto eq. 2.12):

$$
m_a < \sqrt{\frac{2\pi E_a}{L}} \equiv m_{\rm coh}
$$

Everything on the right is set by orbit and photon energy. $L$ is where the geomagnetic field dies off —
a few Earth radii, since $B \sim r^{-3}$ — and $E_a$ is the band, 1–10 keV for DarkNESS.

## Numbers for DarkNESS

Evaluated at $L = 6\,R_E$ (the integration path Yamamoto used for their IGRF calculation):

| $E_a$ | $m_{\rm coh}$ |
|---|---|
| 1 keV | 5.7×10⁻⁶ eV |
| 3.5 keV | 1.07×10⁻⁵ eV |
| 7 keV | 1.51×10⁻⁵ eV |

`DERIV`. So the DarkNESS curve will be flat below roughly 10⁻⁵ eV and turn upward as $m_a^2$ above it —
the same knee shape as Yamamoto's cyan region, in the same place.

**Weak lever available:** $m_{\rm coh} \propto L^{-1/2}$, so a shorter effective path pushes the knee to
*higher* mass while costing signal linearly in $B_\perp L$. That trade is almost certainly not worth
making, but it is the only mass-axis control the mission has, and it should be checked once rather than
assumed.

## A discrepancy in Yamamoto worth carrying forward

Their text quotes $m_{\rm coh} \simeq 3.3\times10^{-6}$ eV, but their published Figure 7 cyan curve has its
knee at $1.26\times10^{-5}$ eV (measured by digitising the figure — see the ALP replication notebook in
`darkmatter/ALP`). Backing out $L$:

- knee at 1.26×10⁻⁵ eV → $L \approx$ 4–9 $R_E$ for 3.5–7 keV — consistent with their stated "up to 6 times
  the Earth's radius" IGRF integration
- text value 3.3×10⁻⁶ eV → $L \approx$ 36–107 $R_E$ — not consistent with anything they describe

The figure agrees with the stated geometry; the text number is the outlier. **Do not inherit 3.3×10⁻⁶ eV.**
Compute $m_{\rm coh}$ from our own path integral, which we have to do anyway.

## Consequence for framing

At $m_a \lesssim 10^{-5}$ eV the QCD axion band sits at $g \sim 2\times10^{-15}$ GeV⁻¹. A DarkNESS limit
landing near $10^{-8}$ GeV⁻¹ is ~7 orders of magnitude above it. **The mission will not touch KSVZ or
DFSZ,** and neither did Yamamoto. The honest framing is a purpose-built test of the geomagnetic conversion
channel with controlled systematics, not a QCD axion search. Anything stronger will not survive review.

## Links

- part of [[../ALP]]
- upstream: [[alp-signal-chain]]
- reach: [[sensitivity-scaling]]
