#AIzaSyC0mmO4MuqXmb9s1a_a4Q7kUBfXxLN6MeE
import streamlit as st
import google.generativeai as genai
import os
from PIL import Image, ImageDraw, ImageFont
import io
import base64
from datetime import datetime
import random
import requests
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="YouTube Script & Thumbnail Generator",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS
# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 4rem;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ff4b4b !important;
        color: white !important;
    }
    .info-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        color: #1e1e1e; /* Added dark text color to ensure visibility */
    }
    .result-area {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        color: #1e1e1e; /* Added dark text color to ensure visibility */
    }
    h1, h2, h3 {
        color: #1e1e1e;
    }
    .red-button {
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# App title and introduction
st.title("🎬 YouTube Script & Thumbnail Generator")
st.markdown("Generate professional YouTube scripts and eye-catching thumbnails using Gemini AI.")

# API key input
with st.expander("🔑 Configure API Key", expanded=True):
    api_key = st.text_input("Enter your Gemini API key:", type="password", 
                           help="Get your API key from https://ai.google.dev/")
    
    if api_key:
        try:
            genai.configure(api_key=api_key)
            st.success("API key configured successfully!")
        except Exception as e:
            st.error(f"Error configuring API: {e}")

# Create tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["📝 Script Generator", "🖼️ Thumbnail Creator", "ℹ️ Help"])

# Tab 1: Script Generator
with tab1:
    st.header("YouTube Script Generator")
    
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            video_topic = st.text_input("Enter your video topic:", 
                                      placeholder="e.g., How to start investing in stocks for beginners")
            
            video_length = st.slider("Select approximate video length (minutes):", 
                                   min_value=2, max_value=30, value=10, step=1)
            
            audience = st.selectbox("Select your target audience:", 
                                  ["Beginners", "Intermediate", "Advanced", "General audience"])
            
            tone_options = ["Educational", "Entertaining", "Inspirational", "Conversational", 
                          "Professional", "Enthusiastic", "Calm & Relaxed"]
            tone = st.selectbox("Select the tone for your script:", tone_options)
            
            include_options = st.multiselect("Include in your script:", 
                                          ["Hook/Attention grabber", "Introduction", "Main points", 
                                           "Examples/Case studies", "Call to action", "Outro"],
                                          default=["Hook/Attention grabber", "Introduction", "Main points", "Call to action", "Outro"])
            
        with col2:
            st.markdown("### Advanced Options")
            
            script_style = st.radio("Script Style:", 
                                  ["Detailed (full script)", "Bullet points (outline)"])
            
            additional_notes = st.text_area("Additional notes or instructions:", 
                                         placeholder="Any specific points to cover or style preferences...")
    
    # Generate script button
    if st.button("🚀 Generate Script", type="primary", use_container_width=True):
        if not api_key:
            st.error("Please enter your Gemini API key first.")
        elif not video_topic:
            st.error("Please enter a video topic.")
        else:
            with st.spinner("Generating your YouTube script... This may take a moment."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-pro')
                    
                    # Different prompts based on script style
                    if script_style == "Detailed (full script)":
                        prompt = f"""
                        Write a COMPLETE, DETAILED YouTube script about: {video_topic}
                        
                        Script details:
                        - Target audience: {audience}
                        - Approximate video length: {video_length} minutes
                        - Tone: {tone}
                        - Include: {', '.join(include_options)}
                        
                        Additional notes: {additional_notes}
                        
                        IMPORTANT INSTRUCTIONS:
                        1. This MUST BE A FULL SCRIPT with complete sentences and paragraphs, NOT bullet points.
                        2. Write exactly as the YouTuber would speak, with natural language and complete sentences.
                        3. Include dialogue with actual words to be spoken.
                        4. Use proper paragraphs and formatting, NOT bullet points.
                        5. Format as a speaking script with clear sections like INTRO, MAIN CONTENT, OUTRO.
                        6. For a {video_length} minute video, create an appropriate length script.
                        7. Include natural transitions and engagement points.
                        8. DO NOT use bullet points anywhere in the script.
                        9. Structure as full paragraphs of natural speech.

                        Format this as a complete speaking script that a YouTuber can read directly to camera.
                        """
                    else:
                        prompt = f"""
                        Create a BULLET POINT OUTLINE for a YouTube video about: {video_topic}
                        
                        Script details:
                        - Target audience: {audience}
                        - Approximate video length: {video_length} minutes
                        - Tone: {tone}
                        - Include: {', '.join(include_options)}
                        
                        Additional notes: {additional_notes}
                        
                        IMPORTANT INSTRUCTIONS:
                        1. Format as a hierarchical bullet point outline with main points and sub-points.
                        2. Use bullet points, numbering, and indentation for clear structure.
                        3. Include key talking points only, not full sentences for everything.
                        4. Organize into clear sections like INTRO, MAIN CONTENT, OUTRO.
                        5. For a {video_length} minute video, include appropriate number of points.
                        
                        Format this as a structured outline that a YouTuber can use as speaking notes.
                        """
                    
                    generation_config = {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "top_k": 40,
                        "max_output_tokens": 8192,
                    }
                    
                    response = model.generate_content(
                        prompt,
                        generation_config=generation_config
                    )
                    
                    script_result = response.text
                    
                    st.markdown("### 📝 Your YouTube Script:")
                    st.markdown(f'<div class="result-area">{script_result}</div>', unsafe_allow_html=True)
                    
                    # Add download button for the script
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"youtube_script_{timestamp}.txt"
                    
                    st.download_button(
                        label="📥 Download Script",
                        data=script_result,
                        file_name=filename,
                        mime="text/plain",
                    )
                
                except Exception as e:
                    st.error(f"Error generating script: {e}")

# Function to search and get image URLs from Unsplash
def search_unsplash_images(query, count=5):
    try:
        # Unsplash API endpoint for searching photos (using demo access key)
        url = f"https://api.unsplash.com/search/photos?query={query}&per_page={count}"
        headers = {
            "Authorization": "Client-ID YOUR_UNSPLASH_API_KEY"  # Replace with your Unsplash API key
        }
        
        # For demo purposes, use a sample of fixed URLs if API key is not set
        sample_urls = [
            "https://images.unsplash.com/photo-1611162616305-c69b3fa7fbe0?w=800&auto=format&fit=crop",  # YouTube/video related
            "https://images.unsplash.com/photo-1598550476439-6847785fcea6?w=800&auto=format&fit=crop",  # Camera/filming
            "https://images.unsplash.com/photo-1626379953822-baec19c3accd?w=800&auto=format&fit=crop",  # Success/achievement
            "https://images.unsplash.com/photo-1611162616475-46b635cb6868?w=800&auto=format&fit=crop",  # Technology
            "https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?w=800&auto=format&fit=crop",  # Abstract background
        ]
        
        # Check if "YOUR_UNSPLASH_API_KEY" is still in the headers
        if "YOUR_UNSPLASH_API_KEY" in headers["Authorization"]:
            return sample_urls
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if "results" in data:
            return [photo["urls"]["regular"] for photo in data["results"]]
        else:
            return sample_urls
    except:
        # Fallback to sample URLs if there's an error
        return sample_urls

# Function to create a thumbnail with a background image
def create_thumbnail_with_image(image_url, title, subtitle, style, color_scheme, text_position, include_border, include_emoji=False, emoji=""):
    width, height = 1280, 720
    
    # Define color schemes
    color_schemes = {
        "Red & Black": ["#ff0000", "#000000", "#ffffff"],
        "Blue & White": ["#0066cc", "#ffffff", "#003366"],
        "Green & Yellow": ["#33cc33", "#ffff00", "#006600"],
        "Orange & Purple": ["#ff9933", "#9966cc", "#ffffff"],
        "Black & Gold": ["#000000", "#ffd700", "#ffffff"],
        "Pink & Teal": ["#ff66cc", "#00cccc", "#ffffff"],
        "Grayscale": ["#333333", "#dddddd", "#ffffff"]
    }
    
    colors = color_schemes.get(color_scheme, ["#ff0000", "#000000", "#ffffff"])
    
    try:
        # Load and resize background image
        response = requests.get(image_url)
        bg_image = Image.open(BytesIO(response.content))
        bg_image = bg_image.resize((width, height), Image.LANCZOS)
        
        # Apply overlay based on style
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        if style == "Modern & Bold":
            # Semi-transparent overlay
            overlay_draw.rectangle([0, 0, width, height], fill=(0, 0, 0, 180))
            # Add diagonal element
            overlay_draw.polygon([(0, 0), (width, 0), (width, height//2)], fill=(int(colors[1][1:3], 16), int(colors[1][3:5], 16), int(colors[1][5:7], 16), 150))
            
        elif style == "Minimalist":
            # Full dark overlay with higher transparency
            overlay_draw.rectangle([0, 0, width, height], fill=(0, 0, 0, 120))
            # Add border
            padding = 40
            overlay_draw.rectangle([padding, padding, width-padding, height-padding], 
                                  outline=(int(colors[1][1:3], 16), int(colors[1][3:5], 16), int(colors[1][5:7], 16), 255), width=5)
            
        elif style == "Vibrant & Colorful":
            # Colored overlay
            overlay_draw.rectangle([0, 0, width, height], fill=(int(colors[0][1:3], 16), int(colors[0][3:5], 16), int(colors[0][5:7], 16), 130))
            # Add colorful elements
            for i in range(5):
                size = random.randint(100, 200)
                x = random.randint(0, width)
                y = random.randint(0, height)
                overlay_draw.ellipse([x-size, y-size, x+size, y+size], 
                                    fill=(int(colors[1][1:3], 16), int(colors[1][3:5], 16), int(colors[1][5:7], 16), 130))
        
        elif style == "Professional":
            # Dark overlay
            overlay_draw.rectangle([0, 0, width, height], fill=(0, 0, 0, 150))
            # Add header and footer bars
            overlay_draw.rectangle([0, 0, width, height//6], fill=(int(colors[1][1:3], 16), int(colors[1][3:5], 16), int(colors[1][5:7], 16), 230))
            overlay_draw.rectangle([0, height-height//6, width, height], fill=(int(colors[1][1:3], 16), int(colors[1][3:5], 16), int(colors[1][5:7], 16), 230))
            
        elif style == "Dramatic":
            # Darker overlay for drama
            overlay_draw.rectangle([0, 0, width, height], fill=(0, 0, 0, 180))
            # Add dramatic vignette effect
            for i in range(10):
                radius = 300 - i*25
                alpha = 130 - i*10
                if alpha > 0:
                    overlay_draw.ellipse([width//2-radius, height//2-radius, width//2+radius, height//2+radius], 
                                        fill=(0, 0, 0, 0), outline=(0, 0, 0, alpha), width=20)
            
        elif style == "Tech/Gaming":
            # Semi-transparent overlay
            overlay_draw.rectangle([0, 0, width, height], fill=(0, 0, 0, 170))
            # Add tech frame
            overlay_draw.rectangle([20, 20, width-20, height-20], 
                                  outline=(int(colors[1][1:3], 16), int(colors[1][3:5], 16), int(colors[1][5:7], 16), 255), width=10)
            overlay_draw.rectangle([60, 60, width-60, height-60], 
                                  outline=(int(colors[2][1:3], 16), int(colors[2][3:5], 16), int(colors[2][5:7], 16), 255), width=5)
            
        elif style == "Tutorial Style":
            # Light overlay
            overlay_draw.rectangle([0, 0, width, height], fill=(255, 255, 255, 140))
            # Add darker rectangle for text
            if text_position == "Top":
                overlay_draw.rectangle([0, 0, width, height//3], fill=(0, 0, 0, 170))
            elif text_position == "Center":
                overlay_draw.rectangle([0, height//3, width, 2*height//3], fill=(0, 0, 0, 170))
            else:  # Bottom
                overlay_draw.rectangle([0, 2*height//3, width, height], fill=(0, 0, 0, 170))
                
            # Add step indicators
            for i in range(3):
                overlay_draw.ellipse([50+i*150, height-100, 120+i*150, height-30], 
                                    fill=(int(colors[1][1:3], 16), int(colors[1][3:5], 16), int(colors[1][5:7], 16), 230))
        
        # Combine the background image with overlay
        combined_img = Image.alpha_composite(bg_image.convert('RGBA'), overlay)
        img = combined_img.convert('RGB')
        draw = ImageDraw.Draw(img)
            
        # Add border if selected
        if include_border:
            draw.rectangle([0, 0, width-1, height-1], outline=colors[1], width=10)
        
        # Add title text
        try:
            # Try to load common fonts
            font_size = 80
            title_font = ImageFont.truetype("arial.ttf", font_size)
            subtitle_font = ImageFont.truetype("arial.ttf", 50)
        except IOError:
            try:
                # Try another common font
                title_font = ImageFont.truetype("DejaVuSans.ttf", font_size)
                subtitle_font = ImageFont.truetype("DejaVuSans.ttf", 50)
            except IOError:
                try:
                    # Try another common font path
                    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
                    subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 50)
                except IOError:
                    # Use default font if custom font fails
                    title_font = ImageFont.load_default()
                    subtitle_font = ImageFont.load_default()
        
        # Prepare title text with emoji if selected
        if include_emoji and emoji:
            title_text = f"{emoji} {title} {emoji}"
        else:
            title_text = title
        
        # Calculate text position
        # First check if draw has textlength method
        try:
            title_width = draw.textlength(title_text, font=title_font)
        except AttributeError:
            # For older PIL versions
            title_width = title_font.getsize(title_text)[0]
        
        title_x = (width - title_width) // 2
        
        if text_position == "Top":
            title_y = 100
        elif text_position == "Center":
            title_y = (height - 100) // 2
        else:  # Bottom
            title_y = height - 200
        
        # Draw text shadow for better readability
        draw.text((title_x+5, title_y+5), title_text, font=title_font, fill="#000000")
        # Draw main text
        draw.text((title_x, title_y), title_text, font=title_font, fill=colors[2])
        
        # Add subtitle if provided
        if subtitle:
            try:
                subtitle_width = draw.textlength(subtitle, font=subtitle_font)
            except AttributeError:
                # For older PIL versions
                subtitle_width = subtitle_font.getsize(subtitle)[0]
                
            subtitle_x = (width - subtitle_width) // 2
            subtitle_y = title_y + 100
            
            # Draw subtitle shadow
            draw.text((subtitle_x+3, subtitle_y+3), subtitle, font=subtitle_font, fill="#000000")
            # Draw subtitle
            draw.text((subtitle_x, subtitle_y), subtitle, font=subtitle_font, fill=colors[2])
        
        # Convert to bytes for display
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return buf.getvalue()
    
    except Exception as e:
        # If there's an error with the image, create a basic thumbnail
        st.error(f"Error processing image: {e}. Creating basic thumbnail instead.")
        
        # Create basic thumbnail
        img = Image.new('RGB', (width, height), colors[0])
        draw = ImageDraw.Draw(img)
        
        # Add basic styling
        if include_border:
            draw.rectangle([0, 0, width-1, height-1], outline=colors[1], width=10)
        
        # Add title with default font
        default_font = ImageFont.load_default()
        
        # Add title text
        title_x = width // 2 - (len(title) * 5)  # rough estimate for centering
        
        if text_position == "Top":
            title_y = 100
        elif text_position == "Center":
            title_y = height // 2
        else:  # Bottom
            title_y = height - 200
        
        # Draw text
        draw.text((title_x, title_y), title, font=default_font, fill=colors[2])
        
        # Add subtitle if provided
        if subtitle:
            subtitle_x = width // 2 - (len(subtitle) * 5)  # rough estimate for centering
            subtitle_y = title_y + 50
            draw.text((subtitle_x, subtitle_y), subtitle, font=default_font, fill=colors[2])
        
        # Convert to bytes for display
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return buf.getvalue()

# Tab 2: Thumbnail Creator
with tab2:
    st.header("YouTube Thumbnail Creator")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        thumbnail_title = st.text_input("Thumbnail Title:", 
                                     placeholder="Enter eye-catching title (keep it short)")
        
        thumbnail_subtitle = st.text_input("Subtitle/Tagline (optional):", 
                                        placeholder="Optional supporting text")
        
        style_options = ["Modern & Bold", "Minimalist", "Vibrant & Colorful", 
                       "Professional", "Dramatic", "Tech/Gaming", "Tutorial Style"]
        thumbnail_style = st.selectbox("Thumbnail Style:", style_options)
        
        color_scheme = st.selectbox("Color Scheme:", [
            "Red & Black", "Blue & White", "Green & Yellow", 
            "Orange & Purple", "Black & Gold", "Pink & Teal", "Grayscale"
        ])
        
        # Background image search
        st.subheader("Background Image")
        background_query = st.text_input("Search for background image:", 
                                       placeholder="e.g., technology, nature, business")
        
    with col2:
        st.markdown("### Thumbnail Size")
        st.info("YouTube recommended: 1280 × 720 pixels (16:9)")
        
        # Custom option for thumbnail generation
        st.markdown("### Text Position")
        text_position = st.radio("Main Title Position:", ["Top", "Center", "Bottom"])
        
        include_border = st.checkbox("Add border", value=True)
        include_emoji = st.checkbox("Include emoji in title", value=False)
        
        if include_emoji:
            emoji_options = ["🔥", "✅", "💰", "🚀", "⚡", "💯", "🎯", "❓", "⭐", "🔴", "✨"]
            selected_emoji = st.selectbox("Select emoji:", emoji_options)
    
    # Search for images
    if background_query:
        st.subheader("Select Background Image")
        image_urls = search_unsplash_images(background_query)
        selected_image = None
        
        # Display images in a grid
        cols = st.columns(3)
        for i, url in enumerate(image_urls[:6]):  # Limit to 6 images
            with cols[i % 3]:
                st.image(url, width=200)
                if st.button(f"Select Image {i+1}", key=f"img_{i}"):
                    selected_image = url
                    st.session_state.selected_image = url
        
        # If image was previously selected, keep it
        if 'selected_image' in st.session_state:
            if selected_image is None:  # Only update if a new image wasn't just selected
                selected_image = st.session_state.selected_image
            
            st.success(f"Background image selected! Generate your thumbnail now.")
    
    # Generate thumbnail button
    if st.button("🖼️ Generate Thumbnail", type="primary", use_container_width=True):
        if not thumbnail_title:
            st.error("Please enter a thumbnail title.")
        else:
            with st.spinner("Generating your thumbnail..."):
                try:
                    # Get selected image or use default
                    selected_image = st.session_state.get('selected_image', None)
                    
                    if selected_image:
                        # Generate thumbnail with background image
                        emoji = selected_emoji if include_emoji else ""
                        byte_im = create_thumbnail_with_image(
                            selected_image,
                            thumbnail_title, 
                            thumbnail_subtitle, 
                            thumbnail_style, 
                            color_scheme, 
                            text_position, 
                            include_border, 
                            include_emoji, 
                            emoji
                        )
                    else:
                        st.error("Please select a background image first.")
                        st.stop()
                    
                    # Display the image
                    st.markdown("### 🖼️ Your YouTube Thumbnail:")
                    st.image(byte_im, caption="Generated Thumbnail", use_column_width=True)
                    
                    # Add download button
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    st.download_button(
                        label="📥 Download Thumbnail",
                        data=byte_im,
                        file_name=f"youtube_thumbnail_{timestamp}.png",
                        mime="image/png",
                    )
                    
                    # Also generate AI thumbnail suggestion if Gemini API is available
                    if api_key:
                        st.markdown("### 💡 Thumbnail Improvement Suggestions")
                        
                        with st.spinner("Getting AI suggestions for your thumbnail..."):
                            model = genai.GenerativeModel('gemini-1.5-pro')
                            
                            prompt = f"""
                            Provide 3-5 specific suggestions to improve a YouTube thumbnail with these details:
                            
                            Title: {thumbnail_title}
                            Style: {thumbnail_style}
                            Color Scheme: {color_scheme}
                            
                            Focus on specific, actionable advice for creating a high-CTR thumbnail that stands out.
                            Include tips about composition, text placement, visual elements, and what top YouTubers 
                            do for this type of content.
                            """
                            
                            response = model.generate_content(prompt)
                            suggestions = response.text
                            
                            st.markdown(f'<div class="info-box">{suggestions}</div>', unsafe_allow_html=True)
                    else:
                        st.info("Add your Gemini API key to get AI suggestions for improving your thumbnail.")
                        
                except Exception as e:
                    st.error(f"Error generating thumbnail: {e}")
                    import traceback
                    st.error(traceback.format_exc())

# Tab 3: Help section
with tab3:
    st.header("How to Use This App")
    
    st.markdown("""
    ### 📝 Script Generator
    
    1. **Enter your API key** - You'll need a Google Gemini API key
    2. **Enter your video topic** - Be as specific as possible
    3. **Adjust settings** - Set video length, tone, and audience
    4. **Generate script** - Click the generate button to create your script
    5. **Download** - Save your script as a text file
    
    ### 🖼️ Thumbnail Creator
    
    1. **Enter thumbnail text** - Keep it short and attention-grabbing
    2. **Choose style** - Select a style that matches your channel aesthetic
    3. **Search for background images** - Find the perfect image for your thumbnail
    4. **Select a background image** - Choose one of the search results
    5. **Adjust settings** - Customize colors, positions, and elements
    6. **Generate thumbnail** - Create your custom thumbnail
    7. **Download** - Save as PNG to upload to YouTube
    
    ### 📚 Tips for Great YouTube Content
    
    - **Titles matter** - Use numbers, emotions, or questions to attract viewers
    - **First 15 seconds** - Hook viewers immediately with a strong intro
    - **Clear value proposition** - Tell viewers what they'll learn or gain
    - **Call to action** - Always remind viewers to like, subscribe, and comment
    - **Thumbnail best practices** - Use contrasting colors, readable text, and emotional triggers
    
    ### 🔑 Getting Your API Key
    
    1. Visit [Google AI Studio](https://ai.google.dev/)
    2. Create an account or sign in
    3. Navigate to API keys section
    4. Create a new API key
    5. Copy and paste the key into this app
    """)
    
    st.markdown("""
    ### 📈 Maximizing Your YouTube Success
    
    For the best results with your YouTube content:
    
    - **Consistency is key** - Maintain a regular upload schedule
    - **Analyze performance** - Check YouTube analytics to see what works
    - **A/B test thumbnails** - Try different styles to see what gets more clicks
    - **Optimize for search** - Use relevant keywords in titles, descriptions and tags
    - **Engage with comments** - Build community by responding to viewers
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center;">
        <p>Built with ❤️ using Streamlit and Gemini AI</p>
        <p><small>Remember to use your own API key • Not affiliated with YouTube or Google</small></p>
    </div>
    """,
    unsafe_allow_html=True
)
