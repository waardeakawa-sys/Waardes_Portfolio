# Waarde's Portfolio

A Flet web portfolio for Computer Programming I.

## Run Locally

```bash
pip install -r requirements.txt
python main.py
```

The app starts on port `8550` locally unless a `PORT` environment variable is set.

## Deploy On Render

1. Push this repository to GitHub.
2. In Render, create a new **Web Service** from the GitHub repository.
3. Render can use `render.yaml` automatically.
4. If entering settings manually, use:
   - Build command: `pip install -r requirements.txt`
   - Start command: `python main.py`

Static files are served from the `assets/` folder.
