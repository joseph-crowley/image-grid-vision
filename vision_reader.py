from openai import OpenAI
import base64
import json
from setup_logger import setup_logger

class VisionReader:
    def __init__(self, grid_shape=None, logger=None):
        """
        Initialize the VisionReader object.

        :param grid_shape: Tuple specifying the grid shape (rows, cols). Defaults to (10, 1).
        :param logger: Logger object for logging messages. If None, a default logger is set up.
        """
        self.client = OpenAI()
        self.grid_shape = grid_shape or (10, 1)
        self.instructions = "Reply with a json object where the values are just the digits read out from the image. The readings are in format with numerical digits, and a sign indication for negative. Example reading: \"X.XXX nA\" where X is a digit 0-9. example response json: {\"row0col0\": \"0.000\", \"row1col0\": \"0.000\", ...}."
        self.logger = logger or setup_logger('logs/vision_reader.log')
        self.logger.info(f"Initialized VisionReader with grid shape {self.grid_shape}")

    def encode_image(self, image_path):
        """
        Encode an image to base64 format.

        :param image_path: Path to the image file.
        :return: Base64 encoded string of the image.
        :raises: Exception if the image cannot be opened or encoded.
        """
        try:
            with open(image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            self.logger.debug(f"Encoded image {image_path} to base64")
            return encoded_image
        except Exception as e:
            self.logger.error(f"Error encoding image {image_path}: {e}")
            raise

    def read_image_grid(self, query, image_path):
        """
        Send a query to the OpenAI API with an image and retrieve the response.

        :param query: Query text to be sent along with the image.
        :param image_path: Path to the image to be processed.
        :return: Response from the OpenAI API.
        :raises: Exception if there's an issue in sending the query or processing the response.
        """
        base64_image = self.encode_image(image_path)
        kwargs = {
            "model": "gpt-4-vision-preview",
            "messages": [
              {
                "role": "system",
                "content": [
                  {
                    "type": "text",
                    "text": self.instructions + f" The image is a {self.grid_shape[0]}x{self.grid_shape[1]} grid. Reply with a the json object for every reading in the grid."
                  }
                ]
              },
              {
                "role": "user",
                "content": [
                  {
                    "type": "text",
                    "text": query
                  },
                  {
                    "type": "image_url",
                    "image_url": {
                      "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                  }
                ]
              }
            ],
            "max_tokens": 3000,
        }
        try:
            response = self.client.chat.completions.create(**kwargs)
            self.logger.info(f"Received response from OpenAI for image {image_path}")
            return response
        except Exception as e:
            self.logger.error(f"Error in read_image_grid for {image_path}: {e}")
            raise

    def parse_image(self, image_path):
        """
        Parse the OpenAI API response to extract readings data.

        :param image_path: Path to the image to be parsed.
        :return: Parsed content from the GPT response.
        :raises: Exception if there's an error in parsing or processing the response.
        """
        try:
            response = self.read_image_grid("What are the current readings for all panels?", image_path)
            if response is None:
                self.logger.error(f"No response received for image {image_path}")
                return None

            self.logger.debug(f"Response: {response}")

            content = response.choices[0].message.content

            # try to remove the code block
            for line in content.splitlines():
                if line.startswith("```"):
                    self.logger.debug("Found code block in vision run response, removing it.")
                    content = content.replace(line, "")

            parsed_content = json.loads(content)
            self.logger.info(f"Parsed content from image {image_path}")
            self.logger.debug(f"Content: {parsed_content}")
            return parsed_content
        except Exception as e:
            self.logger.error(f"Error in parse_image for {image_path}: {e}")
            raise
