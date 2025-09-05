#!/usr/bin/env python3
"""
Script de test pour différentes solutions d'emoji
Teste: NotoColorEmoji, Pilmoji
"""

import os
import sys
import django

sys.path.append('/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
django.setup()

from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from pilmoji import Pilmoji


base_dir = settings.BASE_DIR
test_emoji = '🔧'
base_font = "Poppins-Regular.ttf"
noto_font = "NotoColorEmoji.ttf"
base_font_path = base_dir / 'tournesol/resources' / base_font
noto_font_path = base_dir / 'tournesol/resources' / noto_font
output_dir = '/backend/scripts/tmp/'

def create_test_image(title):
    img = Image.new('RGB', (500, 80), 'white')
    draw = ImageDraw.Draw(img)

    font_small = ImageFont.truetype(str(base_font_path), 12)
    draw.text((10, 5), title, font=font_small, fill='gray')
    
    return img, draw

def test_noto_color_emoji():
    img, draw = create_test_image("Test 1: NotoColorEmoji.ttf")
    
    try:
        # https://github.com/python-pillow/Pillow/issues/3346#issuecomment-612139601
        emoji_font = ImageFont.truetype(str(noto_font_path), 109) # Bitmap font, lower size = pixel error

        # Créer une image temporaire pour l'emoji
        emoji_img = Image.new('RGBA', (120, 120), (255, 255, 255, 0))
        emoji_draw = ImageDraw.Draw(emoji_img)
        emoji_draw.text((5, 5), test_emoji, font=emoji_font, embedded_color=True)

        # Redimensionner à 30px
        emoji_resized = emoji_img.resize((30, 30), Image.Resampling.LANCZOS)
        
        # Coller sur l'image principale
        img.paste(emoji_resized, (10, 25), emoji_resized)
        
        text_font = ImageFont.truetype(str(base_font_path), 20)
        draw.text((50, 30), "Noto Color Emoji", font=text_font, fill='black')

        img.save(output_dir+'test1_noto_color_emoji.png')

    except Exception as e:
        print(f"NotoColorEmoji: FAILED - {e}")
        

def test_pilmoji():
    img, _ = create_test_image("Test 4: Pilmoji")

    text_font = ImageFont.truetype(str(base_font_path), 20)
        
    with Pilmoji(img) as pilmoji:
        pilmoji.text((50, 30), f"{test_emoji} Pilmoji emoji", font=text_font, fill='black')

    img.save(output_dir+'test2_pilmoji.png')

test_noto_color_emoji()
test_pilmoji()

