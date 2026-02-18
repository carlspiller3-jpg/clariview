import numpy as np
from PIL import Image

def analyze_stroke_width(image_path):
    try:
        img = Image.open(image_path).convert("L")
        arr = np.array(img)
        
        # Binarize (assuming dark text on light bg or vice versa)
        # We know from prev step it's likely light text on dark bg or has transparency
        # Let's use gradient magnitude to find edges, then measure variance?
        # Simpler: Scan horizontal details of the first char 'C' (approx area)
        
        # Crop to the 'C' we found previously (approx coords from previous run)
        # Prev run: BBox (175, 362, 850, 662)
        # Char 1 starts at col ~0 of that bbox.
        # Let's just look at the middle of the 'C'.
        
        crop = arr[400:600, 180:260] # Approximate slice
        
        # Count consecutive pixels
        strokes = []
        for row in crop:
            # find runs of pixels
            pixels = np.where(row < 128)[0] # Assuming dark text? Or light?
            # actually usually logos are on trans background
            # Let's checking center pixel
            pass

        # Better: distance transform
        from scipy.ndimage import distance_transform_edt
        
        # Reload as binary
        img_rgba = Image.open(image_path).convert("RGBA")
        alpha = np.array(img_rgba)[:,:,3]
        binary = alpha > 128
        
        # Distance to nearest zero (background)
        dist = distance_transform_edt(binary)
        
        # The "ridges" of the distance transform are the centers of strokes.
        # The values there are half-widths.
        # We need the skeletal ridges.
        
        # Peak detection: pixel > neighbors
        # crude max
        max_dist = np.max(dist)
        print(f"Max semi-stroke width: {max_dist}")
        print(f"Estimated full stroke width: {max_dist * 2} px")
        
        print("Stroke analysis complete.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_stroke_width("clariview_logo.png")
