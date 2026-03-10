from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# novos controllers
from src.api.endpoints import (
    auth_controller,
    company_controller,
    user_controller,
    folder_controller,
    search_controller,
    attachment_controller,
    history_controller,
    file_controller,
    ftp_controller
)

app = FastAPI(
    title="WeIA API",
    description="API de Inteligência Artificial",
    version="1.0.0",
    docs_url=None,
    redoc_url=None
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

prefix = "/api/v1"

app.include_router(attachment_controller.router, prefix=prefix, tags=["attachment"])
app.include_router(search_controller.router, prefix=prefix, tags=["search"])
app.include_router(history_controller.router, prefix=prefix, tags=["history"])
app.include_router(auth_controller.router, prefix=prefix, tags=["auth"])
app.include_router(company_controller.router, prefix=prefix, tags=["companies"])
app.include_router(user_controller.router, prefix=prefix, tags=["users"])
app.include_router(folder_controller.router, prefix=prefix, tags=["folders"])
app.include_router(file_controller.router, prefix=prefix, tags=["files"])
app.include_router(ftp_controller.router, prefix=prefix, tags=["ftp"])