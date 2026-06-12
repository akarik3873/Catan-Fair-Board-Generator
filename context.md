# Catan Fair Board Generator — Project Context

A small web app that generates "fair" Settlers of Catan boards. A Python script
(`board.py`) holds the generation algorithm; everything documented here is the
layer around it — the web server, the browser UI, and the supporting files.

## How to run

```bash
python3 server.py
# then open http://localhost:8000
```

No dependencies — both the server and the generator use only the Python
standard library, and the frontend is a single self-contained HTML file
(its only external fetch is two Google Fonts).

## Project layout

| Path | What it is |
|---|---|
| `board.py` | The board-generation algorithm (backend script — not covered here). Exposes a `Board` class; `Board().board_generator()` fills 19 tiles with resource types, dice numbers, and ports. |
| `server.py` | Tiny stdlib HTTP server that wraps `board.py` and serves the frontend. |
| `index.html` | The whole frontend: page, styles, and SVG board renderer in one file. |
| `catanGenerator2.py` | An older, partial draft of the tile/side classes. Not used by anything. |
| `Past Iterations/` | Earlier attempts (`Board.py`, `Board2.py`, `Board3.py`, `Node_Class.py`, random-board variants, a GUI folder, `main.py`). Historical reference only. |
| `catan-board.png` | A saved screenshot of a generated board. |
| `.playwright-mcp/` | Artifacts from browser-automation testing sessions. Not part of the app. |
| `README.md` | Currently just a placeholder line. |

## server.py — the web server

`server.py` is a ~70-line `http.server.ThreadingHTTPServer` on port **8000**
with two routes:

- **`GET /` (or `/index.html`)** — serves `index.html` from disk.
- **`GET /generate`** — creates a fresh `board.Board()`, runs
  `board_generator()`, and returns the result as JSON.

Implementation notes:

- `board.py` prints a lot of debug output and even runs a full generation at
  import time. The server wraps both the import and each generation in
  `contextlib.redirect_stdout(io.StringIO())` to swallow that output.
- Responses are sent with `Cache-Control: no-store` so the browser never
  caches a board, and request logging is disabled to keep the console clean.

### The `/generate` JSON shape

```json
{
  "tiles": [ { "id": 0, "type": "Wheat", "number": 9 }, ... 19 total ],
  "ports": [ { "tile": 6, "side": 2, "resource": "Wood" }, ... ]
}
```

- **tiles** — all 19 hexes. `id` follows the generator's layout convention:
  `18` is the center tile, `0–5` are the inner ring, `6–17` are the outer
  (coastal) ring. The desert tile has `number: 7` and gets no number token.
- **ports** — taken from the outward-facing sides (sides 2, 3, 4) of the
  coastal tiles, where the generator stores port resources as plain strings.
  `"Water"` entries are open sea; two adjacent entries with the same resource
  form one two-dock 2:1 port. They are listed in coastal order so the
  frontend can pair adjacent docks.

## index.html — the frontend

A single file containing the markup, CSS, and ~180 lines of vanilla
JavaScript. No frameworks, no build step.

### Look and feel

Nautical "old sea chart" theme: deep-sea radial-gradient background, a
fractal-noise grain overlay for a printed-paper texture, parchment and gold
colors, and the Cinzel Decorative / Alegreya fonts. The favicon is an inline
SVG hexagon. Tiles pop in with a staggered scale animation; ports fade in
afterwards.

### Page structure

- A header with the title and the **"Forge a New Isle"** button.
- An SVG element (`viewBox="-330 -330 660 660"`) where the board is drawn.
- A legend strip mapping each resource color (plus the port marker).

### How rendering works

1. **`forge()`** — runs on page load and on every button click. Disables the
   button, fetches `/generate`, and hands the JSON to `drawBoard()`. On
   failure it alerts with a hint to start `server.py`.
2. **Coordinates** — `axialOf(id)` converts the generator's tile ids to axial
   hex coordinates: 18 → origin, 0–5 → the six unit directions, 6–17 → the
   outer ring (even ids are corners in line with inner tile `(id-6)/2`, odd
   ids sit on the edge between two corners). `toPixel()` converts axial to
   pixel coordinates with hex size `S = 52` (pointy-top layout).
3. **Tiles** — each hex is drawn as two stacked polygons (darker edge color
   under the fill color, giving a border) plus a subtle white inner stroke.
   Non-desert tiles get a parchment number token with the dice number
   (red and larger for 6/8, the high-probability "hot" numbers) and
   probability pips (`6 - |7 - number|` dots, matching the physical game).
4. **Ports** — consecutive same-resource entries in the `ports` array are
   paired into one port. For each dock, `waterDir(tile, side)` figures out
   which sea direction that side faces; a dock line is drawn from the hex
   edge out to sea, and a two-circle port marker (parchment ring around the
   resource color) is placed at the midpoint of the pair. Hovering shows a
   "`<Resource>` port (2:1)" tooltip via an SVG `<title>`.
5. **Colors** — the `RES` map defines fill/edge colors per resource
   (Wheat, Sheep, Wood, Brick, Stone, Desert) and also drives the legend.

## Data flow, end to end

```
browser click → GET /generate → server.py → board.Board().board_generator()
             ← JSON {tiles, ports} ←
drawBoard(): tile ids → axial coords → SVG hexes + number tokens + ports
```

## Known quirks

- The repo has both `board.py` (current) and references to `Board.py` in git
  status — on macOS's case-insensitive filesystem these are the same file,
  which can confuse git.
- `board.py` executes a generation at module import time (it instantiates and
  prints a board at the bottom of the file), which is why `server.py` has to
  silence stdout just to import it.
- The generator retries from scratch when it paints itself into a corner, so
  `/generate` latency varies — usually well under a second.
