---
type: note
tags: [darkness, alp, research]
created: 2026-06-22
updated: 2026-06-22
status: draft
---

# Designing and Simulating a LEO SmallSat ConOps for Reverse-Primakoff ALP Sensitivity

## Navigator

- home: [[ALP]]
- parent: [[../DarkNESS]]
- [Executive summary](#executive-summary)
- [Physics basis and literature](#physics-basis-and-literature)
- [Experiments and mission heritage](#experiments-and-mission-heritage)
- [Signal, background, and sensitivity model](#signal-background-and-sensitivity-model)
- [ConOps optimization and mission trades](#conops-optimization-and-mission-trades)
- [Simulation architecture, validation, and research merit](#simulation-architecture-validation-and-research-merit)

## Source Artifact

- canonical source: [[Designing and Simulating a LEO SmallSat ConOps for Reverse-Primakoff ALP Sensitivity.pdf]]
- working note: this markdown file is a readable transcription for search, linking, and editing
- preserve equations, figures, and original pagination in the PDF

![[Designing and Simulating a LEO SmallSat ConOps for Reverse-Primakoff ALP Sensitivity.pdf]]

## Executive summary

This report assumes that the instrument, budget, and schedule are still unspecified. Under that assumption, the cleanest SmallSat science case is **not** a general axion mission. It is a **targeted LEO search for geomagnetically modulated photon signals from relativistic axion-like particles**, using the reverse Primakoff effect in the Earth's field. The reason is simple. A SmallSat cannot compete with ground experiments by brute magnetic field strength. But it can exploit long coherent paths through the magnetosphere, repeated orbital modulation, and low-cost repetition of observing geometries that are difficult to achieve on the ground. Yamamoto et al. showed that the relevant line-of-sight magnetic integral can reach order $10^2$ Tm in LEO and used Suzaku data to place a null result on a field-correlated 2 to 6 keV contribution to the diffuse X-ray background. That makes their work the strongest empirical benchmark for this mission class.

The key physical lever is the coherent weak-mixing limit, where $P_{a\to\gamma}\propto g_{a\gamma\gamma}^2(B_\perp L)^2$. For an Earth-field path with $B_\perp L\sim 100$ Tm, the coherent conversion probability is only about $2.6\times 10^{-17}$ for $g_{a\gamma\gamma}=10^{-10}\,\mathrm{GeV^{-1}}$, and it falls to $2.6\times 10^{-19}$ and $2.6\times 10^{-21}$ for $10^{-11}$ and $10^{-12}\,\mathrm{GeV^{-1}}$, respectively. So the mission will almost certainly be **background dominated** unless the ALP source class is bright, line-like, or strongly modulated in a way that can be separated from backgrounds. This is why ConOps matter as much as hardware.

The strongest baseline architecture is therefore a **soft X-ray, wide-field, low-background, eclipse-favored observatory**. The recommended starting point is a 6U-class bus with either a collimated silicon-drift or skipper-CCD payload in roughly the 0.5 to 10 keV band, modest spectral resolution, anti-coincidence or aggressive particle filtering, and enough attitude control to execute repeatable anti-Sun, off-limb, and magnetic-meridian scans. Heritage exists. HaloSat demonstrated low-cost diffuse soft X-ray astronomy from a CubeSat and explicitly used anti-Sun nighttime observations to suppress solar-wind charge-exchange contamination. DarkNESS proposes a 6U nanosatellite with skipper CCDs, 1 to 10 keV sensitivity, a 20 degree field of view, and an eclipse-rich low-radiation operating concept. ASTERIA showed that arcsecond-class stability is possible in 6U when precision pointing is mission critical.

For optimization, the correct objective is **not** "maximize magnetic path length." Limb and high-latitude viewing can increase $B_\perp L$, but they also amplify atmospheric, albedo, and particle backgrounds. The science metric should instead maximize a weighted quantity like $\int S^2/(S+B)\,dt\,dE$, or its equivalent profile-likelihood Fisher information for $g_{a\gamma\gamma}$. In practice, that usually favors **Earth-shadow observing, anti-Sun or near-anti-Sun inertial pointings, and scheduled scans that build differential on-off magnetic templates**, while avoiding bright Earth limb and the South Atlantic Anomaly.

The research merit is real, but it has to be stated honestly. A LEO SmallSat is unlikely to supersede CAST, IAXO, or the best astrophysical bounds on generic $g_{a\gamma\gamma}$ in empty parameter space. Its value is different. It can test a **distinct experimental channel** that is sensitive to **geomagnetically converted, orbital-phase-modulated, keV-band ALP signatures**. That channel is complementary to helioscopes, haloscopes, and light-shining-through-wall experiments. It becomes especially compelling if the mission is framed as a null test or confirmation test for Earth-field conversion scenarios like those explored with XMM-Newton and Suzaku, and if it is designed to improve on Yamamoto-like analyses through better grasp, cleaner background modeling, and purpose-built pointing control.

## Physics basis and literature

Axion-like particles couple to electromagnetism through the standard interaction term $ \mathcal{L}\supset -\frac14 g_{a\gamma\gamma} a F\tilde F = g_{a\gamma\gamma} a\,\mathbf{E}\cdot\mathbf{B}$. In an external magnetic field, one linear photon polarization mixes with the ALP state. In the weak-mixing limit relevant to most LEO scenarios, the conversion probability along a ray path can be written as
$$
P_{a\to\gamma}(E,\hat n,t)\simeq \frac{g_{a\gamma\gamma}^{2}}{4}\left|\int_{\rm los} B_\perp(s,\hat n,t)\,
e^{\,i\int_0^s q(s')ds'}\,ds\right|^{2},
$$
with momentum mismatch
$$
q(s)=\frac{m_a^2-\omega_{\rm pl}^2(s)}{2E}.
$$
For a uniform field and negligible phase mismatch, this reduces to the familiar coherent limit $P_{a\to\gamma}\simeq (g_{a\gamma\gamma}B_\perp L/2)^2$. This is the same core formalism behind helioscopes, many astrophysical conversion searches, and modern Fourier-domain conversion calculations in inhomogeneous magnetic fields.

For a LEO mission, the natural ALP mass range is the one that preserves coherence across magnetospheric path lengths and keV photon energies. The exact boundary depends on plasma frequency, viewing geometry, and magnetic-field structure, so it must be simulated rather than assumed. But the literature is clear on the regime. For low-mass ALPs, plasma and field inhomogeneity matter more than naive vacuum formulas suggest, and "resonant" shortcuts can fail in realistic plasmas. That argues for a full line-of-sight propagation kernel in the simulator, not a single-domain approximation unless it has been validated against the full integral.

The most relevant source classes for a SmallSat reverse-Primakoff mission are summarized below.

| Signal class                                         | Expected spectrum                                                                                                                                  | Why it matters in LEO                                                                                                                                                                                            | Source |
| ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| Solar axions or ALPs                                 | Broad soft X-ray continuum, typically strongest below a few keV, with model dependence from Primakoff, bremsstrahlung, and Compton-like production | Can convert in the Earth's field or, in a different mission concept, in solar magnetic structures. Strongest motivation for Sun-aware ConOps, but also strongest contamination risk from solar activity and SWCX |        |
| Diffuse extragalactic or cosmological ALP background | Broad continuum. In decay-driven scenarios it is often redshift broadened                                                                          | Best matched to wide-field soft X-ray surveys and orbital modulation analyses                                                                                                                                    |        |
| Line-like ALP signal from two-body parent decay      | Narrow line in parent rest frame, broadened by Doppler, cosmology, and instrument response                                                         | Strongly favored by high-resolution line searches and differential on-off magnetic templates                                                                                                                     |        |
| Polarization-bearing converted photons               | Geometry-dependent linear polarization signature                                                                                                   | Nice-to-have discriminator if area is not sacrificed too much, but not the primary driver for first mission design                                                                                               |        |

A focused literature review points to three especially important facts. First, the experimental ALP field is now broad and mature. Ground programs span helioscopes, haloscopes, dielectric haloscopes, and light-shining-through-wall experiments. Second, space-based Earth-field conversion analyses are still sparse and not yet settled. Fraser et al. reported a seasonally modulated XMM-Newton excess consistent with solar axions converted in the geomagnetic field, while Roncadelli and Tavecchio argued that the proposed axion interpretation was physically inconsistent. Yamamoto et al. then performed a more direct field-correlation search with Suzaku and found no evidence for an ALP-induced component. Third, modern review literature stresses that realistic plasma and magnetic-field structure matter. That makes simulation quality central, not optional.

The parameter space that a LEO mission should scan first is therefore a **mission-driven** rather than purely theory-driven box: $m_a$ from very small values up into the point where coherence across magnetospheric scales begins to fail, and $g_{a\gamma\gamma}$ from roughly $10^{-13}$ to $10^{-10}\,\mathrm{GeV^{-1}}$. The lower end overlaps with IAXO-style aspirations and strong astrophysical limits. The upper end includes the territory historically probed by CAST-scale helioscopes and some Earth-field claims. That keeps the simulation physically relevant while avoiding a parameter domain the mission cannot realistically touch.

## Experiments and mission heritage

The existing ALP search landscape is highly complementary. Ground experiments dominate raw coupling reach because they can use strong, purpose-built magnets or resonant structures. CAST set a world-leading helioscope limit of $g_{a\gamma}<0.66\times 10^{-10}\,\mathrm{GeV^{-1}}$ for $m_a\lesssim 0.02$ eV in its final vacuum phase. IAXO is designed to reach down to about $10^{-12}\,\mathrm{GeV^{-1}}$ in favorable regions. ALPS II reported first science results in 2025 with a limit near $1.5\times10^{-9}\,\mathrm{GeV^{-1}}$ for very low masses and plans further upgrades. MADMAX has already demonstrated a first dielectric-haloscope search near 77 to 80 $\mu$eV with limits around $2\times10^{-11}\,\mathrm{GeV^{-1}}$. HAYSTAC continues to push microwave-cavity searches near 17 to 19 $\mu$eV, and ABRACADABRA has set leading limits in the neV regime. A LEO SmallSat will not replace any of these. It offers a different observable. It measures **orbital and directional conversion in the Earth environment**.

| Experiment or mission | Platform | Main method | Most relevant result for this study | Source |
|---|---|---|---|---|
| CAST | Ground | Solar helioscope | $g_{a\gamma}<0.66\times10^{-10}\,\mathrm{GeV^{-1}}$ for $m_a\lesssim 0.02$ eV | |
| IAXO | Ground, planned | Next-generation helioscope | Target sensitivity down to $\sim10^{-12}\,\mathrm{GeV^{-1}}$ and strong Figure-of-Merit logic for $B^2L^2A$ and background suppression | |
| ALPS II | Ground | Light shining through wall | First science run excluded $g_{a\gamma\gamma}\approx1.5\times10^{-9}\,\mathrm{GeV^{-1}}$ at low mass and upgrades are underway | |
| MADMAX prototype | Ground | Dielectric haloscope | First search reached $g_{a\gamma}\sim2\times10^{-11}\,\mathrm{GeV^{-1}}$ near 77 to 80 $\mu$eV | |
| HAYSTAC Phase II | Ground | Microwave cavity haloscope | Extended quantum-limited search in the 17 to 19 $\mu$eV range | |
| ABRACADABRA-10 cm | Ground | Broadband axion-photon search | World-leading neV-scale limits down to $3.2\times10^{-11}\,\mathrm{GeV^{-1}}$ | |
| XMM-Newton seasonal analysis | Space | Search for seasonally modulated Earth-field conversion | Reported a modulated excess consistent with solar axion interpretation | |
| Roncadelli and Tavecchio critique | Theory on archival space result | Validity test of the XMM claim | Argued the claimed solar-axion interpretation was not physically consistent | |
| Suzaku Earth-field search | Space | Correlation of diffuse X-ray background with geomagnetic path integral | Null result. Upper limit on residual 2 to 6 keV contribution. Strongest direct benchmark for LEO geomagnetic ALP searches | |

For SmallSat design specifically, the heritage is better than it may look at first glance. HaloSat proved that a CubeSat can do scientifically credible diffuse soft X-ray survey work if the science is matched to a large grasp and a wide field of view. It used three small collimated detectors, reached a total grasp of $17.6\,\mathrm{cm^2\,deg^2}$ at 600 eV, and deliberately observed toward the anti-Sun direction during orbital nighttime to reduce solar-wind charge-exchange foregrounds. That operating logic is directly relevant here.

DarkNESS is even closer to the desired mission class. The uploaded 2025 paper describes a 6U nanosatellite concept built around four skipper CCDs, a roughly 20 degree field of view, and a 1 to 10 keV science band. The mission concept emphasizes low-radiation orbit selection, Earth-shadow operations, line-sensitive dark-matter searches, and a simple spacecraft bus with average power near 32 W, peak power near 38 W, total mass about 10.3 kg, and science data around 105 Mb per day with downlink capacity around 708 Mb per day. Those numbers are not the answer for an ALP mission, but they are an excellent starting envelope for mass, power, thermal design, and data rate.

Other missions provide narrower but still useful heritage. MinXSS showed that commercial silicon-drift detectors can deliver about 0.15 keV FWHM energy resolution at 5.9 keV in a 3U spacecraft, with 0.5 to 30 keV coverage and low power. PolarLight demonstrated a CubeSat-compatible gas-pixel X-ray polarimeter and also produced one of the most useful modern analyses of in-orbit CubeSat X-ray background. ASTERIA demonstrated 0.5 arcsecond RMS pointing stability and $\pm 10$ mK thermal control in a 6U for precision photometry. SSAXI is not yet a flight heritage mission, but it is directly relevant because it is a SmallSat axion concept. It proposed MiXO optics with CMOS X-ray sensors in 0.5 to 6 keV, optimized for solar axion signatures in the 3 to 4.5 keV band. EZIE, launched in 2025, is not an ALP mission, but it is highly relevant as a modern 3-by-6U magnetic remote-sensing architecture with drag-based formation control and automated operations.

Balloon work matters mainly as instrument heritage, not as direct LEO analog. PoGO+ and XL-Calibur show that X-ray polarimetry missions benefit strongly from anti-coincidence shields, detailed Geant4 background modeling, and explicit optimization against atmospheric neutron and photon backgrounds. Those lessons carry cleanly into a SmallSat photon-conversion mission. A balloon does not reproduce the LEO environment. But it does teach what background-rejection discipline looks like when the expected polarization or excess is small.

## Signal, background, and sensitivity model

The end-to-end count model should be written in the detector domain, not only in flux space. For time bin $i$ and reconstructed energy bin $j$,
$$
\mu_{ij}=S_{ij}+B_{ij},
$$
with
$$
S_{ij}=\int_{\Delta t_i}\!\!dt\int dE\int d\Omega\;
I_a(E,\hat n,t)\,P_{a\rightarrow\gamma}(E,\hat n,t)\,A_{\rm eff}(E,\hat n,t)\,R_j(E)\,\epsilon_{\rm cuts}(E,t),
$$
and
$$
B_{ij}=B_{\rm CXB}+B_{\rm SWCX}+B_{\rm particle}+B_{\rm albedo}+B_{\rm straylight}+B_{\rm instrumental}.
$$
This is the right level because most decision variables in ConOps act through time dependence, pointing dependence, and cut efficiency.

A useful benchmark comes from the coherent limit. If $B_\perp L=100$ Tm, then
$$
P_{a\to\gamma}\approx 2.6\times10^{-17}
\left(\frac{g_{a\gamma\gamma}}{10^{-10}\,\mathrm{GeV^{-1}}}\right)^2
$$
before plasma suppression, field reversals, and atmospheric transmission losses are applied. This tiny probability is the core design truth. The signal model only becomes favorable when at least one of three things happens. The ALP source is bright. The converted photons are spectrally sharp. Or the observing program creates a robust temporal or directional modulation template. That is exactly why a LEO mission should prioritize differential analyses instead of absolute photometry alone.

The dominant backgrounds depend on band and pointing. In the soft X-ray regime, particle backgrounds are often set by high-energy electrons and secondary electrons, while diffuse sky photons and SWCX dominate the celestial foreground. High-latitude and high-inclination orbits generally increase the non-X-ray background because geomagnetic cutoff rigidity falls and particle access rises. SAA passages add delayed activation, though some missions find that the induced component decays quickly enough to be masked with modest dead time. Near the bright Earth limb, atmospheric and albedo contributions rise sharply. In harder X-rays and gamma rays, Earth albedo becomes a first-order photon background. In all cases, background varies with orbit, space weather, and pointing. A static template is not enough.

| Background | Physical origin | When it is worst | What to model first | Source |
|---|---|---|---|---|
| Trapped electrons and protons | Geomagnetic belts and SAA activation | High inclination, SAA, storm times | AP9/AE9-style environment, orbit masks, activation tails | |
| Prompt charged-particle background | Galactic cosmic rays and secondaries in spacecraft mass | Polar regions, quiet geomagnetic shielding loss | Geant4 mass model and event morphology cuts | |
| SWCX and magnetospheric foregrounds | Solar-wind ions exchanging charge with neutrals in heliosphere or magnetosheath | Sun-facing geometries, variable solar wind | Anti-Sun scheduling, solar-wind proxies, dedicated calibration fields | |
| Atmospheric absorption and near-limb transmission loss | Residual column density along tangent line of sight | Limb-grazing views at low tangent altitude | NRLMSISE-00 or occultation-calibrated atmosphere model | |
| Earth albedo photons and neutrons | Atmospheric production and reflection | Nadir and limb, especially above several keV | Albedo templates and Earth-avoidance angles | |
| Sunlight and stray light | Optical and solar X-ray contamination, thermal loading | Sunlit operations and near-Sun angles | Baffle model, eclipse gating, Sun-angle rules | |
| RFI and spacecraft EMI | Internal electronics, wheels, torquers, radios | During downlink, wheel ramps, torque events | Quiet-science windows and housekeeping-based vetoes | |

The sensitivity metric should match the expected analysis. For a background-dominated search with $S\ll B$, the common detection significance behaves like
$$
{\rm SNR}\approx \frac{S}{\sqrt{B}}.
$$
Since the signal scales as $S\propto g_{a\gamma\gamma}^2$, the coupling reach scales only as the **fourth root** of exposure in a null search. That is an important design consequence. Doubling observing time helps, but improving background or increasing the differential magnetic response can help just as much. In this regime, a natural scalar objective is
$$
J \equiv \sum_{i,j}\frac{S_{ij}^2}{S_{ij}+B_{ij}}
\approx \sum_{i,j}\frac{S_{ij}^2}{B_{ij}},
$$
or the equivalent profile-likelihood Fisher information on $g_{a\gamma\gamma}^2$. This is the quantity to optimize over pointing schedules. It naturally balances more magnetic signal against more background.

A second metric is **detection probability under paired ConOps**. Define "on" and "off" states that preserve most backgrounds while changing $P_{a\to\gamma}$. Then
$$
\Delta S \propto g_{a\gamma\gamma}^2(\kappa_{\rm on}-\kappa_{\rm off})T,
$$
with $\kappa$ the geometry-weighted conversion kernel. This differential metric is particularly valuable for LEO because orbital phase, eclipse state, geomagnetic latitude, and line-of-sight magnetic geometry can all be modulated without changing the instrument. That is one of the strongest strategic arguments for the mission.

## ConOps optimization and mission trades

The best ConOps depend on which source class is primary. If the mission is aimed at a **diffuse or line-like ALP background arriving from outside the magnetosphere**, then the baseline should be **eclipse-only anti-Sun inertial observing with controlled scan offsets**. That configuration suppresses direct solar contamination, reduces SWCX relative to Sun-facing geometries, and keeps the bright Earth well away from the boresight while still allowing the line of sight to traverse structured geomagnetic field. This is close to the logic HaloSat used for diffuse soft X-ray science, and it is compatible with the DarkNESS-style eclipse-rich operating concept.

If the mission is aimed at **solar axions**, the trade changes. Sunward views improve source flux, but they sharply raise requirements on baffling, thermal control, and foreground discrimination. That is why SSAXI uses focusing optics, modest field of view, and solar-minimum operations. A first mission should only adopt solar-first ConOps if the payload is designed around that use case from the start. Otherwise, solar mode should be a secondary observing program.

Limb pointing is tempting because it can increase path length through magnetized plasma and, in some geometries, raise $B_\perp L$. But it is also the easiest way to lose the experiment. Atmospheric columns rise rapidly at low tangent altitude. Earth albedo and scattered backgrounds rise. Thermal and stray-light constraints worsen. Proper optimization will often show a maximum at **moderate Earth avoidance**, not at the geometric limb itself. That is the kind of result the simulator must be built to find.

The most useful first-pass pointing strategies are compared below.

| Pointing mode | Signal leverage | Background risk | Operational complexity | Best use | Initial verdict |
|---|---|---|---|---|---|
| Earth-shadow anti-Sun inertial | Moderate to high | Low | Low | Baseline diffuse or line search | **Best starting mode** |
| Earth-shadow magnetic-meridian scan | High differential leverage | Low to moderate | Moderate | Build on-off magnetic templates | **Best science optimization mode** |
| Moderate off-limb scan | Potentially higher $B_\perp L$ | Moderate to high | Moderate | Trade-study only | **Maybe useful in narrow windows** |
| Bright-limb grazing | High geometric path | Very high | High | Stress test, not baseline science | **Usually reject** |
| Nadir | Low ALP sensitivity | Earth backgrounds dominate | Low | Calibration and Earth albedo characterization | **Use as control mode** |
| Sunward or near-Sun | Very high for solar source models | Very high | High | Solar-axion campaign only | **Secondary unless mission is solar-first** |

The instrument trade is similarly clear.

| Candidate instrument concept | Heritage anchor | Energy band | Main advantage | Main limitation | Source |
|---|---|---|---|---|---|
| Wide-field skipper CCD spectrometer | DarkNESS-like | 1 to 10 keV | Very low noise, line sensitivity, diffuse-survey compatible | Slow readout and modest pointing in current concept | |
| Collimated silicon-drift detector spectrometer | HaloSat, MinXSS | 0.5 to 30 keV | Simple, compact, mature, moderate resolution, good grasp for diffuse signals | Limited imaging and polarization information | |
| Gas-pixel detector polarimeter | PolarLight | 2 to 8 keV | Polarization sensitivity and event morphology | Small effective area and tighter source-rate limits | |
| Focusing MiXO plus CMOS imager | SSAXI-like | 0.5 to 6 keV | Strong for solar-core morphology and source discrimination | Narrow field and Sun-centered operations | |

A mission-constraint table is useful even this early because it prevents "analysis drift" into unbuildable concepts.

| Heritage reference | Form factor | Mass | Power | Data | Cost |
|---|---|---:|---:|---:|---:|
| DarkNESS concept | 6U | 10.3 kg | 32.3 W average, 37.6 W peak | 105 Mb/day science, 708 Mb/day downlink capacity | Unspecified |
| HaloSat | 6U | Unspecified in source used here | Unspecified in source used here | Unspecified in source used here | < $4M |
| ASTERIA | 6U | 10 kg | Unspecified in source used here | Unspecified in source used here | Unspecified |

Sources: DarkNESS, HaloSat, ASTERIA

The orbit trade is important. A low-altitude, low-to-moderate inclination orbit minimizes many particle backgrounds and resembles the successful Suzaku and DarkNESS logic. A higher-inclination orbit provides stronger geomagnetic variation and better modulation leverage, but it pays in trapped-particle exposure and activation. Because the science is background dominated, both should be simulated explicitly. The likely answer is a Pareto front, not a single winner. My recommended design study begins with two orbit families. The first is around 400 to 550 km and $i\lesssim 30^\circ$. The second is around 500 km and ISS-like to mid-inclination. A dawn-dusk Sun-synchronous orbit is less attractive for a diffuse eclipse-favored mission, though it can be attractive for a dedicated solar concept.

## Simulation architecture, validation, and research merit

The recommended simulation architecture is modular. It should separate geometry, propagation physics, detector response, and inference. That keeps the code auditable and lets you swap source models without rewriting the whole stack.

At minimum, the simulator needs these components:

**Orbital geometry.** Propagate orbit and eclipse using a high-fidelity but fast propagator with J2, drag, and Sun-Earth geometry. Include Earth occultation, limb angle, bright-Earth angle, SAA masks, local time, and geomagnetic latitude. HaloSat and DarkNESS both show that these geometry variables directly shape diffuse X-ray data quality and safe operations.

**Attitude and pointing profiles.** Implement discrete and continuous strategies: fixed inertial anti-Sun, stepped great-circle scans, magnetic-meridian tracking, nadir control, and limb-offset modes. Include realistic slew rate, settle time, Sun-angle keep-out, momentum management, and data-taking dead time. If the bus is based on present 6U heritage, include both "coarse" and "precision" pointing options so the science value of ASTERIA-class stability can be quantified instead of assumed.

**Instrument model.** Represent aperture or effective area, bandpass, spectral redistribution, particle rejection, polarization response if present, dark noise, read cadence, dead time, and on-board thresholds. For soft X-ray concepts, response should be stored in ARF-like and RMF-like products so the same pipeline can ingest heritage data and simulated data. DarkNESS, HaloSat, MinXSS, PolarLight, and SSAXI collectively span the realistic design space.

**Magnetosphere and field models.** Use the Earth's internal field from the IGRF family and an external-field model from the Tsyganenko family, driven by solar-wind and geomagnetic inputs where relevant. If a current version is needed, IGRF-14 is the present standard release. The simulator should allow ablations with internal field only, internal plus T96, and internal plus T05-like storm-aware external fields. That is important because the signal may depend on the same space-weather conditions that also alter backgrounds.

**Photon propagation and conversion.** This module should compute the full line integral with phase accumulation, not only the coherent shortcut. For broad scans, use the coherent formula as a fast approximate mode. For shortlisted ConOps and high-priority parameter points, rerun with the full integral. Modern Fourier and FFT-based methods are well suited here and can accelerate large parameter sweeps.

**Background models.** Use NRLMSISE-00 for atmospheric density and tangent-column calculations. Use AP9/AE9-style trapped-particle environments, plus empirical masks or learned corrections where known model biases matter. Seed diffuse photon backgrounds from CXB and Earth albedo templates, and add SWCX proxies or dedicated nuisance components. Then propagate the whole environment through a Geant4 mass model of the payload. This is standard practice in modern CubeSat and LEO high-energy mission work.

**Optimization and inference.** Start with a coarse Latin-hypercube or grid search over orbit family, Earth-avoidance angle, local-time window, eclipse gating, and scan law. Then refine with Bayesian optimization or evolutionary multi-objective search. Use profile likelihoods or Bayesian posterior predictive checks to estimate detection probability and coupling limits. The objective should be a Pareto set over science, power, data, and risk, not a single scalar.

The validation plan should be strict. First, reproduce known limits or scaling laws before exploring new designs. Reproduce CAST-like coherent scaling in a vacuum test. Reproduce Yamamoto's order-of-magnitude $B_\perp L$ and sensitivity normalization in a simplified Suzaku-like geometry. Reproduce HaloSat anti-Sun scheduling logic and show that your SWCX nuisance component behaves sensibly. Reproduce PolarLight-like particle background dominance in a similar orbital environment. Then inject synthetic ALP signals with known coupling and verify unbiased recovery. Only after those tests should the optimizer be trusted.

The source list to prioritize is short and should stay primary-first. For theory, start with Irastorza and Redondo, Graham et al., and Marsh et al. for conversion in realistic magnetic fields. For experimental benchmarks, start with CAST, IAXO, ALPS II, MADMAX, HAYSTAC, and ABRACADABRA. For space-based Earth-field searches, prioritize Fraser, Roncadelli and Tavecchio, and Yamamoto. For mission design, prioritize the uploaded DarkNESS paper, HaloSat, MinXSS, PolarLight, ASTERIA, SSAXI, and official NASA or JPL documentation for current missions like EZIE. For environment models, prioritize IGRF, Tsyganenko, NRLMSISE-00, and AE9/AP9, then supplement with mission-specific background papers like PolarLight and DIXE.

The next experimental step should be modest and concrete. Build a Phase 0 simulator around a DarkNESS-like 6U envelope and two orbit families. Compare three payload options: skipper CCD, silicon-drift detector, and gas-pixel detector. Use 2 to 6 keV as the first benchmark band because Yamamoto gives a direct empirical reference there. Optimize five ConOps modes: anti-Sun eclipse, magnetic-meridian eclipse, off-limb moderate, nadir control, and solar-special mode. Require every candidate schedule to return not only expected coupling reach, but also calibration time, data volume, thermal margin, SAA dead time, and model-risk score. That will rapidly show whether the mission is science-limited or systematics-limited.

The concise research merit statement is this. A LEO SmallSat reverse-Primakoff mission can open a **distinct and under-tested search channel** for low-mass ALPs by coupling the Earth's long magnetic path lengths to modern low-cost soft X-ray instrumentation and differential orbital modulation. Its best-case reach is not a universal replacement for helioscopes or haloscopes. Its value is that it probes a different observable tied to dark-matter and dark-radiation scenarios that can produce keV-band ALP signals. If designed around low-background eclipse operations, purpose-built differential ConOps, and validated field-plus-background simulation, it can materially improve the experimental status of Earth-field ALP conversion and either tighten or decisively test the remaining observational space suggested by earlier archival claims.




