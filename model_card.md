# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Goal / Task

VibeFinder takes a user's taste profile — a preferred genre, mood, and energy level — and returns the top songs from a small catalog that best match those preferences. It does not learn from behavior over time. It scores every song once per query and ranks them.

---

## 3. Data Used

- **Catalog size:** 20 songs in `data/songs.csv`
- **Features per song:** genre, mood, energy (0–1), tempo_bpm, valence (0–1), danceability (0–1), acousticness (0–1)
- **Genres covered:** pop, lofi, rock, jazz, ambient, synthwave, indie pop, electronic, folk, metal, soul, chiptune, classical, latin, blues, psych rock, world
- **Moods covered:** happy, chill, intense, relaxed, focused, moody, melancholy
- **Limits:** Hip-hop, country, R&B, and K-pop are entirely absent. Most genres have only 1–2 songs, so catalog thinness is a major constraint. The data was hand-crafted for this simulation and does not reflect real listening patterns.

---

## 4. Algorithm Summary

For each song, the system adds up points based on how well it matches the user:

- **+2.0** if the song's genre exactly matches the user's preferred genre
- **+1.0** if the song's mood exactly matches the user's preferred mood
- **+0 to 1** based on how close the song's energy is to the user's target (closer = more points)
- **+0 to 1** based on valence closeness, if the user provides a valence target

The song with the highest total score is recommended first. Ties are broken by the order songs appear in the CSV. Each result comes with a plain-English explanation listing which features contributed points.

---

## 5. Observed Behavior / Biases

**Genre dominates too strongly.** Because a genre match is worth +2.0 and mood is only +1.0, a song with the right genre but wrong mood can outscore a song with the right mood but wrong genre. In testing, a melancholy folk song ranked #1 for a "folk/relaxed" user because the genre match outweighed the mood mismatch.

**Mood matching has no partial credit.** "Relaxed" and "chill" feel similar but score as completely different. A perfectly-energied chill song gets zero mood points for a relaxed-seeking user.

**Niche genres either win perfectly or fall off a cliff.** With only one metal song in the catalog, the metal profile got a perfect score for that song and then saw scores drop by more than half for second place. Users of underrepresented genres have almost no safety net.

**The energy formula does not match perception.** A 0.2 energy gap at low levels (0.1 vs. 0.3) feels different to a listener than the same gap at high levels (0.7 vs. 0.9), but the math treats them identically.

---

## 6. Evaluation Process

Four user profiles were tested by running `python src/main.py` with different `user_prefs` dictionaries:

| Profile | Genre | Mood | Energy | Top Result |
|---------|-------|------|--------|------------|
| Baseline | pop | happy | 0.8 | Sunrise City (3.98) |
| EDM/focused | electronic | focused | 0.9 | Desert Frequency (3.78) |
| Acoustic/relaxed | folk | relaxed | 0.3 | Broken Compass (2.99) |
| Metal/intense | metal | intense | 0.97 | Neon Funeral (4.00) |

A weight-shift experiment was also run: genre weight halved to +1.0 and energy weight doubled to ×2. This caused "Gym Hero" to drop from #2 to #5 for the baseline profile, revealing that the default weights were masking an energy mismatch with the genre match.

The most telling result was the acoustic/relaxed profile: the #1 song ("Broken Compass") had the wrong mood. It won purely on genre + energy, which suggests the weights favor genre correctness over emotional correctness.

---

## 7. Intended Use and Non-Intended Use

**Intended use:**
- A classroom simulation for learning how content-based recommenders work
- Exploring the effect of feature weights on ranking order
- A starting point for discussing fairness and bias in algorithmic systems

**Not intended for:**
- Real music listeners expecting personalized recommendations
- Any production or commercial deployment
- Making inferences about real artists or songs
- Replacing human curation or editorial taste

---

## 8. Ideas for Improvement

1. **Partial mood credit:** Build a mood-similarity table so "relaxed" and "chill" share 0.5 points instead of 0. This would reduce the harsh penalty for near-miss moods.
2. **Genre-frequency normalization:** Penalize genre matches for genres that dominate the catalog, so a pop match is worth less than a metal match (since metal is rarer and therefore more specific).
3. **Diversity enforcement:** After scoring, apply a rule that prevents more than 2 songs from the same genre in the top-5, pushing the system toward broader recommendations.

---

## 9. Personal Reflection

**Biggest learning moment:** The weight-shift experiment was the clearest lesson. Before running it, the +2.0 genre weight felt obviously correct — you would not recommend jazz to a metal fan. But once energy was doubled, the rankings changed in ways that felt *more* accurate, not less. That moment made it clear that the math does not enforce correctness; the designer's weight choices do. Every weight is a claim about what music listeners care about, and those claims can be wrong.

**How AI tools helped, and when I had to double-check:** AI tools were useful for scaffolding the CSV expansion and generating the initial scoring formula quickly. But I had to verify the output manually — for example, the weight-shift experiment showed that the generated weights produced a genre-dominant system that was masking mood mismatches. The AI wrote valid code but could not know whether the design was fair. That judgment required running the profiles and reading the results critically.

**What surprised me about simple algorithms "feeling" like recommendations:** The most surprising thing was how convincing the output looks even when it is wrong. When "Broken Compass" (melancholy folk) ranked #1 for a relaxed-seeking user, the explanation string said "genre match (+2.0); energy proximity (0.99)" — which sounds logical. Without knowing the mood should have been wrong, a real user might accept it. Simple algorithms can produce confident-looking explanations for flawed recommendations, and that is exactly what makes them risky in real products.

**What I would try next:** The single most useful next step would be replacing binary mood labels with a 2D mood space — valence on one axis, energy on the other — so moods like "chill" and "relaxed" are close in space rather than categorically different. This is closer to how audio ML models like Spotify's actually represent songs, and it would immediately improve the quality of recommendations for the harder edge cases this simulation revealed.
