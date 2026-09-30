import os
import json

from gemini_flash import generate_outline
from gemini_pro import generate_story
from layout_builder import build_comic_layout
from exporters import save_pdf


def main():

    print("\n==============================")
    print("       COMICCRAFT")
    print("==============================\n")

    story_prompt = input("Enter your comic story idea: ")

    # Step 1: Generate 5-panel outline
    print("\nGenerating 5-panel comic outline...")

    outline = generate_outline(story_prompt)

    if not outline:
        print("\nComic outline could not be generated.")
        return

    print("\nOutline generated successfully!")

    # Step 2: Generate comic story
    print("\nGenerating comic story...")

    story = generate_story(outline)

    if not story:
        print("\nComic story could not be generated.")
        return

    print("\nComic story generated successfully!")

    # Display story
    print("\n==============================")
    print("        COMIC STORY")
    print("==============================\n")

    print(story)

    # Step 3: Prepare story panels
    stories = []

    for panel in outline:
        panel_number = panel.get("panel", 0)
        stories.append(f"Panel {panel_number}: {panel.get('scene', '')}")

    # Step 4: Image paths
    images = []

    for i in range(len(outline)):
        image_path = os.path.join(
            "static",
            "panels",
            f"panel_{i + 1}.png"
        )

        images.append(image_path)

    # Step 5: Build comic layout
    print("\nBuilding comic layout...")

    comic_layout = build_comic_layout(
        images,
        stories
    )

    print("\nComic layout created successfully!")

    # Step 6: Export PDF
    print("\nCreating PDF...")

    pdf_path = save_pdf(comic_layout)

    print("\n==============================")
    print("       COMICCRAFT COMPLETE")
    print("==============================")

    print("\nPDF created at:")
    print(pdf_path)


if __name__ == "__main__":
    main()