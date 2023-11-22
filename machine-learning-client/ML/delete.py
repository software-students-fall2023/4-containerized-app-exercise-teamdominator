import os
import glob

# Set the directory where the files are located
directory = '.'

# Pattern to match files (e.g., frame_0.jpg, frame_1.jpg, etc.)
pattern = "frame_*.jpg"

# Construct full file paths and remove each file
for filepath in glob.glob(os.path.join(directory, pattern)):
    try:
        os.remove(filepath)
        print(f"Removed {filepath}")
    except OSError as e:
        print(f"Error: {e.strerror} - {filepath}")
