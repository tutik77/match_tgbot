import os
import aiohttp
from openai import AsyncOpenAI
from settings import settings

os.environ['OPENAI_API_KEY'] = settings.openai_api_key
openai_api_key = settings.openai_api_key


class GPTService:
    def __init__(self):
        self.client = AsyncOpenAI()

    async def initialize_assistant(self):
        self.assistant = await self.client.beta.assistants.create(
            name="Помощник для выделения ключевый слов из текста.",
            instructions="Из получаемого текста ты должен выделять ключевые слова, по которым можно будет искать профили в базе данных.",
            model="gpt-4o",
        )
        self.thread = await self.client.beta.threads.create()

    async def get_keywords_from_description(self, description):
        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{'role': 'user', 'content': f"Из описания профиля пользователя: '{description}', выдели ключевые слова, фразы, обобщения интересов, параметры внешности, черты характера. Форматировать не нужно, просто перечисляй все ключевые слова, которые в наибольшей степени описывают челоевека."}],
        )
        return response.choices[0].message.content

    async def get_keywords_from_query(self, query):
        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{'role': 'user', 'content': f"Из полученного запроса: '{query}' помоги выделить ключевые слова для поиска профилей пользователей по интересам, занятиям, параметрам внешности. Нужно получить наиболее релевантные слова, их синонимы, различные формулировки, которые люди могут использовать для описания себя, чтобы потом по этим словам искать профили в базе данных. В ответе укажи ТОЛЬКО сами слова, перечисленные через запятую."}]
        )
        return response.choices[0].message.content.split(", ")

    async def compare_query_with_description(self, query: str, description: str):
        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{'role': 'user', 'content': f"Сравни запрос '{query}' с описанием '{description}'."}]
        )
        return response.choices[0].message.content


class RegisterService:
    def __init__(self):
        self.url = "http://django:8000/api/users/"

    async def get_user_by_tg_id(self, user_id):
        url = f"{self.url}{user_id}/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 404:
                    return None
                return await response.json()

    async def create_user(self, user_data: dict):
        user_data["description_keywords"] = await gpt_service.get_keywords_from_description(user_data["description"])
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=user_data) as response:
                return await response.json()


class SearchService:
    def __init__(self):
        self.url = "http://django:8000/api/"

    async def search_users_by_keywords(self, keywords: list):
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{self.url}users/search/', json={"keywords": keywords}) as response:
                if response.status == 404:
                    return None
                return await response.json()

    async def add_query_to_db(self, query_text: str, user_id: int):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}user_queries/", json={"query_text": query_text, "user_id": user_id}) as response:
                return await response.json()


gpt_service = GPTService()
register_service = RegisterService()
search_service = SearchService()