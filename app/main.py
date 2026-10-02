"""FastAPI entrypoint. T0: health check only."""

from fastapi import FastAPI

app = FastAPI(title="Ruko Zara")


@app.get("/healthz")
def healthz() -> dict[str, bool]:
    return {"ok": True}
