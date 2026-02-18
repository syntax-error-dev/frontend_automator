import pandas as pd
import os
import logging
from config import FILE_PROJECTS, FILE_CURRENCIES, DEFAULT_CURRENCY

logger = logging.getLogger(__name__)

def load_projects():
    try:
        # Пути теперь относительные для удобства
        df_curr = pd.read_excel(os.path.join("data", FILE_CURRENCIES), header=None)
        currency_map = {str(row[0]).strip(): str(row[2]).strip()
                        for _, row in df_curr.iterrows() if pd.notna(row[0])}

        df_proj = pd.read_excel(os.path.join("data", FILE_PROJECTS), header=None)
        final_list = []
        for _, row in df_proj.iterrows():
            url = str(row[0]).strip()
            if url.startswith("http"):
                country = str(row[2]).strip() if pd.notna(row[2]) else "Unknown"
                final_list.append({
                    "url": url,
                    "curr": currency_map.get(country, DEFAULT_CURRENCY)
                })
        return final_list
    except Exception as e:
        logger.error(f"Ошибка чтения данных: {e}")
        return []