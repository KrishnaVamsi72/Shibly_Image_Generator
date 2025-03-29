from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image, UnidentifiedImageError
import io
import os
import base64
import requests
from openai import OpenAI

app = FastAPI()

# ✅ Set OpenAI API Key securely (best stored as environment variable)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your_api_key"))

# ✅ Convert any image format to PNG and compress to be < 4MB
def convert_image_to_png(image_data):
    """Convert any image format to PNG and compress to be < 4MB."""
    try:
        img = Image.open(io.BytesIO(image_data))

        # Resize if necessary to reduce file size
        max_size = (1024, 1024)
        img.thumbnail(max_size)

        # Save as PNG in a buffer
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")

        # Check if the size is below 4MB
        if buffered.tell() > 4 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Failed to reduce image size below 4 MB. Please resize the image.")

        return buffered.getvalue()

    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid image format. Please upload a valid PNG, JPEG, GIF, or WEBP.")


# ✅ Generate description of the uploaded image using GPT-4o Vision
async def get_image_description(img_data):
    """Use GPT-4o to describe the uploaded image in detail."""
    try:
        # Convert image to base64 for OpenAI
        img_base64 = base64.b64encode(img_data).decode("utf-8")

        # Use GPT-4o to generate a detailed prompt
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert AI in creating highly detailed, artistic descriptions of images in Studio Ghibli style. "
                        "Describe the facial features, expressions, clothing, and fine details in extreme detail, "
                        "and explain the background, textures, lighting, and atmosphere with vivid language."
                    ),
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe this image in detail to create a Studio Ghibli-style prompt."},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}"}},
                    ],
                },
            ],
            max_tokens=300,
        )

        # ✅ Extract description
        if response and response.choices:
            description = response.choices[0].message.content
            return description

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating image description: {str(e)}")


# ✅ Endpoint to generate Studio Ghibli-style image using DALL·E 3
@app.post("/generate-ghibli/")
async def generate_image(file: UploadFile = File(...)):
    try:
        # ✅ Read and convert uploaded file to PNG
        image_bytes = await file.read()
        img_data = convert_image_to_png(image_bytes)

        # ✅ Get detailed description of the uploaded image
        image_description = await get_image_description(img_data)

        # ✅ Create a detailed Ghibli-style prompt using extracted description
        ghibli_prompt = (
            f"Generate a 2D Studio Ghibli-style illustration with warm pastel colors, expressive faces, and vivid backgrounds. "
            f"The image should reflect the following details with high accuracy: {image_description}. "
            "Ensure that the scene captures the magic, warmth, and rich details found in Ghibli films like 'My Neighbor Totoro', "
            "'Spirited Away', and 'Howl's Moving Castle'."
        )

        # ✅ Generate a Ghibli-style image using DALL·E 3
        dalle_response = client.images.generate(
            model="dall-e-3",
            prompt=ghibli_prompt,
            n=1,
            size="1024x1024",
        )

        # ✅ Parse response and return the generated image URL
        if dalle_response and dalle_response.data:
            image_url = dalle_response.data[0].url
            return JSONResponse(content={"image_url": image_url})

        raise HTTPException(status_code=500, detail="Error generating Ghibli-style image. Please try again.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

