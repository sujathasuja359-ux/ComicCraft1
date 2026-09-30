import os
import json
import time
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


def generate_outline(story_prompt):
    """
    Generate a structured 5-panel comic outline
    using the Gemini Flash model.
    """

    prompt = f"""
Create a structured 5-panel comic outline based on this story idea:

{story_prompt}

For each panel, provide:

- panel number
- title
- scene description
- image generation prompt

Return ONLY valid JSON in this format:

[
  {{
    "panel": 1,
    "title": "Panel title",
    "scene": "Scene description",
    "image_prompt": "Image generation prompt"
  }},
  {{
    "panel": 2,
    "title": "Panel title",
    "scene": "Scene description",
    "image_prompt": "Image generation prompt"
  }},
  {{
    "panel": 3,
    "title": "Panel title",
    "scene": "Scene description",
    "image_prompt": "Image generation prompt"
  }},
  {{
    "panel": 4,
    "title": "Panel title",
    "scene": "Scene description",
    "image_prompt": "Image generation prompt"
  }},
  {{
    "panel": 5,
    "title": "Panel title",
    "scene": "Scene description",
    "image_prompt": "Image generation prompt"
  }}
]
"""

    max_retries = 5

    for attempt in range(max_retries):

        try:
            print(f"Trying Gemini request... Attempt {attempt + 1}/{max_retries}")

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            result = response.text.strip()

            # Remove markdown code block if Gemini adds it
            if result.startswith("```json"):
                result = result[7:]

            if result.startswith("```"):
                result = result[3:]

            if result.endswith("```"):
                result = result[:-3]

            result = result.strip()

            # Convert JSON text into Python list
            outline = json.loads(result)

            return outline

        except Exception as e:

            error_message = str(e)

            if "503" in error_message or "UNAVAILABLE" in error_message:

                print("\nGemini server is currently busy.")
                print("Waiting before trying again...\n")

                if attempt < max_retries - 1:
                    time.sleep(10)
                else:
                    print("Gemini is still unavailable.")
                    print("Please try again later.")

            else:
                print("Error:", e)
                break

    return None


# Test the function
if __name__ == "__main__":

    sample_story = """
    A young girl finds a lost robot in her neighborhood.
    She tries to find the robot's owner and finally reunites them.
    """

    print("\nGenerating comic outline...\n")

    outline = generate_outline(sample_story)

    if outline:

        print("\nComic Outline:\n")

        print(json.dumps(outline, indent=2))

    else:

        print("\nComic outline could not be generated.")