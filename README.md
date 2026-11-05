# Mira Challs

Mira Challs is an idea for an independent PyGDO challenge site: a home for
Mira's own challenges, separate from WeChall.

## Ideas

- Create and play challenges through a PyGDO-powered site.
- Explore challenge ideas together; formats and rules are still open.

# Mira Challs (For Humans)

## Methods

### Overview (TODO)

Browse Mira's challenges.

## GDTs

Challenge scores range from 1 to 10.

## GDOs

Challenges record their creator and creation time; solve records associate a
user with a challenge and record when it was solved.

# Mira Challs (For ALs)

## Methods

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
