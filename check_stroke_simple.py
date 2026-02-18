import numpy as np
from PIL import Image

def analyze_stroke_simple(image_path):
    try:
        # Load alpha channel
        img = Image.open(image_path).convert("RGBA")
        alpha = np.array(img)[:,:,3]
        binary = alpha > 128
        
        # Scan horizontal lines to find run-lengths (horizontal strokes)
        run_lengths = []
        
        for row in range(binary.shape[0]):
            row_data = binary[row, :]
            # Find edges
            padded = np.pad(row_data, (1,1), 'constant', constant_values=0)
            diff = np.diff(padded.astype(int))
            starts = np.where(diff == 1)[0]
            ends = np.where(diff == -1)[0]
            
            for s, e in zip(starts, ends):
                length = e - s
                if length > 0:
                    run_lengths.append(length)
                    
        # Filter mostly vertical strokes by checking vertical run lengths too? 
        # Actually, typography has vertical stems and horizontal bars.
        # Vertical stems are measured by horizontal scans.
        
        # We start with horizontal scans -> measures Vertical Stems (like sides of 'H', 'n', 'l')
        vertical_stems = [l for l in run_lengths if 5 < l < 50] # constraint to avoid measuring the whole width of 'E'
        
        if vertical_stems:
            median_stroke = np.median(vertical_stems)
            print(f"Median Vertical Stem Width: {median_stroke} px")
        else:
            print("No stems detected.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_stroke_simple("clariview_logo.png")
