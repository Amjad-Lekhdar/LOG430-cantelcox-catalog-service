from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from app.modules.catalog.interfaces.api.router import router as catalog_router
from app.ui.catalog_admin import CATALOG_ADMIN_HTML

app = FastAPI(title="CanTelcoX Catalog Service API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1|10\.0\.2\.2|192\.168\.\d+\.\d+)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(catalog_router)


@app.get("/", response_class=HTMLResponse)
def catalog_admin_page() -> HTMLResponse:
    return HTMLResponse(CATALOG_ADMIN_HTML)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "catalog-service"}
