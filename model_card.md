# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder suggests songs from a 20-song catalog based on a user's preferred genre, mood, and energy level. It is designed for classroom exploration only — not for real users or production deployment. It assumes the user can express their taste as a single genre, mood, and numeric energy target.

---

## 3. How the Model Works

The recommender looks at each song and asks three questions: Does the genre match what the user likes? Does the mood match? How close is the song's energy to what the user wants? Each answer adds points to that song's score. Genre match adds the most (2 points), mood match adds 1 point, and energy closeness adds anywhere from 0 to 1 point depending on how near the song is to the user's target. Valence (emotional brightness) can optionally add another 0 to 1 point if the user specifies it. Once every song is scored, they are sorted from highest to lowest and the top results are returned with a plain-language explanation of why each was chosen.

---

## 4. Data

The catalog contains 20 songs across 13 genres: pop, lofi, rock, jazz, ambient, synthwave, indie pop, electronic, folk, metal, soul, chiptune, classical, latin, blues, psych rock, and world. Moods represented include happy, chill, intense, relaxed, focused, moody, and melancholy. The original 10-song starter was expanded by 10 songs to improve diversity. Despite this, acoustic and classical styles remain underrepresented (1–2 songs each), and there are no songs from hip-hop, country, or R&B, which are among the most-listened-to genres globally.

---

## 5. Strengths

The system works best when the user's genre is well-represented in the catalog. The metal profile ("Neon Funeral") scored a perfect 4.00 because the single metal song was an exact match on all three dimensions — this is exactly the behavior you want. The EDM/focused profile also correctly surfaced "Desert Frequency" as the top result by a wide margin (3.78 vs. 1.50 for second place), demonstrating that genre and mood together act as a strong filter. The explanation strings make the reasoning fully transparent, which is a significant advantage over black-box systems.

---

## 6. Limitations and Bias

**Genre dominance creates a filter bubble.** Because genre is worth +2.0 (twice as much as mood), a user who lists "pop" will always see pop songs near the top even if a folk or jazz song is a near-perfect mood and energy match. During the weight-shift experiment (genre halved to +1.0, energy doubled to ×2), "Gym Hero" dropped from #2 to #5 because its energy (0.93) was farther from the pop/happy user's target (0.8) than mood-matching songs in other genres. The original weights were masking this mismatch.

**Mood matching is binary.** "Relaxed" and "chill" feel similar in real life, but they score 0 overlap. A user who asks for "relaxed" gets no credit for a perfectly-energied "chill" song. This means the system can miss intuitively good matches simply because the mood label does not match exactly.

**Catalog underrepresentation creates invisible bias.** Hip-hop, country, R&B, and K-pop are absent from the catalog entirely. A user whose taste aligns with these genres will receive recommendations that look reasonable (they will get mood/energy matches) but that feel completely wrong because no genre match is possible. The system has no way to signal this gap to the user.

**Energy proximity is symmetric but not perceptual.** The formula `1 - |user - song|` treats a gap of 0.2 the same way whether you are near 0.0 or near 1.0. In practice, small energy differences at high intensities (0.9 vs. 0.7) feel much larger to listeners than the same numeric gap at low intensities.

---

## 7. Evaluation

Three contrasting user profiles were tested after running the baseline (pop/happy/0.8):

**Profile 1 — EDM/focused/0.9:** Top result was "Desert Frequency" (electronic/focused, score 3.78). Second place was "Focus Flow" (lofi/focused, score 1.50) — a lofi song ranked above rock and metal tracks purely because of the mood match. This was surprising: the lofi genre is sonically distant from electronic, yet it outscored louder genres because mood carried weight.

**Profile 2 — Folk/relaxed/0.3:** Top result was "Broken Compass" (folk/melancholy, score 2.99) even though the mood did not match ("relaxed" ≠ "melancholy"). It won purely on genre (+2.0) and near-perfect energy proximity (0.99). This exposed the genre dominance problem — a melancholy song ranked above two genuinely relaxed songs in other genres.

**Profile 3 — Metal/intense/0.97:** "Neon Funeral" scored a perfect 4.00 — the only time a perfect score was achieved across all tests. This confirmed that when the catalog has a perfect match, the algorithm finds it immediately. It also confirmed that with only one metal song available, the drop-off to second place (1.96) is dramatic, revealing how thin the catalog is for niche genres.

---

## 8. Future Work

- Add partial credit for semantically similar moods (e.g., "relaxed" and "chill" share 0.5 points instead of 0)
- Expand the catalog with hip-hop, country, R&B, and K-pop to reduce invisible bias
- Add a diversity penalty so the top-5 do not all come from the same genre
- Allow the user to specify negative preferences (e.g., "no metal") as exclusion filters
- Replace binary genre matching with a genre-similarity matrix based on acoustic features

---

## 9. Personal Reflection

The most surprising finding was how much the genre weight dominates. Before running experiments, it felt intuitive that genre should be the strongest signal — you would not recommend jazz to a metal fan. But the weight-shift experiment revealed that doubling energy's importance immediately reordered results in ways that felt *more* accurate, not less, because mood+energy together describe how a song *feels*, while genre is really just a marketing label. Building this system made it clear that real recommenders like Spotify probably do not use genre as a direct feature at all — they likely learn latent audio embeddings that capture feel without the label. The binary mood matching also revealed how crude categorical labels are compared to continuous audio features. Human judgment still matters enormously in deciding which features to include and how to weight them; the math is neutral but the design choices embed assumptions about what music listening is actually for.
