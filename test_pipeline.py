from video import extract_frames
from pipeline import generate_all_captions

frames = extract_frames("sample.mp4", num_frames=4)

scene, captions = generate_all_captions(frames)

print("\n========== SCENE ==========\n")
print(scene)

print("\n========== CAPTIONS ==========\n")

for style, caption in captions.items():
    print(f"\n{style.upper()}")
    print(caption)