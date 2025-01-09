import os

import uvicorn

UVICORN_HOST = os.getenv("UVICORN_HOST", "0.0.0.0")  # noqa: S104
UVICORN_PORT = int(os.getenv("UVICORN_PORT", "8000"))

if __name__ == "__main__":
    uvicorn.run("app:app", host=UVICORN_HOST, port=UVICORN_PORT, reload=True, reload_dirs=["/app"])
