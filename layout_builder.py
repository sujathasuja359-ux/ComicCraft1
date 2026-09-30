def build_comic_layout(images, stories):
    """
    Match each comic panel image with its corresponding story.

    Args:
        images: List of image paths
        stories: List of panel story texts

    Returns:
        List of dictionaries containing:
        - panel number
        - image path
        - text
    """

    comic_layout = []

    # Find the number of panels available
    panel_count = min(len(images), len(stories))

    for i in range(panel_count):

        panel = {
            "panel": i + 1,
            "image": images[i],
            "text": stories[i]
        }

        comic_layout.append(panel)

    return comic_layout


# Test the function
if __name__ == "__main__":

    sample_images = [
        "static/panels/panel_1.png",
        "static/panels/panel_2.png",
        "static/panels/panel_3.png",
        "static/panels/panel_4.png",
        "static/panels/panel_5.png"
    ]

    sample_stories = [
        "A girl finds a lost robot.",
        "She decides to help the robot.",
        "They discover a clue.",
        "They find the robot's owner.",
        "The robot is happily reunited with its owner."
    ]

    layout = build_comic_layout(
        sample_images,
        sample_stories
    )

    print("\nComic Layout:\n")

    for panel in layout:
        print(panel)