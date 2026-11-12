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

### Challenge

Visit `mira_challs.challenge.named.BJ.html` to open the Blackjack challenge.
Earn at least one million Blackjack credits, leave the table for a signed token,
and submit it while logged in. A successful answer records the solve once.
The token is a bearer credential: anyone possessing it can redeem it, as in
the GWF3 draft; keep it private. Invalid or unconfigured tokens fail closed.
When requested from a chat channel, the Blackjack token is returned privately.
Blackjack and BJ share a BJ-specific key, stored outside the web root at
`.config/pygdo/secret_bj_token` in the installation owner's home. Override
the path with `PYGDO_BJ_SECRET_PATH`; on separate hosts provision the same
private 64-hex-character key securely on each. This shared core token protocol avoids a module dependency in either
direction. Existing unrelated secrets are not used.

### Install challenges

`mira_challs.install` lists uninstalled challenge folders for owners.
Each loadable challenge has its own Install link; incomplete folders are
shown without one. The link opens a confirmation form. Installation uses a
CSRF-protected POST and rechecks the challenge before inserting it, without
overwriting an existing challenge.

NotAgain requires its private UTF-8 source text at
`challs/NotAgain/secret_plaintext`; this file is deliberately not tracked.
Installation stores a bcrypt hash, not the plaintext or answer. Back up the
source securely: changing it later changes the puzzle without updating the
installed answer.

Errection similarly requires the local files `challs/Errection/secret_message`
and `secret_plaintext`. The former is displayed to players; the latter is the
corrected message used to create the installed answer hash. Keep them in sync.

APPLY is reviewed manually. After reviewing a submission, an administrator can
use `mira_challs.apply_approve` to mark the installed challenge solved for a
selected user. The challenge page links to the approval form for admins only.

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
