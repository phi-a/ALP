---
type: result
tags: [darkness, alp, source, ceiling, conops, block-b]
created: 2026-09-24
updated: 2026-09-24
status: active
---

# 2026-09-24 — ceiling refresh: the continuum from the derived spectrum

Figure 6 of `jupyter/conops.ipynb` (the allowed-signal ceiling, D28)
scaled its continuum from `[Yam20]`'s ALP-flux *upper limit*,
$1.6\times10^{-9}$ erg s⁻¹ cm⁻² sr⁻¹ at $K = 10^4$ T² m², by
$(g/g_Y)^2\,\Gamma\tau_Y/K_Y$. Block B derived the spectrum
([[01-physics/block-b-source]]); the cell now uses it.

## What changed

Continuum counts are

$$
N_c = \int_{2}^{6}\frac{dI}{dE}\,dE\;
\times 2.45\times10^{-21}\Big(\frac{g}{10^{-10}}\Big)^2
\sum K\,\Delta t\;\times A\Omega\;\times\epsilon ,
$$

with `source.continuum_intensity(E, 7, share=1, tau_gyr=1/6.3e-3)`:
share 1 and $\tau = 1/(6.3\times10^{-3}\ \mathrm{Gyr^{-1}})$ put the
benchmark $f\,\mathrm{Br}/\tau$ into the lifetime. The integral is a
trapezoid on a 4001-point grid; the spectrum stops at $E_0 = 3.5$ keV,
so only 2–3.5 keV contributes. The line is the same formula as before,
now called through `source.line_intensity`. The continuum's mean photon
energy, which sets its coherence mass axis, comes from the same
spectrum: 2.73 keV, not the 4.17 keV of an $E^{1/2}$ law to 6 keV.

## Result

Reference day, 187-day science phase, D28 benchmark
($g = 5.8\times10^{-11}$ GeV⁻¹, $f\,\mathrm{Br}/\tau = 6.3\times10^{-3}$
Gyr⁻¹, 7 keV parent):

| | D28, `[Yam20]` scaling | now, derived |
|---|---|---|
| continuum per T² m², 2–6 keV, cm⁻² s⁻¹ sr⁻¹ | $6.4\times10^{-14}$ | $3.1\times10^{-14}$ |
| continuum counts | $1.2\times10^{-3}$ | $5.9\times10^{-4}$ |
| Milky Way line counts | $9.2\times10^{-3}$ | $9.2\times10^{-3}$ |
| coherence halves at | $1.7\times10^{-5}$ eV | $1.7\times10^{-5}$ eV |

The continuum is $0.48\times$ the D28 value, as Block B predicted. The
conclusion stands: the largest allowed benchmark is two orders below
one count on this schedule.

## Close

The ceiling now runs on the derived source alone; no `[Yam20]` limit
enters the count. 93 tests pass, scenario pins unmoved.

## Links

- decision: [[decisions]] D28 addendum
- derivation: [[01-physics/block-b-source]] §5
- code: `source.continuum_intensity`, `source.line_intensity`,
  `jupyter/conops.ipynb` figure 6
