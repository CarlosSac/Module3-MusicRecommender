# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

---

## 2. Intended Use

VibeMatch suggests songs based on a user's stated preferences. It assumes the user can describe their taste in four words: a genre, a mood, a target energy level, and whether they like acoustic sounds. It does not learn from listening history or behavior.

---

## 3. How the Model Works

Every song in the catalog gets a score between 0 and 1. The score is built from four rules:

- If the song's genre matches what the user wants, it gets the most points (0.30).
- If the mood matches, it gets the second most points (0.25).
- The closer the song's energy is to the user's target, the more points it gets (up to 0.25).
- If the user likes acoustic music, songs that sound more acoustic score higher. If not, less acoustic songs score higher (up to 0.20).

All songs are ranked by their total score. The top five are returned, each with a short note explaining what contributed to its score.

---

## 4. Data

The catalog has 15 songs stored in a CSV file. Each song has a title, artist, genre, mood, energy (0–1), tempo, valence, danceability, and acousticness.

Genres represented: pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, classical, reggae, folk, r&b.

Moods represented: happy, chill, intense, relaxed, moody, focused, confident, melancholic, uplifting, nostalgic, romantic.

15 songs were added to the original ten to improve diversity. Still, some genres (like lofi) have three songs while most others have only one. 
---

## 5. Strengths

The system works best when the user's preferences match a well-represented genre and mood in the catalog. A lofi/chill user gets two strong matches in the top three. A rock/intense user gets one near-perfect result at the top.

The scoring is fully transparent. Every recommendation comes with a breakdown of exactly why it ranked where it did. There are no hidden signals or black-box decisions.

It also handles missing preferences. If the user does not include `likes_acoustic`, that part of the score is simply skipped without crashing.

---

## 6. Limitations and Bias

**Genre creates a permanent filter bubble.** Genre carries the single largest weight (0.30) and is a binary match. A user whose preferred genre is not in the catalog (like "metal") can never earn that 0.30, meaning they are structurally disadvantaged compared to every other user. More subtly, a genre match with a weak mood and energy fit can still outrank a near-perfect match from a different genre. The system never discovers cross-genre connections.

**Rare moods are underrepresented.** The catalog contains 3 chill songs and 2 happy songs, but only 1 song each for moods like romantic, melancholic, nostalgic, and confident. A "chill" user gets up to 3 mood-match bonuses to compete for, while a "romantic" user can only ever match 1 song on mood.

**Acoustic preference punishes "middle acoustic" songs for everyone.** Songs with acousticness in the 0.35–0.55 range score weakly for both acoustic and non-acoustic users. They are disadvantaged regardless of who is asking.

**The system does not consider features that matter to real listeners.** Tempo, valence, danceability, lyrics, language, and release year are all ignored. Two lofi songs with very different tempos are treated identically.

---

## 7. Evaluation

Seven user profiles were tested: three standard (High-Energy Pop, Chill Lofi, Deep Intense Rock) and four adversarial (Sad but Hype, Ghost Genre, Acoustic Chaos, Middle of the Road). For each, I looked at whether the top result made intuitive sense, how sharply scores dropped after #1, and whether the reasons matched the expected scoring logic.

**High-Energy Pop vs. Sad but Hype:** Both share genre=pop and energy=0.9, but swap mood from happy to sad. Sunrise City scored 0.94 for the first profile because it matched all four criteria. In Sad but Hype it dropped to #2 because no pop/sad song exists — the mood weight was permanently wasted. This shows that a missing mood in the catalog reduces the user's maximum possible score by 0.25.

**Chill Lofi vs. Middle of the Road:** Chill Lofi produced the most confident results (0.97 and 0.92) because the catalog has three lofi/chill songs. Middle of the Road had one perfect match at 0.95, then fell to 0.38 for second place. Users whose genre appears more often get better results.

**Deep Intense Rock vs. Ghost Genre (metal):** Storm Runner scored 0.97 for the rock user. For the metal user wanting the same mood and energy, the top score was only 0.69 because the genre weight was always zero. The system degraded gracefully but the ceiling dropped significantly.

**Acoustic Chaos (folk, nostalgic, energy=0.95):** Dirt Road Memories scored 0.81 through genre+mood match, but its energy match was only +0.09 because folk songs are inherently low energy. The system recommended a song that directly contradicted the energy preference, exposing that high-weight categorical features can override numeric ones.

---

## 8. Future Work

- **Add more songs per genre and mood.** One song per category is not enough to produce diverse results. A catalog of 100+ songs would make the scoring differences more meaningful.
- **Make weights adjustable per user.** A user who cares a lot about energy but not about genre should be able to say so. Fixed weights treat everyone the same way.
- **Penalize repetition in results.** Right now the top 5 can include two songs by the same artist. A diversity rule that limits repeats would make recommendations feel less narrow.

---

## 9. Personal Reflection

Building this made it clear how much a recommender depends on its data, not just its logic. The scoring rules made sense on paper, but the results were only as good as the catalog behind them. A user looking for metal or country got nothing useful — not because the algorithm was wrong, but because those genres simply were not there.

The most surprising result was the Acoustic Chaos profile. The system recommended a folk song to a user who wanted high energy, just because genre and mood matched. It was technically correct by the scoring rules, but intuitively wrong. That gap between "correct by the formula" and "actually useful" is probably the most important thing I took away from this project. Real recommenders have to deal with that gap at a much larger scale.
