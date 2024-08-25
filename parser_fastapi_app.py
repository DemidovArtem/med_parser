import importlib
import os

from fastapi import FastAPI
from fastapi.security import HTTPBearer

app = FastAPI(debug=True)

SERVICE_ACCESS_TOKEN = os.environ.get('SERVICE_ACCESS_TOKEN')
security = HTTPBearer()


async def get_data_from_module(module, url: str):
    module = importlib.import_module(module)
    await module.add_to_db(module.analysis_data(url), 'analyzes')
    await module.add_to_db(module.address_data(url), 'addresses')


async def parse_url(url: str):
    for module_name in [
        'BulygaEkaterina.Parse',
        'Lyusin_Dmitry.Parsing',
        'ShevchenkoSemyon.parser',
        'TikhonovaMarina.lab4u'
    ]:
        await get_data_from_module(module_name, url)


@app.post('/parse')
async def parse(
        url: str,
):
    """
    Ендпонит для парсинга сайтов мед оразнизаций. Сохарянет результаты парсинга в БД.
    :param url: Путь до сайта, который надо распарсить.
    # :param token: Токен, позволяющий получить доступ к API из вне.
    :return:
    """
    await parse_url(url)
