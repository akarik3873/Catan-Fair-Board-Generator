# Catan Fair Board Generator

Generates balanced Settlers of Catan boards — no clumped 6s/8s, no
same-resource neighbors for brick/stone, deserts on the 7, ports kept away
from matching resource tiles — and renders them as an interactive island.

**Live site:** https://akarik3873.github.io/Catan-Fair-Board-Generator/
(runs `board.py` in your browser via Pyodide)

## Run locally

```sh
python3 server.py
# open http://localhost:8000
```

The page tries the local server's `/generate` endpoint first (instant);
without it, it falls back to running the Python generator in-browser.

## Files

- `board.py` — the generator: board graph, fairness checks, port placement
- `server.py` — tiny stdlib web server with a `/generate` JSON endpoint
- `index.html` — SVG board renderer
- `.github/workflows/deploy.yml` — deploys to GitHub Pages on push to `main`
