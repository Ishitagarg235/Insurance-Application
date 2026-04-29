# my_pages/studio.py
import streamlit as st
import json
import pandas as pd
import io
from llm import generate_text
from image_gen import generate_image

INSURANCE_TYPES = [
    "Life Insurance", "Health Insurance", "Auto Insurance", "Home Insurance",
    "Cyber Insurance", "Travel Insurance", "Business Insurance", "Pet Insurance"
]

VISUAL_STYLES = [
    "Risk Infographic", "Coverage Map", "Claims Flow", "Risk Pyramid", "Comparison Chart"
]

def render():
    st.header("Creator Studio")
    st.caption("Generate explanations, risk visuals and AI infographics")

    col1, col2 = st.columns([3, 2])
    with col1:
        insurance_type = st.selectbox("Insurance Type", [""] + INSURANCE_TYPES)
    with col2:
        visual_style = st.selectbox("Visual Style", [""] + VISUAL_STYLES)

    context = st.text_area("Context / target audience", height=100)

    if st.button("Generate Concept", type="primary", use_container_width=True):

        if not insurance_type:
            st.error("Please select an insurance type.")
            st.stop()

        with st.spinner("Generating concept..."):

            base = f"{insurance_type}"
            if visual_style:
                base += f" – {visual_style} style"
            if context.strip():
                base += f". Context: {context.strip()}"

            # ── TEXT PART (Gemini) ──────────────────────────────────────────────
            narrative = None
            image_prompt = None
            risk_data = {"risks": []}

            try:
                # Narrative
                narrative_prompt = f"Explain {base} in simple language.\nUse headings: **Overview** **Main Risks** **What is Covered** **Who Needs It** **Tips**"
                narrative = generate_text(narrative_prompt)

                # Image prompt suggestion
                img_prompt_text = f"Write detailed FLUX prompt for infographic: {base}"
                image_prompt = generate_text(img_prompt_text).strip()

                # Risk data
                               
                risk_prompt = f"Return only JSON: {{'risks': [['Risk', level 1-10, 'desc']]}} for {insurance_type}"
                raw = generate_text(risk_prompt)
                cleaned = raw.strip().replace("```json","").replace("```","").strip()

                try:
                    risk_data = json.loads(cleaned)
                except json.JSONDecodeError:
                    st.warning("Could not parse risk JSON — using empty data")
                    risk_data = {"risks": []}
                st.success("Text & data generated successfully (Gemini)")
            except Exception as gemini_err:
                st.error(f"Gemini text generation failed: {str(gemini_err)}")
                st.info("Using fallback content for text parts. Image generation is independent and still works.")

                # Fallback dummy content so tabs don't break
                narrative = f"**Overview**\nThis is a placeholder because Gemini API key is currently blocked.\n\n**Main Risks**\n- Placeholder risk 1\n- Placeholder risk 2\n\n**What is Covered**\n- Placeholder coverage\n\n**Who Needs It**\n- Placeholder audience\n\n**Tips**\n- Get a new API key from https://aistudio.google.com"
                image_prompt = f"Clean professional infographic about {base}, blue-white corporate style, charts, icons"

            # ── IMAGE PART (Hugging Face) ──────────────────────────────────────
            generated_image = None
            try:
                st.caption("Generating image via Hugging Face (FLUX.1-schnell)...")
                generated_image = generate_image(image_prompt)
                if generated_image is not None:
                    st.success("Hugging Face image generated successfully!")
                else:
                    st.warning("Hugging Face returned no image – check terminal")
            except Exception as hf_err:
                st.error(f"Hugging Face image failed: {str(hf_err)}")

            # ── Save to history ─────────────────────────────────────────────────
            st.session_state.history.append({
                "type": insurance_type,
                "style": visual_style or "Default",
                "context": context.strip(),
                "narrative": narrative,
                "image_prompt": image_prompt,
                "risk_data": risk_data,
                "image": generated_image,  # still storing PIL Image here
                "timestamp": pd.Timestamp.now().isoformat()
            })

        # ── Results Tabs ────────────────────────────────────────────────────────
        tab_narr, tab_risk, tab_prompt, tab_img = st.tabs([
            "📝 Narrative",
            "📊 Risk Overview",
            "🎨 Image Prompt",
            "🖼️ AI Image"
        ])

        with tab_narr:
            st.markdown(narrative or "No narrative available")

        with tab_risk:
            if risk_data.get("risks"):
                df = pd.DataFrame(risk_data["risks"], columns=["Risk", "Level", "Description"])
                st.bar_chart(df.set_index("Risk")["Level"], height=320)
                st.dataframe(df, hide_index=True)
            else:
                st.info("No risk data available (Gemini failed)")

        with tab_prompt:
            st.text_area("Image Prompt (used for Hugging Face)", 
                        image_prompt or "No prompt generated", 
                        height=140)

        with tab_img:
            if generated_image is not None:
                st.image(generated_image, 
                         use_column_width=True,
                         caption=f"{insurance_type} — {visual_style or 'Generated Concept'}")

                # Show image dimensions
                w, h = generated_image.size
                st.caption(f"Generated image: {w}×{h} px • PNG")

                # ── FIXED: Convert PIL Image → bytes for download ───────────────
                buf = io.BytesIO()
                generated_image.save(buf, format="PNG")
                byte_data = buf.getvalue()

                st.download_button(
                    label="Download Image",
                    data=byte_data,
                    file_name=f"{insurance_type.replace(' ', '_')}_infographic.png",
                    mime="image/png",
                    use_container_width=False
                )
            else:
                st.info("No image generated this time.\nCheck terminal for Hugging Face logs.")