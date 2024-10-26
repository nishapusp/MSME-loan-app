# utils.py

import streamlit as st

def colorful_document_upload(label, key, color):
    """
    Creates a colorful button for document upload in Streamlit.
    
    Args:
    label (str): The label for the upload button.
    key (str): A unique key for the file uploader.
    color (str): The background color of the button in hex format (e.g., "#3498db").
    
    Returns:
    UploadedFile or None: The uploaded file object if a file was uploaded, None otherwise.
    """
    # Custom CSS for the upload button
    custom_css = f"""
    <style>
        .uploadButton {{
            background-color: {color};
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            text-align: center;
            font-weight: bold;
        }}
        .uploadButton:hover {{
            opacity: 0.8;
        }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # Create a unique key for file uploader
    file_key = f"file_uploader_{key}"

    # Custom file uploader button
    upload_button = f'<div class="uploadButton">Upload {label}</div>'
    clicked = st.markdown(upload_button, unsafe_allow_html=True)
    
    # Actual file uploader
    file = st.file_uploader(f"Choose {label} file", type=["pdf", "png", "jpg", "jpeg"], key=file_key, label_visibility="collapsed")
    
    if file:
        st.success(f"{label} uploaded successfully!")
        return file
    return None

def save_progress(section_name, data):
    """
    Saves the progress of a section.
    
    Args:
    section_name (str): The name of the section being saved.
    data (dict): The data to be saved for the section.
    """
    # Implement saving logic here (e.g., to a database or file)
    st.info(f"Saving progress for section: {section_name}")
    # For now, we'll just log the data
    st.write(f"Data to be saved: {data}")

    # In a real application, you might want to save this data to a database or file
    # Example:
    # with open(f"{section_name}_progress.json", "w") as f:
    #     json.dump(data, f)


# You can add more utility functions here as needed