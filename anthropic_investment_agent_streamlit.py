import streamlit as st
import anthropic
from agent_logic import get_base64_image, get_technical_analysis

def main():
    st.set_page_config(page_title="Crypto Technical and On-Chain Analysis", page_icon="📊")

    st.title("Crypto Technical and On-Chain Analysis")

    api_key = st.text_input("Enter your Anthropic API Key", type="password")

    if api_key:
        client = anthropic.Anthropic(api_key=api_key)

        uploaded_image = st.file_uploader("Upload a Crypto Chart", type=["jpeg", "jpg", "png"])

        if uploaded_image:
            image_data = uploaded_image.getvalue()
            base64_image = get_base64_image(image_data)

            st.markdown(f'<img src="{base64_image}" width="500">', unsafe_allow_html=True)

            analysis = get_technical_analysis(client, image_data)

            st.write("### Technical Analysis Summary")
            st.write(analysis)

if __name__ == "__main__":
    main()
