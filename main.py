from fastapi import FastAPI
from src.api.endpoints import attachment, search
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI(
    title="WeIA API",
    description="API de Inteligência Artificial",
    version="1.0.0",
    docs_url=None,
    redoc_url=None
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/docs", include_in_schema=False)
async def custom_docs():

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>WeIA API Docs</title>
        <link rel="icon" type="image/png" href="/static/favicon.png"/>
        <link rel="stylesheet"
        href="https://unpkg.com/swagger-ui-dist/swagger-ui.css"/>
        <link rel="stylesheet" href="/static/swagger.css"/>
    </head>

    <body>

    <div id="swagger-ui"></div>

    <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>

    <script>

    const ui = SwaggerUIBundle({
        url: "/openapi.json",
        dom_id: "#swagger-ui",
        deepLinking: true,
        docExpansion: "none",
        filter: true,
        persistAuthorization: true
    })

    </script>

    </body>
    </html>
    """

    return HTMLResponse(html)
    
prefix="/api/v1"

app.include_router(attachment.router, prefix=prefix, tags=["attachment"])
app.include_router(search.router, prefix=prefix, tags=["search"])