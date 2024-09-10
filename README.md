# InsightViz: Dynamic Content Extraction and Visualization

**InsightViz** is a dynamic content extraction and visualization tool built using Streamlit, LangChain, and Ollama. The application is designed to take a text article (either via file upload or URL) and break it into meaningful chunks. Each chunk is processed to extract the most important lines and create a comic-style scene description, which is then converted into an image using a text-to-image model.

## Features

- **Text Uploading**: You can upload a text file or input a URL containing text.
- **Content Filtering**: Filters out lines with fewer than three words to focus on important content.
- **Text Chunking**: Breaks the text into a specified number of chunks for scene generation.
- **Scene Generation**: Automatically generates a scene prompt based on selected lines from the article.
- **Image Creation**: Connects to a text-to-image model via WebSockets to visualize the scenes as comic-style images.
- **Customizable Input**: Allows users to control the number of chunks and input methods.

## Installation

To run the application, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Aryan185/InsightViz-Dynamic-Content-Extraction-and-Visualization.git
   cd InsightViz-Dynamic-Content-Extraction-and-Visualization:

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt

3. The image generation side is handled on ComfyUI. It uses Flux Dev model and the workflow is begin exported and used as an API here. Make sure that the server, either locally or remote, is on. Change the server address accordingly. If running locally then use as it is else replace with the IP of the remote server.

4. **Run the application**:
   ```bash
   streamlit run app.py


## Usage
### Sidebar Menu:
**Input Method**: Choose between uploading a local file or entering a URL.
**Number of Images**: Select how many chunks (and corresponding images) you want the article to be divided into.

### File Upload or URL Input:
You can upload a .txt file containing an article, or paste a URL for online content.

### Submit Button:
Once you’ve uploaded your file or entered a URL and set the number of chunks, click Submit to generate scene descriptions and images.

### Generated Scenes and Images:
For each chunk of text, the application will:

1. Extract important lines.
2. Generate a scene description.
3. Use a WebSocket server to request a text-to-image model for comic-style images.
4. Display the generated images and their corresponding scene descriptions on the interface.


## JSON Workflow (comicer_flux.json):
This file contains the workflow for generating images from text descriptions. It includes details like text prompts and image configurations.
