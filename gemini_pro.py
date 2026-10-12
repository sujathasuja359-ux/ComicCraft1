import os
from dotenv import load_dotenv
from google import genai

# Load API key from .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("ERROR: GEMINI_API_KEY not found in .env file.")
    exit()

# Create Gemini client
client = genai.Client(api_key=API_KEY)


def generate_story(panel_outline):
    """
    Generate comic narration and character dialogue
    from the panel outline.
    """

    prompt = f"""
You are a comic story writer.

Convert the following 5-panel comic outline into a complete,
simple and engaging comic story.

For every panel, provide:

Panel number
Narration
Character dialogue

Make the story flow naturally from Panel 1 to Panel 5.

Panel Outline:
{panel_outline}

Return the result in this format:

PANEL 1
Narration: ...
Dialogue:
Character: "..."

PANEL 2
Narration: ...
Dialogue:
Character: "..."

PANEL 3
Narration: ...
Dialogue:
Character: "..."

PANEL 4
Narration: ...
Dialogue:
Character: "..."

PANEL 5
Narration: ...
Dialogue:
Character: "..."
"""

    try:
        print("Generating comic story...")

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        story = response.text.strip()

        return story

    except Exception as e:
        

        print("\nError while generating comic story:")
        print(e)

        return None


# Test the function
if __name__ == "__main__":

    sample_outline = [
        {
            "panel": 1,
            "title": "The Lost Robot",
            "scene": "A young girl finds a small robot alone in her neighborhood.",
            "image_prompt": "A young girl discovering a cute small robot on a neighborhood street."
        },
        {
            "panel": 2,
            "title": "Looking for the Owner",
            "scene": "The girl decides to help the robot find its owner.",
            "image_prompt": "A young girl and a cute robot searching through a neighborhood."
        },
        {
            "panel": 3,
            "title": "A Clue",
            "scene": "They find a clue that may lead to the robot's owner.",
            "image_prompt": "A girl and robot discovering a clue near a park."
        },
        {
            "panel": 4,
            "title": "Finding the Owner",
            "scene": "The girl follows the clue and finds the robot's owner.",
            "image_prompt": "A happy child finding the robot's owner in a colorful neighborhood."
        },
        {
            "panel": 5,
            "title": "Happy Reunion",
            "scene": "The robot is reunited with its owner.",
            "image_prompt": "A happy reunion between a child, a cute robot and its owner."
        }
    ]

    print("\nStarting ComicCraft story generation...\n")

    story = generate_story(sample_outline)

    if story:

        print("\n==============================")
        print("       COMIC STORY")
        print("==============================\n")

        print(story)

    else:

        print("\nStory could not be generated.")