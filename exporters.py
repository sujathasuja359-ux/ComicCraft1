import os
from fpdf import FPDF


def save_pdf(comic_layout):
    """
    Create a multi-page PDF from the comic layout.

    Each panel gets a separate page containing
    the panel image and story text.

    Returns:
        str: Path of the generated PDF
    """

    # Create exports folder
    output_folder = os.path.join("static", "exports")
    os.makedirs(output_folder, exist_ok=True)

    # PDF file path
    pdf_path = os.path.join(
        output_folder,
        "comiccraft_comic.pdf"
    )

    # Create PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in comic_layout:

        pdf.add_page()

        # Panel number
        pdf.set_font("Arial", "B", 18)
        pdf.cell(
            0,
            10,
            f"Panel {panel['panel']}",
            ln=True,
            align="C"
        )

        pdf.ln(5)

        # Add image if it exists
        image_path = panel.get("image", "")

        if image_path and os.path.exists(image_path):

            pdf.image(
                image_path,
                x=15,
                y=30,
                w=180
            )

            pdf.ln(120)

        else:

            pdf.set_font("Arial", "I", 12)
            pdf.cell(
                0,
                10,
                "Image not available",
                ln=True,
                align="C"
            )

            pdf.ln(10)

        # Story text
        pdf.set_font("Arial", "", 12)

        story_text = str(
            panel.get("text", "")
        )

        pdf.multi_cell(
            0,
            8,
            story_text
        )

    # Save PDF
    pdf.output(pdf_path)

    print("\nPDF created successfully!")
    print("PDF path:")
    print(pdf_path)

    return pdf_path


# Test the function
if __name__ == "__main__":

    sample_layout = [
        {
            "panel": 1,
            "image": "static/panels/panel_1.png",
            "text": "A girl finds a lost robot."
        },
        {
            "panel": 2,
            "image": "static/panels/panel_2.png",
            "text": "She decides to help the robot."
        },
        {
            "panel": 3,
            "image": "static/panels/panel_3.png",
            "text": "They discover a clue."
        },
        {
            "panel": 4,
            "image": "static/panels/panel_4.png",
            "text": "They find the robot's owner."
        },
        {
            "panel": 5,
            "image": "static/panels/panel_5.png",
            "text": "The robot is happily reunited with its owner."
        }
    ]

    save_pdf(sample_layout)