from PIL import Image, ImageDraw, ImageFont

def create_logo():
    # Colors
    bg_color = (26, 30, 57, 255)  # #1A1E39
    text_color = (249, 250, 250, 255) # #F9FAFA
    
    # Dimensions (High res)
    width = 800
    height = 200
    
    # Create image
    img = Image.new('RGBA', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Load Font
    # We'll try to load a system font or default if not available
    try:
        # Try to find a nice sans-serif font
        font = ImageFont.truetype("arial.ttf", 100)
    except IOError:
        font = ImageFont.load_default()
        
    text = "ClariView"
    
    # Calculate text size using textbbox (newer PIL versions)
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    text_w = right - left
    text_h = bottom - top
    
    # Center text
    x = (width - text_w) / 2
    y = (height - text_h) / 2 - 10 # nudge up slightly
    
    draw.text((x, y), text, font=font, fill=text_color)
    
    img.save("assets/logo-new.png")
    print("Logo created at assets/logo-new.png")

if __name__ == "__main__":
    create_logo()
