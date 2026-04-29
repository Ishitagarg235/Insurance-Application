# my_pages/history.py
import streamlit as st

def render():
    st.header("Generation History")

    if not st.session_state.history:
        st.info("No generations yet.")
        return

    search_term = st.text_input("Search", "")

    filtered = [item for item in st.session_state.history if search_term.lower() in str(item).lower()]

    for item in filtered:
        with st.expander(f"{item['type']} – {item['style']}"):
            st.write(f"Context: {item.get('context', '—')}")
            if st.button("View Detail", key=f"h_view_{id(item)}"):
                st.session_state.detail_item = item
                st.session_state.page = "detail"
                st.rerun()
            if st.button("Delete", key=f"h_del_{id(item)}"):
                st.session_state.history.remove(item)
                st.rerun()