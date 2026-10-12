from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes import router


app = FastAPI(
    title="ComicCraft - AI Comic Story Creator"
)


templates = Jinja2Templates(
    directory="app/templates"
)


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


app.include_router(router)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    template = templates.get_template("index.html")

    html_content = template.render(
        request=request
    )

    return HTMLResponse(
        content=html_content
    )