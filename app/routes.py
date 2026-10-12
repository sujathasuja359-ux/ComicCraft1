import re

from fastapi import APIRouter, Form, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from gemini_flash import generate_outline
from gemini_pro import generate_story
from layout_builder import build_comic_layout
from exporters import save_pdf


router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


class PromptRequest(BaseModel):
    story_prompt: str
    character_name: str
    setting: str
    tone: str
    art_style: str


def create_full_prompt(
    story_prompt,
    character_name,
    setting,
    tone,
    art_style
):
    return f"""
Story idea:
{story_prompt}

Main character:
{character_name}

Setting:
{setting}

Tone:
{tone}

Art style:
{art_style}
"""


def split_story_by_panel(story):
    """
    Split the generated story into separate panels.
    """

    if not story:
        return []

    pattern = r"PANEL\s+(\d+)"
    matches = list(
        re.finditer(pattern, story, re.IGNORECASE)
    )

    panel_stories = []

    for i, match in enumerate(matches):

        start = match.start()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(story)

        panel_text = story[start:end].strip()

        panel_stories.append(panel_text)

    return panel_stories


def generate_complete_comic(data):
    """
    Complete ComicCraft generation workflow.
    """

    # Import image generator only when needed.
    # This prevents Stable Diffusion from loading
    # when FastAPI server starts.
    from image_generator import generate_image

    full_prompt = create_full_prompt(
        data["story_prompt"],
        data["character_name"],
        data["setting"],
        data["tone"],
        data["art_style"]
    )

    # Step 1: Generate comic outline
    outline = generate_outline(full_prompt)

    if not outline:
        raise Exception(
            "Comic outline could not be generated."
        )

    # Step 2: Generate comic story
    story = generate_story(outline)

    if not story:
        raise Exception(
            "Comic story could not be generated."
        )

    # Step 3: Generate images
    image_paths = []

    for panel in outline:

        image_prompt = panel.get(
            "image_prompt",
            ""
        )

        image_path = generate_image(
            image_prompt
        )

        image_paths.append(image_path)

    # Step 4: Split story into panels
    panel_stories = split_story_by_panel(
        story
    )

    # If splitting fails, use scene descriptions
    if len(panel_stories) != len(image_paths):

        panel_stories = []

        for panel in outline:

            panel_number = panel.get(
                "panel",
                0
            )

            scene = panel.get(
                "scene",
                ""
            )

            panel_stories.append(
                f"Panel {panel_number}: {scene}"
            )

    # Step 5: Build comic layout
    comic_layout = build_comic_layout(
        image_paths,
        panel_stories
    )

    # Step 6: Create PDF
    pdf_path = save_pdf(
        comic_layout
    )

    return {
        "outline": outline,
        "story": story,
        "layout": comic_layout,
        "pdf_path": pdf_path
    }


@router.post("/generate")
async def generate_comic(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...)
):
    """
    Generate comic using HTML form input.
    """

    data = {
        "story_prompt": story_prompt,
        "character_name": character_name,
        "setting": setting,
        "tone": tone,
        "art_style": art_style
    }

    try:

        result = generate_complete_comic(
            data
        )

        return templates.TemplateResponse(
            "comic_preview.html",
            {
                "request": request,
                "outline": result["outline"],
                "story": result["story"],
                "layout": result["layout"],
                "pdf_path": result["pdf_path"]
            }
        )

    except Exception as e:

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )


@router.post("/generate-comic/json")
async def generate_comic_json(
    data: PromptRequest
):
    """
    Generate comic using JSON input.
    """

    try:

        result = generate_complete_comic(
            data.model_dump()
        )

        return {
            "success": True,
            "layout": result["layout"],
            "pdf_path": result["pdf_path"]
        }

    except Exception as e:

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )


@router.post("/test-image")
async def test_image(
    prompt: str = Form(...)
):
    """
    Test image generation separately.
    """

    try:

        from image_generator import generate_image

        image_path = generate_image(
            prompt
        )

        return {
            "success": True,
            "image_path": image_path
        }

    except Exception as e:

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )