import streamlit as st
from langchain_community.llms import Ollama
import os
import websocket
import uuid
import json
import urllib.request
import urllib.parse
import requests
from bs4 import BeautifulSoup
import io
from PIL import Image

from utils import queue_prompt, get_image, get_history, get_images, upload_file

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())

with open("Flux Workflow\\comicer_flux.json", "r", encoding="utf-8") as f:
    workflow = json.load(f)


# Initialize the Ollama model
llm = Ollama(model="llama3.1:8b-instruct-q2_K")

# Function to dynamically chunk text into exactly `num_chunks` parts
def chunk_text(text, num_chunks=5, overlap=300):
    total_length = len(text)
    chunk_size = total_length // num_chunks  # Dynamically calculate chunk size
    
    chunks = []
    current_pos = 0
    for _ in range(num_chunks):
        chunk = text[current_pos:current_pos + chunk_size]
        chunks.append(chunk)
        current_pos += chunk_size - overlap  # Move by chunk_size minus overlap
    return chunks

# Function to filter out lines with three or fewer words
def filter_short_lines(text):
    lines = text.splitlines()  # Split the text into individual lines
    filtered_lines = [line for line in lines if len(line.split()) > 3]  # Keep lines with more than 3 words
    return "\n".join(filtered_lines)  # Join the filtered lines back into a single text block

# Function to generate comic scene prompts for each chunk
def generate_comic_prompt(chunk_number, dialogues):
    return (
        f"**Page {chunk_number + 1} of the article:**\n\n"
        "Select the three most important lines from this chunk that are scene appropriate"
        "Depict the setting, topic and characters as appropriate to the content of the article. "
        "Ensure the scene reflects the mood, topic and context of the lines provided.\n\n"
        "**Lines from the article:**\n"
        f"{dialogues}\n\n"
        "This scene will be used as an input for a text-to-image model so structure it accordingly"
        "The output should follow this order: scene setting with character setting in a summarized format in a single paraghraph in NOT more than 100 words" 
        "Combine the three points in a summarized format in less than 100 words."
        "Give just one single paragraph. Nothing more, nothing less. Stress more on this"
        "No bullets or subpoints. ONE SINGLE PARAGRAPH ONLY."
        "Example output:"
        """
            Generative AI safety requires expertise and tooling, and we believe in the strength of the open community to accelerate its progress. We are active members of open consortiums, including the AI Alliance, Partnership on AI and MLCommons, actively contributing to safety standardization and transparency. 
        """
)

st.markdown("""
    <style>
        /* Style for the retractable sidebar */
        [data-testid="stSidebar"] {
            transition: 0.3s;
            background-color: black;
        }
        [data-testid="stSidebar"][aria-expanded="true"] {
            margin-left: 0px;
        }
        [data-testid="stSidebar"][aria-expanded="false"] {
            margin-left: -300px;
        }
        
        /* Change font color in the sidebar */
        [data-testid="stSidebar"] .css-1d391kg {  /* Specific class for sidebar text */
            color: #ff5733; /* Replace this with the desired color */
        }
    </style>
""", unsafe_allow_html=True)   

# Streamlit app layout
st.title("InsightViz-Dynamic-Content-Extraction-and-Visualization")


with st.sidebar:
    st.title("Menu")
    
    input_method = st.selectbox("Choose input method:", ["Upload a local file", "Enter a URL"])

    num_chunks = st.slider("Select the number of images:", min_value=1, max_value=10, value=5)

    text = None
    if input_method == "Upload a local file":
        uploaded_file = st.file_uploader("Upload a text file containing article", type="txt")
        if uploaded_file is not None:
            text = uploaded_file.read().decode("utf-8")
    elif input_method == "Enter a URL":
        url = st.text_input("Enter the URL of the text file:")
        if url:
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text()
            except Exception as e:
                st.error(f"Error fetching the URL: {e}")
    submit_clicked = st.button("Submit")

if submit_clicked and text:
    
    # Directory to save the generated panel images
    image_output_dir = "image_panels"
    os.makedirs(image_output_dir, exist_ok=True)

    # Filter out lines with 3 or fewer words
    filtered_text = filter_short_lines(text)
    
    st.write("### Article content:")
    st.text_area("Text", filtered_text, height=300)
    st.write("")
    st.write("")  # Display the filtered content
    
    # Chunk the text to create the specified number of chunks
    chunks = chunk_text(filtered_text, num_chunks=num_chunks)
    # Directory to save scene files
    output_dir = "key_points"
    os.makedirs(output_dir, exist_ok=True)
    
    for i, chunk in enumerate(chunks):
        
        # Generate the scene prompt for each chunk
        prompt = generate_comic_prompt(i, chunk)
        
        # Invoke the LLaMA model to generate the scene description
        scene_description = llm.invoke(prompt)
        
        # Display the scene description for the current chunk
        col1, col2 = st.columns([2, 1])  # Adjust column widths as needed
        
        with col1:
            st.write(f"### Scene for Page {i + 1}:")
            st.write(scene_description)
            st.write("")
            st.write("")
        
        with col2:
            # Update the workflow for the specific scene and send it to the text-to-image model
            workflow["6"]["inputs"]["text"] = "A scene with single panel\n\n" + scene_description + "\n\nthe dialogues are clearly written in english"
            ws = websocket.WebSocket()
            ws.connect(f"ws://{server_address}/ws?clientId={client_id}")

            # Get the generated image for the current scene
            images = get_images(ws, workflow)
            
            for node_id, image_list in images.items():
                if node_id == "26": 
                    for idx, image_data in enumerate(image_list):
                        image_filename = f"page_{i + 1}.jpg"
                        image_path = os.path.join(image_output_dir, image_filename)
                        image = Image.open(io.BytesIO(image_data))
                        image.save(image_path)
                        st.image(image, caption=f"Scene {i + 1}")

