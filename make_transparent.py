from PIL import Image
import os

def remove_background(source_path, target_path, tolerance=30):
    try:
        img = Image.open(source_path).convert("RGBA")
        datas = img.getdata()
        
        # Get the background color from top-left pixel
        bg_color = datas[0]
        
        new_data = []
        for item in datas:
            # Check if pixel is close to background color
            if (abs(item[0] - bg_color[0]) <= tolerance and
                abs(item[1] - bg_color[1]) <= tolerance and
                abs(item[2] - bg_color[2]) <= tolerance):
                new_data.append((255, 255, 255, 0)) # Make Transparent
            else:
                new_data.append(item)
        
        img.putdata(new_data)
        img.save(target_path, "PNG")
        print(f"Transparency applied. Saved to {target_path}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    # Create transparent versions of key assets
    remove_background("assets/logo-xl.png", "assets/logo-xl-transparent.png")
    remove_background("assets/logo-md.png", "assets/logo-md-transparent.png")
