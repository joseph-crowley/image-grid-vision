from PIL import Image
import os
from setup_logger import setup_logger

class ImageGrid:
    def __init__(self, images_folder, output_folder, grid_shape=None, logger=None):
        self.images_folder = images_folder
        self.output_folder = output_folder
        self.grid_shape = grid_shape or (10, 1)
        self.logger = logger or setup_logger('logs/image_grid.log')
        self.logger.info(f"Initialized ImageGrid with images folder {images_folder} and output folder {output_folder}")

    def get_image_size(self, image_path):
        try:
            with Image.open(image_path) as img:
                size = img.size
            self.logger.debug(f"Got image size {size} for {image_path}")
            return size
        except Exception as e:
            self.logger.error(f"Error getting image size for {image_path}: {e}")
            raise

    def combine_images_grid(self, image_paths, output_path, rows, cols, border=0):
        if not image_paths:
            self.logger.error("No image paths provided to combine_images_grid")
            raise ValueError("No image paths provided")

        try:
            image_size = self.get_image_size(image_paths[0])
            grid_width = cols * image_size[0] + (cols - 1) * border
            grid_height = rows * image_size[1] + (rows - 1) * border
            grid_image = Image.new('RGB', (grid_width, grid_height))
            self.logger.info(f"Creating grid image at {output_path} with size {grid_width}x{grid_height}")

            for index, image_path in enumerate(image_paths):
                row = index // cols
                col = index % cols
                position = (col * (image_size[0] + border), row * (image_size[1] + border))
                with Image.open(image_path) as img:
                    grid_image.paste(img, position)
                self.logger.debug(f"Pasted image {image_path} at position {position}")

            grid_image.save(output_path)
            self.logger.info(f"Saved grid image at {output_path}")

        except Exception as e:
            self.logger.error(f"Failed to create grid image: {e}")
            raise

    def process_images(self, border=50):
        try:
            all_image_paths = [os.path.join(self.images_folder, img) for img in os.listdir(self.images_folder)]
            os.makedirs(self.output_folder, exist_ok=True)
            self.logger.info(f"Processing images from {self.images_folder} to {self.output_folder} with border {border}")

            group_size = self.grid_shape[0] * self.grid_shape[1]

            for i in range(0, len(all_image_paths), group_size):
                output_path = os.path.join(self.output_folder, f'output_grid_image_{i}.png')
                self.combine_images_grid(all_image_paths[i:i + group_size], output_path, self.grid_shape[0], self.grid_shape[1], border=border)
                self.logger.info(f"Processed image group starting at index {i}")

        except Exception as e:
            self.logger.error(f"Error in process_images: {e}")
            raise
