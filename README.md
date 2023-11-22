# Image Grid Vision

Image Grid Vision is a Python toolkit designed with the capabilities of OpenAI's GPT-4 for insightful interpretation of image content. Alongside this, it offer an efficient solution for assembling image grids, optimizing the usage of the OpenAI API by reducing the number of required calls — a practical and cost-effective approach for large-scale image analysis tasks.

## Features
- **Image Grid Creation**: Easily create grids of images, a feature useful for minimizing the number of calls to the OpenAI API. 
- **AI-Powered Image Reading**: Utilize GPT-4V to interpret and analyze images in grids, perfect for applications that require extracting and understanding content from images.

## Getting Started

### Prerequisites
- Python 3.x
- An OpenAI API key. You can obtain it by following the instructions [here](https://platform.openai.com/docs/quickstart/account-setup).

### Installation
1. **Clone the repository**:
   ```
   git clone https://github.com/joseph-crowley/image-grid-vision.git
   ```
2. **Navigate to the project directory**:
   ```
   cd image-grid-vision
   ```
3. **OpenAI API Key**:
   ```
   cp .env.example .env
   ```
   Open the `.env` file and fill in the value for your OpenAI key.

4. **Run the setup script**:
   ```
   source setup.sh
   ```
   This script will install necessary Python packages, set up directories, and source your `.env` file.

## Usage
- After installation, you can import and use the classes `ImageGrid` and `VisionReader` in your Python projects.
- Use `ImageGrid` to create image grids from a folder of images.
- Use `VisionReader` to read and interpret the content of images using OpenAI's GPT-4 model.

## Contribution
Contributions are welcome! Feel free to fork the repository and submit pull requests.

## License
This project is licensed under [MIT License](LICENSE).