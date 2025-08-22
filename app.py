import streamlit as st

st.set_page_config(
    page_title="Prompting Under Pressure",
    page_icon="🧠",
    initial_sidebar_state="collapsed",
)

hide_streamlit_elements = """
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
        </style>
    """
st.markdown(hide_streamlit_elements, unsafe_allow_html=True)

st.write("# Prompting Under Pressure: Research Overview 🧠")

st.sidebar.success("Navigate through research sections")

st.markdown(
    """
    ### Research Focus
    This project investigates how **cognitive load** and **stress** affect user interactions with 
    Large Language Models (LLMs), particularly the **length, specificity, and quality** of prompts.  

    ### Research Questions
    1. How does stress/cognitive load affect the quality of prompt formulation?  
    2. To what extent does it influence reliance on prompting strategies and perceived task success?  
    3. Are there measurable differences in LLM performance across baseline, stress, and overload conditions?  
    4. What design recommendations can support users under stress when prompting LLMs?  

    ### Motivation
    LLMs are increasingly used in high-pressure scenarios, yet little is known about how stress 
    shapes **prompting behaviour and task outcomes**. This research addresses that gap from a 
    human-centered perspective.  

    ### Methodology
    - **Participants:** 30+, aged 18–45, fluent in English, with prior LLM experience  
    - **Data Collection:**  
      • Surveys (demographics, anxiety levels)  
      • Experimental tasks (baseline, cognitive load, acute stress)
      • Analysis of prompt history (length, specificity, strategy)  

    ### Expected Contributions
    - Empirical evidence on the relationship between stress and LLM prompt quality  
    - Design insights for stress-resilient LLM interfaces  
    - Recommendations for inclusive AI systems supporting diverse real-world conditions  
    """
)
