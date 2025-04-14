import kagglehub
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

# Download latest version to the same directory as this script
path = kagglehub.dataset_download(
    "iamsouravbanerjee/animal-image-dataset-90-different-animals",
    force_download=True,
    output_dir=current_dir
)

print("Path to dataset files:", path)