# frontend/app.py
import streamlit as st
import requests
import io
from PIL import Image

# Streamlit App UI
st.title("🎨 Shibli: Studio Ghibli-Style Image Generator")
st.write("Upload an image and transform it into a magical Studio Ghibli-style illustration! ✨")

# Upload image widget
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Button to generate Ghibli-style image
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

    if st.button("Generate Studio Ghibli Art ✨"):
        with st.spinner("Processing... Please wait!"):
            # Prepare the uploaded file for API
            files = {"file": uploaded_file.getvalue()}

            # Send the image to the backend FastAPI service
            response = requests.post("http://127.0.0.1:8000/generate-ghibli/", files=files)

            if response.status_code == 200:
                # Parse and display generated Ghibli-style image
                image_url = response.json().get("image_url")

                # Fetch the generated image from the URL
                ghibli_image_response = requests.get(image_url)
                if ghibli_image_response.status_code == 200:
                    # Load the image as bytes for displaying and downloading
                    ghibli_image_bytes = io.BytesIO(ghibli_image_response.content)
                    ghibli_image = Image.open(ghibli_image_bytes)

                    # Display the generated image
                    st.image(ghibli_image, caption="✨ Studio Ghibli Style Art", use_container_width=True)

                    # ✅ Add Download Button
                    st.download_button(
                        label="📥 Download Ghibli Art",
                        data=ghibli_image_bytes.getvalue(),
                        file_name="ghibli_art.png",
                        mime="image/png",
                    )
                else:
                    st.error("Failed to fetch the generated image. Please try again.")
            else:
                st.error(f"Error: {response.json().get('detail')}")
