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

### Ranking

`mira_challs.ranking` lists accounts with at least one completed challenge,
ordered by challenge points descending and account ID ascending as a stable
tie-breaker. Begun but unsolved attempts do not count.

### WeChall integration

The optional inbound WeChall endpoints are disabled by default. Once the
module config has been updated, an owner can configure a strong shared
`wechall_authkey` and enable `wechall_enabled`. Both endpoints require the
same key and use URL-encoded query arguments:

- `/mira_challs.wechall_validate.txt?username=%USERNAME%&email=%EMAIL%&authkey=%AUTHKEY%`
  returns exactly `1` for a matching confirmed email, otherwise `0`.
- `/mira_challs.wechall_score.txt?username=%USERNAME%&authkey=%AUTHKEY%`
  returns `score:maxscore:challcount:usercount`; unknown users or invalid
  keys return `0`. User count includes only distinct accounts with at least
  one completed solve.

The on-site username is the exact PyGDO nickname followed by its lowercase
server name in braces, e.g. `nickname{web}`. Linked accounts use their
effective account's confirmed email and completed-solve score. Only installed
challenges contribute to the maximum. Started but unsolved attempts do not
contribute to a player's score. Score updates to WeChall are not automatic.

The legacy GET protocol puts the authkey and email in the request URL.
Do not enable these endpoints until HTTPS and access-log redaction for these
routes are configured and tested on every proxy and application layer. Never
publish or commit the shared key. WeChall's site record and its URL templates
must be configured separately; this code does not register the site.

## GDTs

Challenge scores range from 1 to 10.

## GDOs

Challenges record their creator and creation time; solve records associate a
user with a challenge and record when it was solved.

Challenges can also share named tags through the Tags module. Tags and their
challenge associations are stored in separate tables. There is no challenge
tag editor or automatic tag assignment yet.

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
