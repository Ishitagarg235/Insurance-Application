# my_pages/gallery.py
import streamlit as st

def render():
    st.header("Gallery")

    if not st.session_state.history:
        st.info("No concepts yet.")
        return

    cols = st.columns(3)
    for idx, item in enumerate(st.session_state.history):
        with cols[idx % 3]:
            if item.get("image"):
                st.image(item["image"], use_column_width=True)
            st.caption(item['type'])
            if st.button("View", key=f"g_view_{idx}"):
                st.session_state.detail_item = item
                st.session_state.page = "detail"
                st.rerun()