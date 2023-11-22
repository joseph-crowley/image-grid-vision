import logging
import time

from image_grid import ImageGrid
from vision_reader import VisionReader

# set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
filename = 'logs/main.log'
handler = logging.FileHandler(filename)
handler.setFormatter(formatter)
logger.addHandler(handler)

if __name__ == "__main__":
    grid_shape = (20,1)

    print("Creating image grids")
    grid_maker = ImageGrid('images', 'image_grids', grid_shape=grid_shape, logger=logger)
    grid_maker.process_images()

    print("Reading image grids with GPT")
    reader = VisionReader(grid_shape=grid_shape, logger=logger)
    t0 = time.perf_counter()
    reading = reader.parse_image("image_grids/output_grid_image_0.png")
    t1 = time.perf_counter()

    print(f"Result (took {t1-t0:.02f} seconds): \n\n{reading}\n\n")
