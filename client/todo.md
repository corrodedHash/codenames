# Views

## Room Create

- Select words
  - Textbox with 25 lines
  - Either input manually, or select from wordlists to generate
- Randomize colors
- Select offline
- Pressing start
  - Moves to `Room Join`
  - If offline:
    - Store words and colors in store
    - Mark as offline in store
  - If online:
    - Store words and colors in store
    - Send words and colors through api

## Room List

- Share button
  - If offline:
    - Share as admin with colors, or
    - share as spectator with no colors
  - If online:
    - Leader can share as leader/revealer/spectator
    - Revealer can share as revealer/spectator
- Edit button:
  - As owner, can change words and colors of existing room

## Room Join

- Select Leader/Revealer/Spectator
  - Offer options depending on permissions

# Ideas

- Make rooms shareable
  - QR codes with URLs
  - Offline rooms have entire wordlist and colors in URL
  - Otherwise sessionkey with possible permission token
  - Moves to `Room Join` view
