# Imanipulator

Imanipulator is a simple image processing application built with Tkinter. It allows users to load images, remove their backgrounds, and resize them with ease. This project was developed to assist my girlfriend, that sells at Mercado Livre Shopee and other e-commerce platforms. It served as an opportunity to learn Tkinter and enhance my portfolio.

## Features
- Load multiple images
- Preview selected images
- Remove image backgrounds using `rembg`
- Resize images while maintaining aspect ratio
- Save processed images to a user-selected directory

## Technologies Used
- Python
- Tkinter (GUI framework)
- PIL (Pillow) for image processing
- NumPy
- `rembg` for background removal

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/GustavoHSD/imanipulator.git
   cd imanipulator
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```sh
   python main.py
   ```
2. Click "Carregar imagens" to select images.
3. Choose an action:
   - "Remover fundo" to remove backgrounds.
   - "Redimensionar" to resize images.
4. Select an output directory when prompted.
5. Processed images will be saved in the chosen directory.

## Future Improvements
- Add more image editing options (e.g., cropping, filters)
- Improve UI/UX with better layout and styling
- Add drag-and-drop support for image selection

## License
This project is licensed under the MIT License.


