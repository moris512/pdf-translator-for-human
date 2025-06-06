"""
Helper functions for PDF translation and download
"""
import logging
import streamlit as st
import pymupdf
from deep_translator import GoogleTranslator
from deep_translator.openai_compatible import OpenAICompatibleTranslator

def create_complete_translation(doc, translator_type, source_lang, target_lang_code, text_color, api_settings, pages_per_load, translator_func):
    """
    Create a complete translation of the document and prepare it for download
    
    Args:
        doc: The input PDF document object
        translator_type: Type of translator to use (Google, OpenAI Compatible)
        source_lang: Source language code
        target_lang_code: Target language code
        text_color: Color to use for translated text
        api_settings: Dictionary containing API settings
        pages_per_load: Number of pages to process at once
        translator_func: Function to use for translation
        
    Returns:
        str: Path to the translated PDF file, or None if translation failed
    """
    try:
        # Initialize translator based on user selection
        if translator_type == "Google":
            translator = GoogleTranslator(
                source=source_lang,
                target=target_lang_code
            )
        else:
            translator = OpenAICompatibleTranslator(
                source=source_lang,
                target=target_lang_code,
                api_key=api_settings.get('api_key'),
                base_url=api_settings.get('api_base'),
                model=api_settings.get('model')
            )

        # Translate all pages
        with st.spinner("Translating entire document... This may take a while."):
            output_doc = pymupdf.open()
            output_path = f"translated_document.pdf"
            
            # Use the translator function from the main app
            output_doc = translator_func(
                doc,
                output_doc,
                translator,
                st.empty(),
                pages_per_load,
                text_color=text_color,
                translator_name=translator_type,
                target_lang=target_lang_code,
                output_path=output_path
            )
            
            return output_path
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        logging.error(f"Translation error: {str(e)}")
        return None

def download_translated_pdf(file_path, original_filename):
    """
    Create a download button for the translated PDF
    
    Args:
        file_path: Path to the translated PDF file
        original_filename: Original filename to use as a base for the downloaded file
    """
    try:
        with open(file_path, "rb") as file:
            st.download_button(
                "📥 Download Complete Translation",
                file,
                file_name=f"translated_{original_filename}",
                mime="application/pdf",
                help="Download the complete translated PDF document",
                use_container_width=True,
            )
    except Exception as e:
        st.error(f"Error preparing download: {str(e)}")
        logging.error(f"Error preparing download: {str(e)}")
