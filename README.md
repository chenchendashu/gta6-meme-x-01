# gta6-meme-x-01 — "Covering Your Shift"

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/chenchendashu/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/chenchendashu/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

An entry for make.fun's **Post a GTA 6 meme on X** bounty, by @chenchendashu.

## The meme

GTA 6 launched on Thursday 19 November 2026, and half the planet called
in sick for it. This poster's boss thinks he's in bed — he's in Leonida.
Sitting at his office desk, headset on, covering his shift (and earning
bounties on make.fun at the same time): his AI agent, the make.fun ghost.

> **CALLED IN SICK FOR GTA 6 LAUNCH DAY.**
> Ghost, in a speech bubble: *"GO PLAY. I GOT YOUR SHIFT."*
> Caption: *my AI agent also earns on make.fun while it covers for me*

The picture (`meme.png`) is drawn with Python PIL in `make_meme.py`:
flat shapes for the office, desk, monitor, keyboard and coffee mug, and
the official make.fun ghost (from the press kit,
`assets/mark-1024.png`) cut out of its magenta disc and seated at the
desk wearing a headset, its monitor showing a make.fun bounty chart
going up. It stays legible shrunk to 480×480, ghost and all.

## The post

The exact text to post on X, with the picture attached, is in
[POSTING.md](POSTING.md). Once posted, the post's address goes into
`POST.json` in place of the placeholder.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

That copies `POST.json` to `out/POST.json`, which is all the house asks
the program to do — the entry itself is the post on X.
