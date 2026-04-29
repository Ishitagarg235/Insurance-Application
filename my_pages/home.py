# # my_pages/home.py
# import streamlit as st

# def render():
#     st.markdown("""
#     <div style="background: linear-gradient(135deg, #161616, #0f62fe); 
#                 color: white; padding: 80px 40px; text-align: center; 
#                 border-radius: 12px; margin-bottom: 40px;">
#         <h1 style="font-size: 3.5rem; margin: 0;">InsuranceAI</h1>
#         <p style="font-size: 1.5rem; max-width: 800px; margin: 24px auto 0;">
#             Create narratives, risk visuals and professional AI infographics — powered by Gemini & FLUX.
#         </p>
#     </div>
#     """, unsafe_allow_html=True)

#     st.markdown('<div class="section-title">Key Features</div>', unsafe_allow_html=True)
#     cols = st.columns(3)
#     features = [
#         ("Structured Narratives", "Clear, simple explanations"),
#         ("Risk Visuals", "Bar charts & data insights"),
#         ("AI Infographics", "Professional visuals via FLUX.1")
#     ]
#     for col, (title, desc) in zip(cols, features):
#         with col:
#             st.markdown(f"""
#             <div style="padding: 24px; background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); text-align: center;">
#                 <h3>{title}</h3>
#                 <p>{desc}</p>
#             </div>
#             """, unsafe_allow_html=True)

#     st.markdown('<div class="section-title">How It Works</div>', unsafe_allow_html=True)
#     cols = st.columns(4)
#     steps = ["Select type & style", "Add context", "Generate", "Explore & chat"]
#     for col, step in zip(cols, steps):
#         with col:
#             st.markdown(f"""
#             <div style="padding: 24px; background: #edf4ff; border-radius: 8px; text-align: center;">
#                 <h3 style="color: #0f62fe; margin: 0;">{step}</h3>
#             </div>
#             """, unsafe_allow_html=True)

import streamlit as st
 
def render():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #161616, #0f62fe); 
                color: white; padding: 80px 40px; text-align: center; 
                border-radius: 12px; margin-bottom: 40px;">
        <h1 style="font-size: 3.5rem; margin: 0; color: white;">InsuranceAI</h1>
        <p style="font-size: 1.5rem; max-width: 800px; margin: 24px auto 0; color: white;">
            Create narratives, risk visuals and professional AI infographics — powered by Gemini & FLUX.
        </p>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown('<div class="section-title">Key Features</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    features = [
        ("Structured Narratives", "Clear, simple explanations"),
        ("Risk Visuals", "Bar charts & data insights"),
        ("AI Infographics", "Professional visuals via FLUX.1")
    ]
    for col, (title, desc) in zip(cols, features):
        with col:
            st.markdown(f"""
            <div style="padding: 24px; background: white; border-radius: 8px; 
                        box-shadow: 0 2px 12px rgba(0,0,0,0.08); text-align: center;">
                <h3 style="color: #161616; margin: 0 0 8px 0;">{title}</h3>
                <p style="color: #525252; margin: 0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)
 
    st.markdown('<div class="section-title">How It Works</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    steps = ["Select type & style", "Add context", "Generate", "Explore & chat"]
    for col, step in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div style="padding: 24px; background: #edf4ff; border-radius: 8px; text-align: center;">
                <h3 style="color: #0f62fe; margin: 0;">{step}</h3>
            </div>
            """, unsafe_allow_html=True)
 