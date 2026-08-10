import logging
from datetime import datetime
import requests
from decimal import Decimal
from django.core.cache import cache
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

def get_usd_to_kzt_rate():
    cached = cache.get('usd_kzt_rate')
    if cached:
        return cached
    
    # Форматируем текущую дату в ДД.ММ.ГГГГ
    formatted_date = datetime.now().strftime('%d.%m.%Y')
    url = f'https://nationalbank.kz/rss/get_rates.cfm?fdate={formatted_date}'
    
    try:
        # verify=False отключает строгую проверку SSL (частая проблема с гос. сайтами РК)
        response = requests.get(url, timeout=5, verify=False)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        for item in root.findall('.//item'):
            if item.find('title').text == 'USD':
                rate = Decimal(item.find('description').text)
                cache.set('usd_kzt_rate', rate, 60 * 60)  # кэш 1 час
                return rate
                
    except Exception as e:
        # Логируем реальную ошибку, чтобы видеть её в консоли/логах
        logger.error(f"Ошибка при получении курса валют: {e}")
    
    return Decimal('460')  # fallback