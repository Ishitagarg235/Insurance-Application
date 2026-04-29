# my_pages/detail.py
import streamlit as st
import pandas as pd

def render():
    st.header("Concept Detail")

    item = st.session_state.get("detail_item")
    if not item:
        st.warning("No item selected.")
        return

    st.markdown(f"### {item['type']} – {item['style']}")

    tabs = st.tabs(["Narrative", "Risk", "Prompt", "Image"])

    with tabs[0]:
        st.markdown(item["narrative"])

    with tabs[1]:
        if item["risk_data"].get("risks"):
            df = pd.DataFrame(item["risk_data"]["risks"], columns=["Risk", "Level", "Desc"])
            st.bar_chart(df.set_index("Risk")["Level"])
            st.dataframe(df)

    with tabs[2]:
        st.text_area("Prompt", item["image_prompt"], height=120)

    with tabs[3]:
        if item.get("image"):
            st.image(item["image"], use_column_width=True)
        else:
            st.info("No image")

    if st.button("← Back"):
        st.session_state.page = "history"  # or previous page
        st.rerun()