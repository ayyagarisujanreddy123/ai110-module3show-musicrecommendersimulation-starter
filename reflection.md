# Reflection: Profile Comparisons and Experiment Findings

## Experiment 1 — Weight Shift (genre ÷2, energy ×2)

**Baseline (genre +2.0, energy ×1):** Top 5 for pop/happy/0.8 profile:
1. Sunrise City — 3.98 (genre + mood + energy)
2. Gym Hero — 2.87 (genre + energy, no mood match)
3. Rooftop Lights — 1.96 (mood + energy)
4. Carnival Lights — 1.95 (mood + energy)
5. Pixel Garden — 1.91 (mood + energy)

**Experiment (genre +1.0, energy ×2):** Same profile:
1. Sunrise City — 3.96 (genre + mood + energy×2)
2. Rooftop Lights — 2.92 (mood + energy×2)
3. Carnival Lights — 2.90 (mood + energy×2)
4. Pixel Garden — 2.82 (mood + energy×2)
5. Gym Hero — 2.74 (genre + energy×2, no mood)

**What changed and why it makes sense:** "Gym Hero" dropped from #2 to #5. In the baseline, its genre match (+2.0) compensated for the missing mood match. Once genre was halved, the energy gap (0.93 vs. 0.8 = 0.13 away) became more visible relative to mood-matching songs. The experiment confirmed that the baseline weights were letting genre override mood — a user asking for "happy" energy was getting an "intense" song as their second pick simply because it was also pop.

---

## Profile Comparison 1 — EDM/focused/0.9 vs. Acoustic/relaxed/0.3

**EDM profile top 3:**
1. Desert Frequency (electronic/focused) — 3.78
2. Focus Flow (lofi/focused) — 1.50
3. Storm Runner (rock/intense) — 0.99

**Acoustic profile top 3:**
1. Broken Compass (folk/melancholy) — 2.99
2. Morning Raga (world/relaxed) — 1.97
3. Coffee Shop Stories (jazz/relaxed) — 1.93

**What changed and why it makes sense:** The EDM profile correctly anchors on high-energy tracks — "Desert Frequency" wins by a wide margin, and even the lofi second-place pick has a matching "focused" mood. The large gap between first (3.78) and second (1.50) shows a healthy catalog match. The acoustic profile behaves differently: "Broken Compass" wins on genre+energy despite a mood *mismatch* (melancholy ≠ relaxed). This reveals genre dominance — the folk label was worth more than the mood. Meanwhile, Morning Raga (world/relaxed) and Coffee Shop Stories (jazz/relaxed) both have correct moods but wrong genres, yet rank below a wrong-mood folk song. A listener who actually wants relaxed acoustic music would likely prefer positions 2 and 3 over position 1.

---

## Profile Comparison 2 — Metal/intense/0.97 vs. Pop/happy/0.8

**Metal profile top 3:**
1. Neon Funeral (metal/intense) — 4.00 (perfect score)
2. Gym Hero (pop/intense) — 1.96
3. Storm Runner (rock/intense) — 1.94

**Pop profile top 3:**
1. Sunrise City (pop/happy) — 3.98
2. Gym Hero (pop/intense) — 2.87
3. Rooftop Lights (indie pop/happy) — 1.96

**What changed and why it makes sense:** The metal profile achieved a perfect 4.00 because the single metal song in the catalog was a flawless genre+mood+energy match. The pop profile scored 3.98 for the same reason. Both profiles correctly identify their genre's best song as #1. The interesting difference is positions 2 and 3: the metal profile falls back on *mood* (intense songs in other genres) because there are no more metal songs, while the pop profile falls back on *genre* (pop songs with wrong mood) because genre weight is 2× higher. This confirms that mood is the tiebreaker for underrepresented genres, while genre dominates for well-represented ones — an inconsistency that could feel unfair to listeners of niche genres.

---

## Key Takeaway

The scoring formula behaves predictably and the math is valid — scores always fall within expected ranges and the rankings respond logically to weight changes. However, the genre weight of +2.0 creates an implicit hierarchy: catalog-dominant genres (pop, lofi) are systematically easier to match well, while underrepresented genres (folk, metal) either achieve a perfect score (if the one catalog song matches) or fall off a cliff to mood/energy fallbacks. A fairer system would normalize by genre frequency or add partial genre similarity credit.
