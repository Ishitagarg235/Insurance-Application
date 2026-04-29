from huggingface_hub import InferenceClient
from PIL import Image
import io
import streamlit as st
# Your working token

client = InferenceClient(token=st.secrets["HF_TOKEN"])

def generate_image(prompt: str) -> Image.Image | None:
    """
    Generate image using Hugging Face Inference API.
    Returns PIL Image or None if failed.
    """
    try:
        print(f"[HF] Generating → {prompt[:70]}{'...' if len(prompt)>70 else ''}")

        # The model that worked in your last test
        model_id = "black-forest-labs/FLUX.1-schnell"

        result = client.text_to_image(
            prompt=prompt,
            model=model_id,
            negative_prompt="blurry, low quality, bad anatomy, watermark, text, deformed, ugly, extra limbs",
            width=768,
            height=512,
            num_inference_steps=28,
            guidance_scale=7.0,
        )

        # Handle both return types (bytes or already PIL Image)
        if isinstance(result, Image.Image):
            print(f"[HF] Success – got PIL Image directly")
            return result
        else:
            print(f"[HF] Success – received {len(result)} bytes")
            return Image.open(io.BytesIO(result))

    except Exception as e:
        print(f"[HF ERROR] {type(e).__name__}: {str(e)}")
        return None