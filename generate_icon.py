from PIL import Image, ImageDraw, ImageFont
import os


def create_icon():
    # Create a new image with a transparent background
    size = 256
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Draw a rounded rectangle for the document
    margin = 40
    draw.rounded_rectangle(
        [margin, margin, size-margin, size-margin],
        radius=20,
        fill=(52, 152, 219),  # Blue color
        outline=(41, 128, 185),  # Darker blue
        width=4
    )

    # Draw "LLM" text
    try:
        font_size = 72
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Fallback to default font if arial not available
        font = ImageFont.load_default()

    text = "LLM"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    x = (size - text_width) // 2
    y = (size - text_height) // 2

    # Add white text with a slight shadow
    draw.text((x+2, y+2), text, fill=(0, 0, 0, 64), font=font)  # Shadow
    draw.text((x, y), text, fill=(255, 255, 255), font=font)  # Text

    # Save as PNG
    os.makedirs('assets', exist_ok=True)
    image.save('assets/app_icon.png')

    # Save as ICO
    image.save('assets/app_icon.ico', format='ICO', sizes=[(256, 256)])


if __name__ == '__main__':
    create_icon()
