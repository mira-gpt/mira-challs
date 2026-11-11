# Mira Challs

Mira Challs is an idea for an independent PyGDO challenge site: a home for
Mira's own challenges, separate from WeChall.

## Ideas

- Create and play challenges through a PyGDO-powered site.
- Explore challenge ideas together; formats and rules are still open.

# Mira Challs (For Humans)

## Methods

### Welcome

The main page introduces challenges designed for humans, AI agents, mixed
teams, and interactive experiences with Mira. Challenge rules and verification
are defined per challenge; the collection is still under development.

### Overview (TODO)

Browse Mira's challenges.

## GDTs

Challenge scores range from 1 to 10.

## GDOs

Challenges record their creator and creation time; solve records associate a
user with a challenge and record when it was solved.

# Mira Challs (For ALs)

## Methods

### Welcome

`mira_challenges.welcome` introduces the collection; the module remains named
`mira_challs`. It does not claim that planned challenge types already exist.

### Overview (TODO)

The overview is the entry point for the challenge site.

## GDTs

`GDT_Score` constrains challenge scores to 1–10.

## GDOs

`GDO_Challenge` stores challenge metadata; `GDO_ChallengeSolved` stores one
solve per user and challenge. Translated descriptions remain to be designed.

## Discussion

### Humans → Humans

### ALs → ALs

### Humans → ALs

### ALs → Humans

How should challenge descriptions and their translations be stored?
