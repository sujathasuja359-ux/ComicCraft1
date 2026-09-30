import os
import re
import torch
from diffusers import StableDiffusionPipeline


# Stable Diffusion model
MODEL_ID = "runwayml/stable-diffusion-v1-5"


# Select device
if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"


print("Loading Stable Diffusion model...")
print("Device:", device)


# Load Stable Diffusion
pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32
)

pipe = pipe.to(device)


def generate_image(image_prompt):
    """
    Generate a comic-style image using Stable Diffusion.

    The generated image is saved inside:
    static/panels

    Returns:
        str: Path of the generated image
    """

    # Create output folder
    output_folder = os.path.join("static", "panels")
    os.makedirs(output_folder, exist_ok=True)

    # Create a safe filename
    safe_name = re.sub(
        r"[^a-zA-Z0-9]+",
        "_",
        image_prompt
    )

    safe_name = safe_name[:80].strip("_")

    if not safe_name:
        safe_name = "comic_panel"

    image_path = os.path.join(
        output_folder,
        safe_name + ".png"
    )

    print("\nGenerating image...")
    print("Prompt:")
    print(image_prompt)

    # Generate image
    image = pipe(
        prompt=image_prompt,
        num_inference_steps=20,
        guidance_scale=7.5
    ).images[0]

    # Save image
    image.save(image_path)

    print("\nImage generated successfully!")
    print("Saved at:")
    print(image_path)

    return image_path


# Test the function
if __name__ == "__main__":

    sample_prompt = """
    A cute young girl discovering a small friendly robot
    on a colorful neighborhood street,
    children's comic book style,
    bright and colorful illustration
    """

    print("\nStarting ComicCraft image generation...")

    generated_path = generate_image(sample_prompt)

    print("\nFinal image path:")
    print(generated_path)