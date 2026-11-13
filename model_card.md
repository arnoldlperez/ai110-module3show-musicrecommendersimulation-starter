# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

---

## 2. Intended Use  

**Goal:** VibeMatch suggests the top five songs from a small catalog that best match a listener's taste. The listener states a favorite genre, a favorite mood, how energetic they want the music to be, and optionally how happy it should sound and whether they like acoustic songs. Each suggestion comes with the reasons it was picked.

**Intended use:** This is a classroom project for learning how a content-based recommender turns data into suggestions. It assumes the listener knows what they want and can describe it with one genre and one mood. It is meant for exploring how scoring choices change the results.

**Not intended for:** It should not be used to recommend music to real users. It only knows 19 made up songs, it does not learn from what people actually play or skip, and its labels reflect one person's reading of each song. It should also not be used to judge or sort people by their taste.

---

## 3. How the Model Works  

VibeMatch works like a judge that gives each song points for what it has in common with you. A song gets 2 points if its genre matches yours and 1 point if its mood matches yours. It then gets up to 1.5 points for how close its energy is to the energy you want. A song that is right on target gets the full amount, and one that is far off gets close to nothing. If you give a happiness target, it adds up to 1 more point the same way. If you say whether you like acoustic music, it adds up to half a point for songs that fit. The best possible score is 6 points.

After every song has a score, VibeMatch sorts them from highest to lowest and shows you the top five. If two songs tie, the one listed first in the catalog wins. Each song also shows a list of the points it earned, so you can see exactly why it ranked where it did.

The starter code just returned the first few songs in the file. I added the scoring, the sorting, the happiness and acoustic checks, and the list of reasons.

---

## 4. Data  

The catalog has 19 songs. The starter came with 10, and I added 9 more to cover genres and moods that were missing. There are now 16 genres, including pop, lofi, rock, metal, classical, hip hop, r&b, edm, reggae, folk, and country. There are 14 moods, such as happy, chill, intense, sad, angry, romantic, and nostalgic.

Each song has a genre, a mood, and five number features, which are energy, tempo, valence, danceability, and acousticness. VibeMatch only scores energy, valence, and acousticness. Tempo and danceability rise and fall with energy in this catalog, so scoring them would count the same thing twice.

The data has some clear limits. Most genres only have one song, and only 3 songs sit in the middle of the energy range. The numbers for the songs I added were picked by hand, not measured from real audio. The data also leaves out a lot of what makes up musical taste, like lyrics, language, the era a song is from, and whether it has vocals.

---

## 5. Strengths  

VibeMatch works best for listeners with a clear and common taste. The Chill Lofi, High-Energy Pop, and Deep Intense Rock profiles all got the song I would have picked first at the top of their lists. For Chill Lofi, the whole top five matched my own sense of what fits that vibe.

The valence check also does its job past the genre and mood labels. The pop and rock listeners both want high energy, but the pop list fills in with happier songs and the rock list fills in with darker ones.

The explanations are another strength. Every song shows the points it earned, and they always add up to its score. This made it easy to see why a song like Gym Hero ranked where it did.

---

## 6. Limitations and Bias 

The biggest weakness I found is that the system leans heavily on exact genre labels, which creates a filter bubble that hits some listeners harder than others. A genre match is worth 2.0 points, but 14 of the 16 genres in the catalog only have a single song, so a rock fan gets one strong match and then drops straight from a score of 5.85 to 3.56 for everything after it. A lofi fan, as opposed to that, gets three lofi songs at the top since lofi happens to be the best covered genre in the data. The exact match also means close genres get no credit at all, which is why Gym Hero, a pop workout song, ranked above the happy indie pop song Rooftop Lights for a happy pop listener. In my weight shift experiment, halving genre fixed that ordering, but it let energy take over and pushed a cheerful EDM song into the rock list, so the bias moved somewhere else instead of going away.

I also found a few smaller issues. The matching is case sensitive, so a listener who types "Pop" instead of "pop" loses every genre and mood point. Listeners who want medium energy are served worse, as only 3 songs fall in the middle of the energy range. An energy target above 1.0 is not rejected, and it can give songs negative points.

---

## 7. Evaluation  

I tested eight profiles in total. The first was the starter pop and happy profile from main.py, followed by three listeners I expected to get very different results, which were High-Energy Pop, Chill Lofi, and Deep Intense Rock. I then added four edge case profiles meant to trick the scoring, which were a listener who wants sad folk music at gym level energy, the High-Energy Pop profile typed with capital letters, a genre and mood that do not exist in the catalog, and an energy target of 1.5 that is outside the 0 to 1 scale. For each one I looked at whether the top song made sense, whether the rest of the top five fit the same vibe, and whether the reasons printed under each song actually added up to its score. I also ran the two starter tests with pytest, and both passed.

For my own check I used the Chill Lofi profile, and the results felt right to me. Library Rain and Midnight Coding came out on top, followed by the lofi song Focus Flow and then the ambient and jazz songs, which is close to how I would order them myself. Library Rain only beat Midnight Coding by 0.06 points, and it won by being a bit more acoustic and closer on valence even though Midnight Coding was closer on energy.

The biggest surprise was how often Gym Hero showed up. It appeared in five of the eight lists, and it was second for both the High-Energy Pop and the Deep Intense Rock listeners, two people with very different taste. The capitalized profile also surprised me, as typing "Pop" instead of "pop" was enough to wipe out every genre and mood point and leave Sunrise City ahead of Gym Hero by only 0.01. I also did not expect the conflicting sad folk listener to get a calm folk song at the top, since its energy was 0.30 compared to the 0.90 they asked for.

### Profile comparisons

**High-Energy Pop vs. Chill Lofi:** The pop listener gets loud, upbeat, non-acoustic songs like Sunrise City and Pulse Theory, while the lofi listener gets quiet acoustic songs like Library Rain and Coffee Shop Stories. None of the songs overlap, which makes sense as the two profiles disagree on genre, mood, energy, and acoustic preference all at once.

**Chill Lofi vs. Deep Intense Rock:** These two are close to opposites. The rock listener's list is all high energy songs like Storm Runner and Iron Verdict, and the lofi listener's list is all low energy songs. Iron Verdict, which is third for rock, is the very last song for the lofi profile. The lofi list stays inside its genre for the top three as opposed to the rock list, which falls off after one song because the catalog only has one rock song.

**High-Energy Pop vs. Deep Intense Rock:** Both lists have Gym Hero in second place since both listeners want high energy, but it gets there for different reasons. The pop fan gives it genre points and the rock fan gives it mood points for being intense. Past that, the pop list picks happier songs like Pulse Theory, while the rock list picks darker ones like Neon Heartbreak and Night Drive Loop, which shows the valence target doing its job.

**Default starter vs. High-Energy Pop:** These are almost the same listener, and the top three are identical. The main difference is that adding a valence target and a non-acoustic preference raised every score and swapped Neon Heartbreak, a sad song, for Pulse Theory, a happy one, in fourth place. That makes sense as the starter profile had no way to ask for happy sounding songs beyond the mood label.

**High-Energy Pop vs. Capitalized Pop / Happy:** The only change is capital letters, but the capitalized profile lost all of its genre and mood points. Its top five turned into a near tie between 2.65 and 2.83, and Rooftop Lights dropped from third to fourth. This should not happen in a real app, and it shows the matching is case sensitive.

**Chill Lofi vs. Unknown k-pop / dreamy:** When nothing in the profile matches a label in the catalog, the scores bunch up between 2.15 and 2.38 and the order comes down to small differences in energy and valence. The lofi profile, as opposed to that, has about a three point spread between its first and fifth song. This shows that the labels are doing most of the sorting work in this system.

**Deep Intense Rock vs. Conflicting high-energy sad folk:** Both want energy around 0.90, but the folk listener's top song is the low energy Empty Platform because its genre and mood matches are worth 3 points, which outweighs the 0.90 energy points it loses. The rest of the folk list looks a lot like the rock list, with Iron Verdict, Storm Runner, and Night Drive Loop, as once the one folk song is used up, energy and valence take over.

**Out of range energy 1.5:** I compared this one to what an EDM listener should get. Pulse Theory is still first because of its genre and mood matches, but every song's energy points shrink, and songs with very low energy like Winter Sonata No. 2 actually get negative points. The input should be limited to the 0 to 1 range before any scoring happens.

### Why Gym Hero keeps showing up

Think of the recommender as a judge that gives a song points for each thing it has in common with you. Gym Hero is labeled pop, so any pop fan gives it two points right away, even if they wanted something happy and Gym Hero is more of a workout song. It is also one of the most energetic songs in the catalog, so anyone who wants high energy music gives it close to full energy points. Since there are only 19 songs and Gym Hero sits right where pop, intense, and high energy overlap, it ends up as the second best match for a lot of people even when it is not really what they asked for.

### Weight shift experiment

I tried halving the genre weight from 2.0 to 1.0 and doubling the energy weight from 1.5 to 3.0. For the starter pop listener this moved the happy indie pop song Rooftop Lights above Gym Hero, which I think is more accurate. However, it also pushed the cheerful EDM song Pulse Theory into the rock listener's top five just because its energy was high, and the sad folk listener's top pick changed to the high energy synthpop song Neon Heartbreak. Overall the change made some lists better and some worse, so I put the weights back to the original recipe.

### Test run output

Output of `python -m src.main`, one block per profile.

**Default (starter)**

```
User profile: favorite_genre=pop, favorite_mood=happy, target_energy=0.8
============================================================
Top recommendations
============================================================

1. Sunrise City by Neon Echo  [pop / happy]
   Score: 4.47
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.82 vs target 0.80 (+1.47)

2. Gym Hero by Max Pulse  [pop / intense]
   Score: 3.30
     - genre match (+2.0)
     - energy 0.93 vs target 0.80 (+1.30)

3. Rooftop Lights by Indigo Parade  [indie pop / happy]
   Score: 2.44
     - mood match (+1.0)
     - energy 0.76 vs target 0.80 (+1.44)

4. Neon Heartbreak by Static Bloom  [synthpop / sad]
   Score: 1.50
     - energy 0.80 vs target 0.80 (+1.50)

5. Concrete Crown by Block Theory  [hip hop / confident]
   Score: 1.47
     - energy 0.78 vs target 0.80 (+1.47)
```

**High-Energy Pop**

```
User profile: favorite_genre=pop, favorite_mood=happy, target_energy=0.85, target_valence=0.8, likes_acoustic=False
============================================================
Top recommendations
============================================================

1. Sunrise City by Neon Echo  [pop / happy]
   Score: 5.83
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.82 vs target 0.85 (+1.46)
     - valence 0.84 vs target 0.80 (+0.96)
     - non-acoustic fit (+0.41)

2. Gym Hero by Max Pulse  [pop / intense]
   Score: 4.82
     - genre match (+2.0)
     - energy 0.93 vs target 0.85 (+1.38)
     - valence 0.77 vs target 0.80 (+0.97)
     - non-acoustic fit (+0.47)

3. Rooftop Lights by Indigo Parade  [indie pop / happy]
   Score: 3.68
     - mood match (+1.0)
     - energy 0.76 vs target 0.85 (+1.36)
     - valence 0.81 vs target 0.80 (+0.99)
     - non-acoustic fit (+0.33)

4. Pulse Theory by Kilo Wave  [edm / euphoric]
   Score: 2.77
     - energy 0.95 vs target 0.85 (+1.35)
     - valence 0.86 vs target 0.80 (+0.94)
     - non-acoustic fit (+0.48)

5. Concrete Crown by Block Theory  [hip hop / confident]
   Score: 2.65
     - energy 0.78 vs target 0.85 (+1.40)
     - valence 0.62 vs target 0.80 (+0.82)
     - non-acoustic fit (+0.44)
```

**Chill Lofi**

```
User profile: favorite_genre=lofi, favorite_mood=chill, target_energy=0.4, target_valence=0.6, likes_acoustic=True
============================================================
Top recommendations
============================================================

1. Library Rain by Paper Lanterns  [lofi / chill]
   Score: 5.85
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.35 vs target 0.40 (+1.42)
     - valence 0.60 vs target 0.60 (+1.00)
     - acoustic fit (+0.43)

2. Midnight Coding by LoRoom  [lofi / chill]
   Score: 5.79
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.42 vs target 0.40 (+1.47)
     - valence 0.56 vs target 0.60 (+0.96)
     - acoustic fit (+0.35)

3. Focus Flow by LoRoom  [lofi / focused]
   Score: 4.88
     - genre match (+2.0)
     - energy 0.40 vs target 0.40 (+1.50)
     - valence 0.59 vs target 0.60 (+0.99)
     - acoustic fit (+0.39)

4. Spacewalk Thoughts by Orbit Bloom  [ambient / chill]
   Score: 3.73
     - mood match (+1.0)
     - energy 0.28 vs target 0.40 (+1.32)
     - valence 0.65 vs target 0.60 (+0.95)
     - acoustic fit (+0.46)

5. Coffee Shop Stories by Slow Stereo  [jazz / relaxed]
   Score: 2.79
     - energy 0.37 vs target 0.40 (+1.46)
     - valence 0.71 vs target 0.60 (+0.89)
     - acoustic fit (+0.45)
```

**Deep Intense Rock**

```
User profile: favorite_genre=rock, favorite_mood=intense, target_energy=0.9, target_valence=0.4, likes_acoustic=False
============================================================
Top recommendations
============================================================

1. Storm Runner by Voltline  [rock / intense]
   Score: 5.85
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.91 vs target 0.90 (+1.48)
     - valence 0.48 vs target 0.40 (+0.92)
     - non-acoustic fit (+0.45)

2. Gym Hero by Max Pulse  [pop / intense]
   Score: 3.56
     - mood match (+1.0)
     - energy 0.93 vs target 0.90 (+1.46)
     - valence 0.77 vs target 0.40 (+0.63)
     - non-acoustic fit (+0.47)

3. Iron Verdict by Grave Signal  [metal / angry]
   Score: 2.70
     - energy 0.97 vs target 0.90 (+1.40)
     - valence 0.22 vs target 0.40 (+0.82)
     - non-acoustic fit (+0.48)

4. Neon Heartbreak by Static Bloom  [synthpop / sad]
   Score: 2.67
     - energy 0.80 vs target 0.90 (+1.35)
     - valence 0.30 vs target 0.40 (+0.90)
     - non-acoustic fit (+0.42)

5. Night Drive Loop by Neon Echo  [synthwave / moody]
   Score: 2.58
     - energy 0.75 vs target 0.90 (+1.27)
     - valence 0.49 vs target 0.40 (+0.91)
     - non-acoustic fit (+0.39)
```

**Conflicting: high-energy sad folk**

```
User profile: favorite_genre=folk, favorite_mood=sad, target_energy=0.9, target_valence=0.2, likes_acoustic=True
============================================================
Top recommendations
============================================================

1. Empty Platform by June Harbor  [folk / sad]
   Score: 5.02
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.30 vs target 0.90 (+0.60)
     - valence 0.18 vs target 0.20 (+0.98)
     - acoustic fit (+0.44)

2. Neon Heartbreak by Static Bloom  [synthpop / sad]
   Score: 3.33
     - mood match (+1.0)
     - energy 0.80 vs target 0.90 (+1.35)
     - valence 0.30 vs target 0.20 (+0.90)
     - acoustic fit (+0.07)

3. Iron Verdict by Grave Signal  [metal / angry]
   Score: 2.39
     - energy 0.97 vs target 0.90 (+1.40)
     - valence 0.22 vs target 0.20 (+0.98)
     - acoustic fit (+0.01)

4. Storm Runner by Voltline  [rock / intense]
   Score: 2.25
     - energy 0.91 vs target 0.90 (+1.48)
     - valence 0.48 vs target 0.20 (+0.72)
     - acoustic fit (+0.05)

5. Night Drive Loop by Neon Echo  [synthwave / moody]
   Score: 2.09
     - energy 0.75 vs target 0.90 (+1.27)
     - valence 0.49 vs target 0.20 (+0.71)
     - acoustic fit (+0.11)
```

**Capitalized: Pop / Happy**

```
User profile: favorite_genre=Pop, favorite_mood=Happy, target_energy=0.85, target_valence=0.8, likes_acoustic=False
============================================================
Top recommendations
============================================================

1. Sunrise City by Neon Echo  [pop / happy]
   Score: 2.83
     - energy 0.82 vs target 0.85 (+1.46)
     - valence 0.84 vs target 0.80 (+0.96)
     - non-acoustic fit (+0.41)

2. Gym Hero by Max Pulse  [pop / intense]
   Score: 2.82
     - energy 0.93 vs target 0.85 (+1.38)
     - valence 0.77 vs target 0.80 (+0.97)
     - non-acoustic fit (+0.47)

3. Pulse Theory by Kilo Wave  [edm / euphoric]
   Score: 2.77
     - energy 0.95 vs target 0.85 (+1.35)
     - valence 0.86 vs target 0.80 (+0.94)
     - non-acoustic fit (+0.48)

4. Rooftop Lights by Indigo Parade  [indie pop / happy]
   Score: 2.68
     - energy 0.76 vs target 0.85 (+1.36)
     - valence 0.81 vs target 0.80 (+0.99)
     - non-acoustic fit (+0.33)

5. Concrete Crown by Block Theory  [hip hop / confident]
   Score: 2.65
     - energy 0.78 vs target 0.85 (+1.40)
     - valence 0.62 vs target 0.80 (+0.82)
     - non-acoustic fit (+0.44)
```

**Unknown genre and mood: k-pop / dreamy**

```
User profile: favorite_genre=k-pop, favorite_mood=dreamy, target_energy=0.6, target_valence=0.7
============================================================
Top recommendations
============================================================

1. Velvet Hours by Mara Jules  [r&b / romantic]
   Score: 2.38
     - energy 0.52 vs target 0.60 (+1.38)
     - valence 0.70 vs target 0.70 (+1.00)

2. Island Postcard by Sol Rivera  [reggae / uplifting]
   Score: 2.32
     - energy 0.60 vs target 0.60 (+1.50)
     - valence 0.88 vs target 0.70 (+0.82)

3. Dust Road Letters by Willow Creek  [country / nostalgic]
   Score: 2.31
     - energy 0.55 vs target 0.60 (+1.43)
     - valence 0.58 vs target 0.70 (+0.88)

4. Rooftop Lights by Indigo Parade  [indie pop / happy]
   Score: 2.15
     - energy 0.76 vs target 0.60 (+1.26)
     - valence 0.81 vs target 0.70 (+0.89)

5. Concrete Crown by Block Theory  [hip hop / confident]
   Score: 2.15
     - energy 0.78 vs target 0.60 (+1.23)
     - valence 0.62 vs target 0.70 (+0.92)
```

**Out of range: energy 1.5**

```
User profile: favorite_genre=edm, favorite_mood=euphoric, target_energy=1.5
============================================================
Top recommendations
============================================================

1. Pulse Theory by Kilo Wave  [edm / euphoric]
   Score: 3.67
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.95 vs target 1.50 (+0.67)

2. Iron Verdict by Grave Signal  [metal / angry]
   Score: 0.70
     - energy 0.97 vs target 1.50 (+0.70)

3. Gym Hero by Max Pulse  [pop / intense]
   Score: 0.65
     - energy 0.93 vs target 1.50 (+0.65)

4. Storm Runner by Voltline  [rock / intense]
   Score: 0.61
     - energy 0.91 vs target 1.50 (+0.61)

5. Sunrise City by Neon Echo  [pop / happy]
   Score: 0.48
     - energy 0.82 vs target 1.50 (+0.48)
```

---

## 8. Future Work  

1. **Give partial credit for related labels.** Metal should earn some points for a rock fan, and relaxed or focused songs should earn some points for a chill listener. This would soften the genre filter bubble without letting energy take over the way it did in my weight shift experiment.
2. **Clean up the input before scoring.** Lowercasing the genre and mood would fix the capitalization problem, and keeping energy and valence targets between 0 and 1 would stop songs from getting negative points.
3. **Add variety to the top five.** A simple rule like allowing only one song per artist, or making sure the list is not all one genre, would help listeners discover new music. Adding more songs to the catalog, especially in the genres with only one song and in the middle of the energy range, would help as well.

---

## 9. Personal Reflection  

My biggest learning moment was the weight shift experiment. I went in thinking that lowering the genre weight would fix the Gym Hero problem, and it did for the pop listener, but it also let energy take over and pushed a cheerful EDM song into the rock list. That showed me that changing a weight can move a bias somewhere else without actually removing it. I also learned how much of the work the genre and mood labels were doing. When none of the labels matched, every song in the top five landed within a few tenths of a point of each other, so the number features alone could barely tell songs apart.

Using an AI assistant helped a lot with the parts that would have been slow to do by hand. It ran the correlations on the dataset, scored every song for each profile, came up with the edge case profiles, and caught the capitalization and out of range energy problems by testing them. I worked through the project one step at a time and made the decisions myself, like the weights, the main profile, and whether to keep the experiment. I still needed to double check it at times. It told me the max score would stay at 6.0 during the weight shift when it was actually 6.5, it first said Gym Hero showed up in four lists when it was five, and some of the correlation numbers it wrote in the README went out of date once I added more songs. None of these were big issues, but they showed me that its numbers needed to be checked against the actual output before going into my write-up.

What surprised me most was how real the results felt for such a simple set of rules. The scoring is just a few additions, yet the Chill Lofi list matched what I would have picked myself, and having the reasons printed under each song made it feel like the app understood my taste. In hindsight that is also what makes it a bit misleading, as Gym Hero looked like a reasonable pick for a happy pop fan until I looked at the points and saw it was mostly getting there on its genre label.

If I kept working on this, I would first give partial credit for related genres and moods so a rock fan gets some points for metal. After that I would like to try adding listening behavior, like plays and skips from several made up users, so I can compare a content based approach with collaborative filtering and see whether mixing the two helps with the filter bubble.
