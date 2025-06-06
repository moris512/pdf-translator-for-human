"""
Utility functions for downloading PDF translations
"""
import os
import logging
import streamlit as st

def check_file_exists(file_path):
    """Check if a file exists and is accessible"""
    if not file_path:
        return False
    return os.path.exists(file_path)

def create_download_button(file_path, original_filename, button_text="Download", help_text=None, use_container_width=False):
    """
    Create a download button for the translated PDF file
    
    Args:
        file_path: Path to the translated PDF file
        original_filename: Original filename to use as a base for the downloaded file
        button_text: The text to display on the button
        help_text: Tooltip text for the button
        use_container_width: Whether the button should expand to fill the container width
        
    Returns:
        bool: True if the button was created, False otherwise
    """
    try:
        if check_file_exists(file_path):
            with open(file_path, "rb") as file:
                st.download_button(
                    label=button_text,
                    data=file,
                    file_name=f"translated_{original_filename}",
                    mime="application/pdf",
                    help=help_text,
                    use_container_width=use_container_width
                )
            return True
        else:
            st.error(f"Translation file not found: {file_path}")
            # Reset session state to allow re-translation
            if 'all_translated' in st.session_state:
                st.session_state.all_translated = False
            return False
    except Exception as e:
        st.error(f"Error preparing download: {str(e)}")
        logging.error(f"Error preparing download: {str(e)}")
        return False
