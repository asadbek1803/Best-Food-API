from rest_framework import serializers
import requests
import logging
import re

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        self.api_key = "f22b4ac2-f4e4-401c-ba01-1687679f38e3:fx"  # DeepL API kalitingizni shu yerga qo'ying
        self.base_url = "https://api-free.deepl.com/v2/translate"  # Free API uchun
        
    # def clean_text(self, text):
    #     """Matnni tarjimaga mos shaklda tozalash (emoji va maxsus belgilarni olib tashlash)"""
    #     return re.sub(r'[^\w\s]', '', text)  # Faqat harflar va bo‘sh joylarni qoldiramiz


    def translate_text(self, text: str, lang: str = "uz") -> str:
        """Matnni berilgan tilga tarjima qilish"""
        if not text:
            return text

        text = re.sub(r'[^\w\s]', '', text)  # ✅ Tarjimadan oldin tozalash

        try:
            target_lang = {
                "eng": "EN-US",
                "en": "EN-US",
                "ru": "RU",
                "rus": "RU",
                "uz": "UZ"
            }.get(lang.lower())

            if not target_lang:
                logger.warning(f"Unsupported language: {lang}")
                return text

            response = requests.post(
                self.base_url,
                headers={"Authorization": f"DeepL-Auth-Key {self.api_key}"},
                data={"text": text, "target_lang": target_lang},
            )
            response.raise_for_status()

            result = response.json()["translations"][0]["text"]
            print(f"✅ TARJIMA NATIJASI: {result}")

            return result

        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            return text
        
    