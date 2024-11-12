import streamlit as st
import PyPDF2
from PIL import Image
import io

# Set up the title of the app
st.title("Document Authenticity Checker")

# File uploader widget
uploaded_file = st.file_uploader("Upload a PDF or Image file", type=["pdf", "jpg", "jpeg", "png", "gif"])

def analyze_pdf(file):
    try:
        reader = PyPDF2.PdfReader(file)
        info = reader.metadata
        
        if info is None or not info:
            st.write("PDF Metadata: None found.")
            return "Forged (No metadata detected)"
        
        st.write("PDF Metadata:")
        for key, value in info.items():
            st.write(f"{key}: {value}")
        
        # Simple legitimacy heuristic
        if info.get('/Producer') and info.get('/CreationDate'):
            return "Legit"
        else:
            return "Forged (Missing key metadata fields)"
    
    except Exception as e:
        st.write(f"Error analyzing PDF: {str(e)}")
        return "Forged (Error reading PDF)"

def analyze_image(file):
    try:
        img = Image.open(file)
        st.write("Image Metadata:")
        st.write(f"Format: {img.format}")
        st.write(f"Size: {img.size}")
        st.write(f"Mode: {img.mode}")
        
        # Simple legitimacy heuristic
        if img.format and img.size and img.mode:
            return "Legit"
        else:
            return "Forged (Incomplete metadata)"
    
    except Exception as e:
        st.write(f"Error analyzing image: {str(e)}")
        return "Forged (Error reading image)"

# Main logic to analyze the uploaded file
if uploaded_file is not None:
    file_extension = uploaded_file.name.split(".")[-1].lower()
    
    # Analyzing PDF file
    if file_extension == "pdf":
        st.write("Analyzing PDF file...")
        status = analyze_pdf(uploaded_file)
        st.write(f"Status: {status}")
    
    # Analyzing Image file
    elif file_extension in ["jpg", "jpeg", "png", "gif"]:
        st.write("Analyzing Image file...")
        status = analyze_image(uploaded_file)
        st.write(f"Status: {status}")
    
    # Unsupported file format
    else:
        st.write("Unsupported file format.")
else:
    st.write("Please upload a PDF or Image file to analyze.")
