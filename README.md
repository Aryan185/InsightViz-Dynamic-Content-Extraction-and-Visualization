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

2. 
