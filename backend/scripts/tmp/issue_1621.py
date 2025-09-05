import os
import sys
import django

sys.path.append('/backend')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
django.setup()

from PIL import Image, ImageDraw, ImageFont
from django.conf import settings

# Test the current production method that causes the emoji issue
base_dir = settings.BASE_DIR

title_font = ImageFont.truetype(str(base_dir / 'tournesol/resources/Poppins-Medium.ttf'), 20)

img = Image.new('RGB', (400, 100), 'white')
draw = ImageDraw.Draw(img)

test_text_with_emoji = '🔧 Emoji in the previews title reproduction issues #1621'

try:
    draw.text((10, 10), test_text_with_emoji, font=title_font, fill='black') 
    print("Text with emoji rendered successfully")
except Exception as e:
    print(f"Error rendering text with emoji: {e}")

img.save('/backend/scripts/previews/test_emoji_rendering.png')