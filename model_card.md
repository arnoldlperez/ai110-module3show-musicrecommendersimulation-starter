# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

The biggest weakness I found is that the system leans heavily on exact genre labels, which creates a filter bubble that hits some listeners harder than others. A genre match is worth 2.0 points, but 14 of the 16 genres in the catalog only have a single song, so a rock fan gets one strong match and then drops straight from a score of 5.85 to 3.56 for everything after it. A lofi fan, as opposed to that, gets three lofi songs at the top since lofi happens to be the best covered genre in the data. The exact match also means close genres get no credit at all, which is why Gym Hero, a pop workout song, ranked above the happy indie pop song Rooftop Lights for a happy pop listener. In my weight shift experiment, halving genre fixed that ordering, but it let energy take over and pushed a cheerful EDM song into the rock list, so the bias moved somewhere else instead of going away.

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

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
