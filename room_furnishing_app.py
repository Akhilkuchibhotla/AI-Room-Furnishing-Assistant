import streamlit as st
import os
import io
import base64
from PIL import Image as PILImage
from google import genai
from google.genai import types
import tempfile
import zipfile
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Room Furnishing Assistant",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1a365d;
        font-size: 2.5rem;
        font-weight: 600;
        margin-bottom: 2rem;
        letter-spacing: -0.02em;
    }
    .section-header {
        color: #2d3748;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 0.5rem;
    }
    .room-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .preference-section {
        background-color: #f7fafc;
        padding: 1.25rem;
        border-radius: 8px;
        margin: 0.75rem 0;
        border-left: 4px solid #3182ce;
        border: 1px solid #e2e8f0;
    }
    .success-message {
        background-color: #f0fff4;
        color: #22543d;
        padding: 0.75rem;
        border-radius: 6px;
        border: 1px solid #9ae6b4;
        font-weight: 500;
    }
    .error-message {
        background-color: #fed7d7;
        color: #742a2a;
        padding: 0.75rem;
        border-radius: 6px;
        border: 1px solid #feb2b2;
        font-weight: 500;
    }
    .info-message {
        background-color: #ebf8ff;
        color: #2c5282;
        padding: 0.75rem;
        border-radius: 6px;
        border: 1px solid #90cdf4;
        font-weight: 500;
    }
    .warning-message {
        background-color: #fffbeb;
        color: #744210;
        padding: 0.75rem;
        border-radius: 6px;
        border: 1px solid #f6e05e;
        font-weight: 500;
    }
    .before-after {
        display: flex;
        gap: 1rem;
        align-items: center;
    }
    .room-image {
        flex: 1;
        text-align: center;
    }
    .button-primary {
        background-color: #3182ce;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 500;
    }
    .button-secondary {
        background-color: #4a5568;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 500;
    }
    .metric-card {
        background-color: #f7fafc;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    .upload-area {
        border: 2px dashed #cbd5e0;
        border-radius: 8px;
        padding: 2rem;
        text-align: center;
        background-color: #f7fafc;
        transition: border-color 0.2s;
    }
    .upload-area:hover {
        border-color: #3182ce;
        background-color: #ebf8ff;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'furnished_rooms' not in st.session_state:
    st.session_state.furnished_rooms = []
if 'client' not in st.session_state:
    st.session_state.client = None
if 'uploaded_furniture' not in st.session_state:
    st.session_state.uploaded_furniture = []

def initialize_client(api_key):
    """Initialize the Gemini client"""
    try:
        client = genai.Client(api_key=api_key)
        st.session_state.client = client
        return True
    except Exception as e:
        st.error(f"Error initializing client: {str(e)}")
        return False

def display_response(response):
    """Display response parts (text and images)"""
    for part in response.parts:
        if part.text:
            st.markdown(part.text)
        elif image := part.as_image():
            # Convert to PIL Image for display
            pil_image = PILImage.open(io.BytesIO(image.image_bytes))
            st.image(pil_image, caption="Furnished Room", use_container_width=True)
            return pil_image
    return None

def save_furnished_room(original_image, furnished_image, preferences, filename, uploaded_furniture=None):
    """Save furnished room to session state"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{timestamp}_{filename}"
    st.session_state.furnished_rooms.append({
        'original': original_image,
        'furnished': furnished_image,
        'preferences': preferences,
        'uploaded_furniture': uploaded_furniture,
        'filename': safe_filename,
        'timestamp': timestamp
    })

def create_room_prompt(preferences, uploaded_furniture_images=None):
    """Create a detailed prompt based on user preferences and uploaded furniture"""
    style = preferences.get('style', 'modern')
    color_scheme = preferences.get('color_scheme', 'neutral')
    furniture_style = preferences.get('furniture_style', 'contemporary')
    room_type = preferences.get('room_type', 'living room')
    lighting = preferences.get('lighting', 'natural')
    additional_items = preferences.get('additional_items', [])
    
    prompt = f"""
    Transform this room into a beautifully furnished {room_type} with the following specifications:
    
    Style: {style}
    Color Scheme: {color_scheme}
    Furniture Style: {furniture_style}
    Lighting: {lighting}
    
    Additional Requirements:
    - Add appropriate furniture for a {room_type}
    - Maintain the room's architectural features and layout
    - Ensure the furniture fits the space proportionally
    - Create a cohesive design that matches the {style} style
    - Use {color_scheme} colors throughout
    - Add {lighting} lighting elements
    """
    
    if additional_items:
        prompt += f"\n- Include these specific items: {', '.join(additional_items)}"
    
    if uploaded_furniture_images:
        prompt += f"\n\nIMPORTANT: The user has uploaded specific furniture/accessory images that they want to see in this room. Please integrate these items naturally into the room design:"
        for i, furniture_data in enumerate(uploaded_furniture_images):
            prompt += f"\n- Furniture Item {i+1}: {furniture_data['description']} (from uploaded image)"
        prompt += "\n- Make sure these uploaded items are prominently featured and well-integrated into the overall design"
        prompt += "\n- Adjust the room's color scheme and other elements to complement these specific furniture pieces"
    
    prompt += """
    
    Make the room look realistic, lived-in, and professionally designed. Ensure all furniture and decor items are appropriate for the space and create a harmonious, inviting atmosphere.
    """
    
    return prompt

# Main header
st.markdown('<h1 class="main-header">AI Room Furnishing Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.1rem; color: #4a5568; margin-bottom: 2rem;">Transform empty spaces into professionally designed rooms using AI-powered furniture integration</p>', unsafe_allow_html=True)

# Sidebar for API key and settings
with st.sidebar:
    st.header("Configuration")
    
    # API Key input
    api_key = st.text_input(
        "Google AI API Key",
        type="password",
        help="Get your API key from https://aistudio.google.com/apikey"
    )
    
    if api_key:
        if initialize_client(api_key):
            st.success("API Key loaded successfully!")
        else:
            st.error("Invalid API Key")
    else:
        st.warning("Please enter your API key to continue")
    
    st.divider()
    
    # Model selection
    model_id = st.selectbox(
        "Select Model",
        ["gemini-2.5-flash-image-preview"],
        help="Currently only Gemini 2.5 Flash Image Preview is supported"
    )
    
    st.divider()
    
    # Furnished rooms counter
    st.metric("Furnished Rooms", len(st.session_state.furnished_rooms))

# Main content area
if not api_key:
    st.info("Please enter your API key in the sidebar to get started!")
    st.stop()

if not st.session_state.client:
    st.error("Please check your API key and try again!")
    st.stop()

# Main interface - Upload Section
st.header("Upload Images")
col_upload1, col_upload2 = st.columns([1, 1])

with col_upload1:
    st.subheader("Room Image")
    uploaded_file = st.file_uploader(
        "Choose a room image",
        type=['png', 'jpg', 'jpeg'],
        help="Upload a clear image of an empty or partially furnished room",
        key="room_upload"
    )
    
    if uploaded_file:
        original_image = PILImage.open(uploaded_file)
        st.image(original_image, caption="Original Room", use_container_width=True)
        st.info(f"Image size: {original_image.size[0]}x{original_image.size[1]} pixels")

with col_upload2:
    st.subheader("Furniture & Accessories (Optional)")
    uploaded_furniture_files = st.file_uploader(
        "Choose furniture/accessory images",
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        help="Upload images of specific furniture or accessories you want to include",
        key="furniture_upload"
    )
    
    if uploaded_furniture_files:
        st.session_state.uploaded_furniture = []
        
        for i, furniture_file in enumerate(uploaded_furniture_files):
            furniture_image = PILImage.open(furniture_file)
            
            col_furn1, col_furn2 = st.columns([1, 2])
            
            with col_furn1:
                st.image(furniture_image, caption=f"Item {i+1}", use_container_width=True)
            
            with col_furn2:
                furniture_description = st.text_input(
                    f"Describe item {i+1}",
                    placeholder="e.g., Modern gray sofa, Wooden coffee table...",
                    key=f"furniture_desc_{i}",
                    help="Describe what this furniture item is"
                )
                
                if furniture_description:
                    st.session_state.uploaded_furniture.append({
                        'image': furniture_image,
                        'description': furniture_description,
                        'filename': furniture_file.name
                    })
        
        if st.session_state.uploaded_furniture:
            st.success(f"{len(st.session_state.uploaded_furniture)} items ready!")
        else:
            st.warning("Please add descriptions for your furniture items")

# Design Preferences Section
st.header("Design Preferences")
col_pref1, col_pref2 = st.columns(2)

with col_pref1:
    st.markdown('<div class="preference-section">', unsafe_allow_html=True)
    
    # Room type
    room_type = st.selectbox(
        "Room Type",
        ["living room", "bedroom", "dining room", "kitchen", "office", "bathroom", "nursery", "study room"],
        help="What type of room is this?"
    )
    
    # Style
    style = st.selectbox(
        "Design Style",
        ["modern", "minimalist", "traditional", "contemporary", "scandinavian", "industrial", "bohemian", "rustic", "mid-century modern", "art deco"],
        help="Choose your preferred design style"
    )
    
    # Color scheme
    color_scheme = st.selectbox(
        "Color Scheme",
        ["neutral", "warm", "cool", "monochrome", "pastel", "bold", "earth tones", "jewel tones", "black and white"],
        help="Select your preferred color palette"
    )
    
    # Furniture style
    furniture_style = st.selectbox(
        "Furniture Style",
        ["contemporary", "vintage", "modern", "traditional", "industrial", "scandinavian", "mid-century", "rustic", "luxury"],
        help="What style of furniture do you prefer?"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

with col_pref2:
    st.markdown('<div class="preference-section">', unsafe_allow_html=True)
    
    # Lighting
    lighting = st.selectbox(
        "Lighting Preference",
        ["natural", "warm", "cool", "ambient", "dramatic", "soft", "bright"],
        help="How would you like the room to be lit?"
    )
    
    # Additional items
    additional_items = st.multiselect(
        "Additional Items (Optional)",
        ["plants", "artwork", "rugs", "cushions", "books", "decorative objects", "mirrors", "lamps", "curtains", "shelving"],
        help="Select any additional decorative items you'd like"
    )
    
    # Special instructions
    special_instructions = st.text_area(
        "Special Instructions (Optional)",
        placeholder="Any specific requirements or preferences not covered above...",
        height=80,
        help="Add any specific requirements or preferences"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Generation Options
st.header("Generate Room Designs")
col_gen1, col_gen2, col_gen3 = st.columns([1, 1, 1])

with col_gen1:
    single_style = st.button("Generate Single Style", type="primary", use_container_width=True)

with col_gen2:
    multiple_styles = st.button("Generate 4 Style Variations", type="secondary", use_container_width=True)

with col_gen3:
    if st.session_state.uploaded_furniture:
        preview_style = st.button("Preview Furniture", type="secondary", use_container_width=True)

# Process single style generation
if single_style and uploaded_file:
    with st.spinner("AI is furnishing your room... This may take a moment."):
        try:
            # Create preferences dictionary
            preferences = {
                'room_type': room_type,
                'style': style,
                'color_scheme': color_scheme,
                'furniture_style': furniture_style,
                'lighting': lighting,
                'additional_items': additional_items,
                'special_instructions': special_instructions
            }
            
            # Create the prompt
            uploaded_furniture_data = st.session_state.uploaded_furniture if st.session_state.uploaded_furniture else None
            base_prompt = create_room_prompt(preferences, uploaded_furniture_data)
            if special_instructions:
                base_prompt += f"\n\nSpecial Instructions: {special_instructions}"
            
            # Prepare content for AI generation
            content_list = [base_prompt, original_image]
            
            # Add uploaded furniture images to the content
            if uploaded_furniture_data:
                for furniture in uploaded_furniture_data:
                    content_list.append(furniture['image'])
            
            # Generate furnished room
            response = st.session_state.client.models.generate_content(
                model=model_id,
                contents=content_list,
                config=types.GenerateContentConfig(
                    response_modalities=['Text', 'Image']
                )
            )
            
            # Display the response
            furnished_image = display_response(response)
            
            if furnished_image:
                # Save to session
                save_furnished_room(original_image, furnished_image, preferences, f"furnished_{room_type}.png", uploaded_furniture_data)
                
                st.success("Room furnished successfully!")
                
                # Show before/after comparison
                st.header("Before & After Comparison")
                
                col_before, col_after = st.columns(2)
                
                with col_before:
                    st.subheader("Before")
                    st.image(original_image, use_container_width=True)
                
                with col_after:
                    st.subheader("After")
                    st.image(furnished_image, use_container_width=True)
                
                # Show preferences used
                st.header("Design Specifications Used")
                col_spec1, col_spec2 = st.columns(2)
                
                with col_spec1:
                    st.markdown(f"**Room Type:** {room_type.title()}")
                    st.markdown(f"**Style:** {style.title()}")
                    st.markdown(f"**Color Scheme:** {color_scheme.title()}")
                
                with col_spec2:
                    st.markdown(f"**Furniture Style:** {furniture_style.title()}")
                    st.markdown(f"**Lighting:** {lighting.title()}")
                    if additional_items:
                        st.markdown(f"**Additional Items:** {', '.join(additional_items)}")
                
            else:
                st.warning("No furnished image was generated. Please try different preferences.")
                
        except Exception as e:
            st.error(f"Error furnishing room: {str(e)}")

# Process multiple style generation
if multiple_styles and uploaded_file:
    with st.spinner("AI is generating 4 different style variations... This may take a few moments."):
        try:
            # Define 4 different styles to generate
            style_variations = [
                {"name": "Modern", "style": "modern", "color": "neutral", "furniture": "contemporary"},
                {"name": "Traditional", "style": "traditional", "color": "warm", "furniture": "traditional"},
                {"name": "Minimalist", "style": "minimalist", "color": "monochrome", "furniture": "modern"},
                {"name": "Scandinavian", "style": "scandinavian", "color": "pastel", "furniture": "scandinavian"}
            ]
            
            generated_variations = []
            
            for i, variation in enumerate(style_variations):
                with st.spinner(f"Generating {variation['name']} style... ({i+1}/4)"):
                    # Create preferences for this variation
                    var_preferences = {
                        'room_type': room_type,
                        'style': variation['style'],
                        'color_scheme': variation['color'],
                        'furniture_style': variation['furniture'],
                        'lighting': lighting,
                        'additional_items': additional_items,
                        'special_instructions': special_instructions
                    }
                    
                    # Create the prompt
                    uploaded_furniture_data = st.session_state.uploaded_furniture if st.session_state.uploaded_furniture else None
                    base_prompt = create_room_prompt(var_preferences, uploaded_furniture_data)
                    if special_instructions:
                        base_prompt += f"\n\nSpecial Instructions: {special_instructions}"
                    
                    # Prepare content for AI generation
                    content_list = [base_prompt, original_image]
                    
                    # Add uploaded furniture images to the content
                    if uploaded_furniture_data:
                        for furniture in uploaded_furniture_data:
                            content_list.append(furniture['image'])
                    
                    # Generate furnished room
                    response = st.session_state.client.models.generate_content(
                        model=model_id,
                        contents=content_list,
                        config=types.GenerateContentConfig(
                            response_modalities=['Text', 'Image']
                        )
                    )
                    
                    # Extract image from response
                    furnished_image = None
                    for part in response.parts:
                        if image := part.as_image():
                            furnished_image = PILImage.open(io.BytesIO(image.image_bytes))
                            break
                    
                    if furnished_image:
                        generated_variations.append({
                            'name': variation['name'],
                            'image': furnished_image,
                            'preferences': var_preferences
                        })
            
            if generated_variations:
                st.success(f"Generated {len(generated_variations)} style variations!")
                
                # Display all variations
                st.header("Style Variations Comparison")
                
                # Show original room
                st.subheader("Original Room")
                col_orig = st.columns(1)[0]
                with col_orig:
                    st.image(original_image, caption="Original Room", use_container_width=True)
                
                # Show variations in a grid
                st.subheader("Style Variations")
                variation_cols = st.columns(2)
                
                for i, variation in enumerate(generated_variations):
                    with variation_cols[i % 2]:
                        st.image(variation['image'], caption=f"{variation['name']} Style", use_container_width=True)
                        
                        # Save each variation
                        save_furnished_room(
                            original_image, 
                            variation['image'], 
                            variation['preferences'], 
                            f"{variation['name'].lower()}_{room_type}.png", 
                            uploaded_furniture_data
                        )
                
                # Show style details
                st.subheader("Style Details")
                for variation in generated_variations:
                    with st.expander(f"{variation['name']} Style Details"):
                        prefs = variation['preferences']
                        col_detail1, col_detail2 = st.columns(2)
                        
                        with col_detail1:
                            st.markdown(f"**Style:** {prefs['style'].title()}")
                            st.markdown(f"**Color Scheme:** {prefs['color_scheme'].title()}")
                        
                        with col_detail2:
                            st.markdown(f"**Furniture Style:** {prefs['furniture_style'].title()}")
                            st.markdown(f"**Lighting:** {prefs['lighting'].title()}")
            else:
                st.warning("No style variations were generated. Please try again.")
                
        except Exception as e:
            st.error(f"Error generating style variations: {str(e)}")

# Process furniture preview
if 'preview_style' in locals() and preview_style and uploaded_file and st.session_state.uploaded_furniture:
    with st.spinner("Creating furniture preview..."):
        try:
            # Create a simple preview prompt
            preview_prompt = f"""
            Create a {room_type} in {style} style featuring the uploaded furniture items.
            Make sure the uploaded furniture is prominently displayed and well-integrated into the room design.
            The room should showcase how these specific furniture pieces look in a {style} {room_type}.
            """
            
            # Prepare content for preview
            preview_content = [preview_prompt, original_image]
            for furniture in st.session_state.uploaded_furniture:
                preview_content.append(furniture['image'])
            
            # Generate preview
            preview_response = st.session_state.client.models.generate_content(
                model=model_id,
                contents=preview_content,
                config=types.GenerateContentConfig(
                    response_modalities=['Text', 'Image']
                )
            )
            
            # Display preview
            preview_image = display_response(preview_response)
            
            if preview_image:
                st.success("Furniture preview generated!")
                st.info(f"Preview shows your furniture in a {style} {room_type}")
            else:
                st.warning("No preview was generated. Please try again.")
                
        except Exception as e:
            st.error(f"Error generating preview: {str(e)}")


# Gallery section
if st.session_state.furnished_rooms:
    st.header("Your Furnished Rooms Gallery")
    
    # Display all furnished rooms
    for i, room_data in enumerate(st.session_state.furnished_rooms):
        with st.expander(f"Room {i+1} - {room_data['preferences']['room_type'].title()} ({room_data['timestamp']})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Before")
                st.image(room_data['original'], use_container_width=True)
            
            with col2:
                st.subheader("After")
                st.image(room_data['furnished'], use_container_width=True)
            
            # Show preferences
            st.subheader("Design Preferences")
            prefs = room_data['preferences']
            col_pref1, col_pref2 = st.columns(2)
            
            with col_pref1:
                st.markdown(f"**Room Type:** {prefs['room_type'].title()}")
                st.markdown(f"**Style:** {prefs['style'].title()}")
                st.markdown(f"**Color Scheme:** {prefs['color_scheme'].title()}")
            
            with col_pref2:
                st.markdown(f"**Furniture Style:** {prefs['furniture_style'].title()}")
                st.markdown(f"**Lighting:** {prefs['lighting'].title()}")
                if prefs['additional_items']:
                    st.markdown(f"**Additional Items:** {', '.join(prefs['additional_items'])}")
            
            # Show uploaded furniture if any
            if room_data.get('uploaded_furniture'):
                st.subheader("Uploaded Furniture Used")
                for j, furniture in enumerate(room_data['uploaded_furniture']):
                    col_furn_display1, col_furn_display2 = st.columns([1, 3])
                    with col_furn_display1:
                        st.image(furniture['image'], caption=f"Item {j+1}", width=100)
                    with col_furn_display2:
                        st.markdown(f"**{furniture['description']}**")
            
            # Download buttons
            col_dl1, col_dl2 = st.columns(2)
            
            with col_dl1:
                # Download original
                img_bytes = io.BytesIO()
                room_data['original'].save(img_bytes, format='PNG')
                st.download_button(
                    label="Download Original",
                    data=img_bytes.getvalue(),
                    file_name=f"original_{room_data['filename']}",
                    mime="image/png",
                    key=f"orig_dl_{i}"
                )
            
            with col_dl2:
                # Download furnished
                img_bytes = io.BytesIO()
                room_data['furnished'].save(img_bytes, format='PNG')
                st.download_button(
                    label="Download Furnished",
                    data=img_bytes.getvalue(),
                    file_name=room_data['filename'],
                    mime="image/png",
                    key=f"furn_dl_{i}"
                )

# Tips section
with st.expander("Tips for Better Results"):
    st.markdown("""
    **For Best Results:**
    
    **Room Image Quality:**
    - Use clear, well-lit photos
    - Ensure the room is visible from a good angle
    - Avoid blurry or dark images
    
    **Design Preferences:**
    - Be specific about your style preferences
    - Consider the room's existing architecture
    - Mix and match different elements for unique looks
    
    **Lighting:**
    - Natural lighting works best for most styles
    - Consider the room's actual lighting conditions
    - Warm lighting creates cozy atmospheres
    
    **Furniture Upload:**
    - Upload clear, well-lit furniture images
    - Provide detailed descriptions for each item
    - Use the preview feature to test different styles
    - Upload multiple items to see how they work together
    
    **Furniture Selection:**
    - Choose furniture styles that complement the room's architecture
    - Consider the room's size when selecting furniture styles
    - Don't be afraid to experiment with different combinations
    - Use the furniture preview to test before final generation
    
    **Pro Tips:**
    - Try multiple variations with different preferences
    - Use the special instructions field for specific requirements
    - Save your favorite combinations for future reference
    - Upload furniture you already own to see how it fits
    - Use the preview feature to experiment with different styles
    """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #4a5568; font-size: 0.9rem;'>
    <p><strong>AI Room Furnishing Assistant</strong> | Powered by Google Gemini</p>
    <p>Built with Streamlit | <a href='https://ai.google.dev/gemini-api/docs/image-generation' target='_blank' style='color: #3182ce;'>Gemini API Documentation</a></p>
</div>
""", unsafe_allow_html=True)
