#  AI Room Furnishing Assistant

An intelligent web application that transforms empty or partially furnished rooms into beautifully designed spaces using AI-powered furniture integration. Built with Streamlit and powered by Google's Gemini AI model.

![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![Google AI](https://img.shields.io/badge/google-ai-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

##  Features

###  **Smart Room Design**
- **AI-Powered Furnishing**: Transform empty rooms into professionally designed spaces
- **Multiple Style Options**: Choose from 10+ design styles (Modern, Traditional, Scandinavian, etc.)
- **Customizable Preferences**: Fine-tune room type, color schemes, furniture styles, and lighting
- **Style Variations**: Generate up to 4 different style variations for comparison

###  **Furniture Integration**
- **Upload Custom Furniture**: Add your own furniture and accessory images
- **Smart Integration**: AI seamlessly integrates uploaded items into room designs
- **Furniture Preview**: Preview how your furniture looks in different styles
- **Detailed Descriptions**: Provide context for each furniture item

###  **Visual Experience**
- **Before/After Comparison**: Side-by-side comparison of original and furnished rooms
- **High-Quality Images**: Professional-grade room visualizations
- **Interactive Gallery**: Save and manage all your furnished room designs
- **Download Options**: Download both original and furnished room images

###  **User-Friendly Interface**
- **Intuitive Design**: Clean, modern interface with professional styling
- **Real-time Processing**: Live progress indicators and status updates
- **Responsive Layout**: Works seamlessly on different screen sizes
- **Session Management**: Maintains your work across browser sessions

##  Quick Start

### Prerequisites
- Python 3.11 or higher
- Google AI API key ([Get one here](https://aistudio.google.com/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-room-furnishing-assistant.git
   cd ai-room-furnishing-assistant
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements_room_furnishing.txt
   ```

4. **Run the application**
   ```bash
   streamlit run room_furnishing_app.py
   ```

5. **Open your browser**
   - Navigate to `http://localhost:8501`
   - Enter your Google AI API key in the sidebar
   - Start furnishing rooms!

##  Requirements

- **streamlit** >= 1.28.0 - Web application framework
- **google-genai** >= 1.32.0 - Google AI SDK for Gemini integration
- **Pillow** >= 10.0.0 - Image processing library

##  How to Use

### 1. **Upload Room Image**
- Upload a clear image of an empty or partially furnished room
- Supported formats: PNG, JPG, JPEG
- Ensure good lighting and clear visibility of the space

### 2. **Set Design Preferences**
- **Room Type**: Choose from living room, bedroom, dining room, kitchen, office, etc.
- **Design Style**: Select from modern, minimalist, traditional, contemporary, etc.
- **Color Scheme**: Pick neutral, warm, cool, monochrome, pastel, bold, etc.
- **Furniture Style**: Choose contemporary, vintage, modern, traditional, etc.
- **Lighting**: Select natural, warm, cool, ambient, dramatic, etc.
- **Additional Items**: Add plants, artwork, rugs, cushions, books, etc.

### 3. **Upload Custom Furniture (Optional)**
- Upload images of specific furniture or accessories you want to include
- Provide detailed descriptions for each item
- Use the preview feature to see how they look in different styles

### 4. **Generate Designs**
- **Single Style**: Generate one design with your preferences
- **Multiple Styles**: Generate 4 different style variations
- **Furniture Preview**: Preview your uploaded furniture in the room

### 5. **Review and Download**
- Compare before and after images
- View design specifications used
- Download both original and furnished room images
- Save designs to your gallery for future reference

##  Supported Styles

| Style | Description | Best For |
|-------|-------------|----------|
| **Modern** | Clean lines, minimal clutter | Contemporary homes |
| **Minimalist** | Simple, uncluttered spaces | Zen-like environments |
| **Traditional** | Classic, timeless designs | Formal living spaces |
| **Contemporary** | Current trends, eclectic mix | Versatile applications |
| **Scandinavian** | Light, airy, functional | Nordic-inspired homes |
| **Industrial** | Raw materials, exposed elements | Urban lofts |
| **Bohemian** | Eclectic, artistic, free-spirited | Creative spaces |
| **Rustic** | Natural materials, cozy feel | Country homes |
| **Mid-Century Modern** | 1950s-60s inspired | Retro enthusiasts |
| **Art Deco** | Geometric patterns, luxury | Glamorous spaces |

## 🛠 Configuration

### API Key Setup
1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Create a new API key
3. Enter the key in the application sidebar
4. The key is stored securely in your session

### Model Selection
- Currently supports **Gemini 2.5 Flash Image Preview**
- Optimized for image generation and text processing
- Fast response times with high-quality results

##  Project Structure

```
ai-room-furnishing-assistant/
├── room_furnishing_app.py          # Main Streamlit application
├── requirements_room_furnishing.txt # Python dependencies
├── README.md                       # Project documentation
└── venv/                          # Virtual environment (created locally)
```

##  Advanced Features

### Custom Furniture Integration
- Upload multiple furniture items
- Provide detailed descriptions for better AI understanding
- Preview how furniture looks in different room styles
- AI automatically adjusts room design to complement your furniture

### Style Variations
- Generate multiple design options simultaneously
- Compare different approaches to the same space
- Save all variations for future reference
- Mix and match elements from different styles

### Session Management
- All generated rooms are saved in your session
- Access your gallery anytime during the session
- Download individual images or entire collections
- Maintains design preferences across generations

##  Tips for Best Results

### **Image Quality**
- Use clear, well-lit photos
- Ensure good visibility of the entire room
- Avoid blurry or dark images
- Capture from a good viewing angle

### **Design Preferences**
- Be specific about your style preferences
- Consider the room's existing architecture
- Mix and match different elements for unique looks
- Use the special instructions field for specific requirements

### **Furniture Upload**
- Upload clear, well-lit furniture images
- Provide detailed descriptions for each item
- Use the preview feature to test different styles
- Upload multiple items to see how they work together

### **Pro Tips**
- Try multiple variations with different preferences
- Use the special instructions field for specific requirements
- Save your favorite combinations for future reference
- Upload furniture you already own to see how it fits
- Use the preview feature to experiment with different styles

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Google Gemini AI** - For providing the powerful AI model
- **Streamlit** - For the excellent web application framework
- **Pillow** - For robust image processing capabilities
- **Open Source Community** - For inspiration and support



## 🔮 Future Enhancements

- [ ] 3D room visualization
- [ ] Virtual reality integration
- [ ] Furniture shopping integration
- [ ] Room measurement tools
- [ ] Collaborative design features
- [ ] Mobile app version
- [ ] Advanced lighting simulation
- [ ] Material texture options

---

**Built with ❤️ using Streamlit and Google Gemini AI**

*Transform your spaces with the power of artificial intelligence!*

