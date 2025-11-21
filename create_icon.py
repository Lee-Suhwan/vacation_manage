from PIL import Image, ImageDraw, ImageFont
import os

def create_calendar_icon():
    # Create a 256x256 image with transparent background
    size = (256, 256)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    bg_color = "#FFFFFF"
    header_color = "#EF4444" # Red header
    text_color = "#1E293B"
    border_color = "#E2E8F0"

    # Draw Calendar Body (Rounded Rectangle-ish)
    # Main white body
    draw.rectangle([20, 40, 236, 236], fill=bg_color, outline=border_color, width=4)
    
    # Red Header
    draw.rectangle([20, 40, 236, 90], fill=header_color)

    # Draw "Rings" at the top
    ring_color = "#94A3B8"
    draw.ellipse([50, 20, 70, 50], fill=ring_color)
    draw.ellipse([186, 20, 206, 50], fill=ring_color)

    # Draw "31" text
    # Since we might not have a specific font, we'll try to draw simple shapes or use default
    # For simplicity in this environment without external fonts, let's draw a simple "31"
    
    # Draw 3
    # We can use a large font if available, or just draw lines. 
    # Let's try using default font, scaled up? PIL default font is tiny.
    # We will draw a simple representation of '31' using rectangles/polygons for robustness
    
    # Number Color
    num_color = text_color
    
    # Draw '3'
    # Top bar
    draw.rectangle([70, 120, 130, 135], fill=num_color)
    # Middle bar
    draw.rectangle([70, 155, 130, 170], fill=num_color)
    # Bottom bar
    draw.rectangle([70, 190, 130, 205], fill=num_color)
    # Right vertical
    draw.rectangle([115, 120, 130, 205], fill=num_color)
    
    # Draw '1'
    draw.rectangle([150, 120, 165, 205], fill=num_color)
    # Top serif
    draw.polygon([(150, 135), (150, 120), (135, 135)], fill=num_color)

    # Save as ICO
    img.save('calendar.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    print("calendar.ico created successfully.")

if __name__ == "__main__":
    try:
        create_calendar_icon()
    except ImportError:
        print("PIL (Pillow) is required. Please run 'pip install Pillow'")
