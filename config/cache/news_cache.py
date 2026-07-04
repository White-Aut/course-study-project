from typing import Any, Dict, Optional

from config.cache_conf import get_json_cache, set_cache

CATEGORIES_KEY = "news:categories"
NEWS_LIST_PREFIX = "news:list:"


async def get_cache_categories():
    return await get_json_cache(CATEGORIES_KEY)


async def set_cache_categories(data: list[Dict[str, Any]], expire: int = 7200):
    return await set_cache(CATEGORIES_KEY, data, expire)


async def get_cache_news_list(category_id: int, page: int, size: int):
    key = f"{NEWS_LIST_PREFIX}{category_id}:{page}:{size}"
    return await get_json_cache(key)


async def set_cache_news_list(category_id: int, page: int, size: int, news_list: list[Dict[str, Any]], expire: int = 1800):
    key = f"{NEWS_LIST_PREFIX}{category_id}:{page}:{size}"
    return await set_cache(key, news_list, expire)
