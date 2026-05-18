from analyze_face import analyze_face
import os
import json

image_folder = "../demo_examples"

results = []

for file_name in os.listdir(image_folder):

    if file_name.lower().endswith((".jpg", ".jpeg", ".png")):

        img_path = os.path.join(image_folder, file_name)

        print(f"\nAnalyzing: {file_name}")

        try:
            analysis = analyze_face(img_path)

            results.append({
                "file_name": file_name,
                "analysis": analysis
            })

            print("Done.")

        except Exception as e:
            print(f"Error processing {file_name}: {e}")

output_path = "outputs/batch_results.json"

with open(output_path, "w") as f:
    json.dump(results, f, indent=4)

print(f"\nSaved batch results to {output_path}")