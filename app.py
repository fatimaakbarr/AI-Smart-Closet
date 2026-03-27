import streamlit as st
from rembg import remove
from PIL import Image
import io

# Set up the page layout
st.set_page_config(page_title="Virtual Closet Uploader", layout="wide")

st.title("👕 Virtual Closet: Item Extractor")
st.write("Upload a photo of your clothing to remove the background and add it to your digital closet!")

# Create a file uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Create two columns on the screen to show Before and After
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Original Photo")
        # Read the uploaded image
        input_image = Image.open(uploaded_file)
        st.image(input_image, use_container_width=True)
        
    with col2:
        st.header("Cleaned Item")
        # Add a button so the user controls when the AI runs
        if st.button("✨ Remove Background ✨"):
            with st.spinner("AI is working its magic..."):
                # Run the background removal
                output_image = remove(input_image)
                
                # Show the clean image
                st.image(output_image, use_container_width=True)
                
                # Create a download button for the clean image
                # We need to convert the image to bytes so the browser can download it
                buf = io.BytesIO()
                output_image.save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                st.download_button(
                    label="💾 Download to Closet",
                    data=byte_im,
                    file_name="clean_clothing_item.png",
                    mime="image/png"
                )