import os
from PIL import Image

def generate_assets(source_path, output_dir="assets"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        # Load high-quality source
        img = Image.open(source_path).convert("RGBA")
        base_size = img.size
        print(f"Loaded source image: {base_size}")

        # Define target sizes
        targets = {
            # Favicons (Standard squares)
            "favicon-16.png": (16, 16),
            "favicon-32.png": (32, 32),
            "favicon-48.png": (48, 48),
            
            # Apple Touch Icon (iOS Home Screen)
            "apple-touch-icon.png": (180, 180),
            
            # Android / PWA Icons
            "android-chrome-192.png": (192, 192),
            "android-chrome-512.png": (512, 512),
            
            # Social Media Profiles (Standard square avatars)
            "social-insta-320.png": (320, 320),
            "social-fb-180.png": (180, 180), # Facebook suggests at least 180x180
            
            # General Usage Sizes
            "logo-xl.png": (1024, 1024), # Original size
            "logo-lg.png": (512, 512),
            "logo-md.png": (256, 256),
            "logo-sm.png": (128, 128),
        }

        # Generate standard resizes
        for name, size in targets.items():
            # Use LANCZOS for high-quality downscaling
            resized = img.resize(size, Image.Resampling.LANCZOS)
            output_path = os.path.join(output_dir, name)
            resized.save(output_path, "PNG")
            print(f"Generated: {name} ({size[0]}x{size[1]})")

        # Special Case: Open Graph Image (1200x630)
        # This is for link previews on Facebook, LinkedIn, Slack, etc.
        # We need a canvas of 1200x630 and center the logo on it.
        og_size = (1200, 630)
        # Create canvas (White background or transparent? Usually white/colored looks better)
        # Let's detect if the logo has transparency. The user's logo was detected as opaque previously.
        # If opaque, we fill with the edge color? Or just stretch? Stretching is bad.
        # Let's assume a white canvas for safety if transparent, or just paste center.
        
        # Check corner pixel for background color
        bg_color = img.getpixel((0, 0))
        
        # Create canvas with that background color
        og_canvas = Image.new("RGBA", og_size, bg_color)
        
        # Calculate centered position
        # We might want to scale the logo down a bit to fit nicely with padding if source is bigger than 630 height
        # Source is 1024x1024. 
        # Target height is 630. Padding is good. Let's aim for logo height ~400px?
        if base_size[1] > 500:
            ratio = 500 / base_size[1]
            new_w = int(base_size[0] * ratio)
            new_h = int(base_size[1] * ratio)
            logo_for_og = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        else:
            logo_for_og = img

        paste_x = (og_size[0] - logo_for_og.size[0]) // 2
        paste_y = (og_size[1] - logo_for_og.size[1]) // 2
        
        og_canvas.paste(logo_for_og, (paste_x, paste_y), logo_for_og)
        og_path = os.path.join(output_dir, "og-image.png")
        og_canvas.save(og_path, "PNG")
        print(f"Generated: og-image.png (1200x630)")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_assets("clariview_logo.png")
