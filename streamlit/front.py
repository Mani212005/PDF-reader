import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from core import create_qa_chain, summarize_pdf

st.title("📄 PDF QA & Summarization Assistant")

# Get Google API key from environment variable
api_key = os.getenv("GOOGLE_API_KEY")

# --- UI Sections ---
if not api_key:
    st.error("Google API key not found. Please add it to your .env file.")
else:
    # Upload PDF
    uploaded_file = st.sidebar.file_uploader("Upload a PDF", type="pdf")

    # --- Process PDF ---
    if uploaded_file:
        # Create a temporary directory if it doesn't exist
        temp_dir = "temp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        temp_file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Store file path in session state to be used by summarizer and QA
        st.session_state.temp_file_path = temp_file_path
        
        # Create QA chain and store it in the session state
        with st.spinner("Processing PDF for Q&A..."):
            try:
                # Only create QA chain if it's not already created for this file
                if "qa_chain" not in st.session_state or st.session_state.get("processed_file") != uploaded_file.name:
                    qa_chain = create_qa_chain(api_key, temp_file_path)
                    st.session_state.qa_chain = qa_chain
                    st.session_state.processed_file = uploaded_file.name
                    st.sidebar.success("PDF processed successfully!")
            except Exception as e:
                st.sidebar.error(f"Error processing PDF: {e}")

    if "qa_chain" in st.session_state:
        # --- Summarization Section ---
        st.sidebar.markdown("---")
        if st.sidebar.button("Summarize PDF"):
            with st.spinner("Summarizing PDF... This may take a moment."):
                try:
                    temp_file_path = st.session_state.get("temp_file_path")
                    if temp_file_path and os.path.exists(temp_file_path):
                        summary = summarize_pdf(api_key, temp_file_path)
                        st.session_state.summary = summary
                    else:
                        st.error("Could not find the processed PDF. Please upload it again.")
                except Exception as e:
                    st.error(f"Error summarizing PDF: {e}")

        # Display Summary
        if "summary" in st.session_state:
            st.header("📄 Summary")
            st.write(st.session_state.summary)
            st.markdown("---")

        # --- Q&A Section ---
        st.header("❓ Ask a Question")
        question = st.text_input("What would you like to know from the document?")

        if question:
            with st.spinner("Finding answer..."):
                try:
                    result = st.session_state.qa_chain({"query": question})
                    st.write("### Answer")
                    st.write(result["result"])

                    with st.expander("Show source documents"):
                        st.write(result["source_documents"])
                except Exception as e:
                    st.error(f"Error getting answer: {e}")
    else:
        st.info("Please upload a PDF to begin.")