**Studio Ghibli-Style Image Generator**

*Overview*

This project explores generating Studio Ghibli-style images using GPT-4o and DALL·E 3. The goal is to transform uploaded images into beautiful, hand-painted Ghibli aesthetics. While the results are promising, the current implementation has limitations in capturing the full essence of Ghibli's signature style.

*Tech Stack*

Frontend: Streamlit

Backend: Python, OpenAI's GPT-4o & DALL·E 3 API

Hosting: Streamlit Cloud

Dependencies: OpenAI API, Pillow, NumPy, Requests

*Features*

Upload an image and apply AI-generated transformations

Generate art inspired by Studio Ghibli’s visual style

Experiment with different prompts and styles

*Current Limitations*

Inconsistent Styling: Some images do not fully capture the soft, dreamy feel of Ghibli aesthetics.

Facial Features: AI struggles with detailed, expressive anime-like facial expressions.

Background Quality: Generated backgrounds may lack the depth and organic touch seen in Ghibli films.

*Try It Out*

You can test the current implementation here: https://shiblyimagegenerator-mb88u94rhqvvzzhn5iknr9.streamlit.app/

**How to Run Locally**

*Prerequisites*

Ensure you have the following installed on your system:

Python 3.8+

pip (Python package manager)

OpenAI API key

*Installation Steps*

Clone the repository:

git clone https://github.com/yourusername/studio-ghibli-image-generator.git
cd studio-ghibli-image-generator

Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

Install the dependencies:

pip install -r requirements.txt

Set up your OpenAI API key:

export OPENAI_API_KEY='your-api-key'  # Windows: set OPENAI_API_KEY=your-api-key

Run the application:

streamlit run app.py

Open your browser and go to http://localhost:8501

How to Improve

We welcome suggestions and contributions to enhance the results! Some potential areas of improvement:

Fine-tuning models with high-quality Ghibli-inspired datasets

Adjusting diffusion-based approaches for better texture and lighting

Exploring alternative AI models specialized in anime-style rendering

Contributing

If you have ideas or improvements, feel free to:

Fork this repository

Create a new branch

Make your changes and submit a pull request

