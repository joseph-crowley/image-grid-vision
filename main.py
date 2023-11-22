import time
import json

from image_grid import ImageGrid
from vision_reader import VisionReader
from setup_logger import setup_logger

def main():
    logger = setup_logger('logs/main.log')
    grid_shape = (20,1)

    print("Creating image grids")
    grid_maker = ImageGrid('images', 'image_grids', grid_shape=grid_shape, logger=logger)
    grid_maker.process_images()

    print("Reading image grids with GPT")
    image_path = "image_grids/output_grid_image_0.png"
    reader = VisionReader(grid_shape=grid_shape, logger=logger)
    t0 = time.perf_counter()
    reading, cost = reader.parse_image(image_path)
    t1 = time.perf_counter()

    print(f"Result (took {t1-t0:.02f} seconds): \n\n{reading}\n\n")
    print(f"Image Cost: \n    ${cost:.6f} total\n    ${cost / (grid_shape[0] * grid_shape[1]):.6f} per reading\n\n")

if __name__ == '__main__':
    main()