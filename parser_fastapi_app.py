import os

from fastapi import FastAPI
from fastapi.security import HTTPBearer
from typing import Dict
app = FastAPI(debug=True)

SERVICE_ACCESS_TOKEN = os.environ.get('SERVICE_ACCESS_TOKEN')
security = HTTPBearer()


async def get_data_from_module(module, url: str):
    analyzes = module.analysis_data(url)
    addresses = module.address_data(url)
    await module.add_to_db(analyzes, 'analyzes')
    await module.add_to_db(addresses, 'addresses')
    return {'analyzes': len(analyzes), 'addresses': len(addresses)}


async def parse_url(url: str):
    parsed_stat = {'analyzes': 0, 'addresses': 0}
    return parsed_stat
    from BulygaEkaterina import Parser
    from Lyusin_Dmitry import Parsing
    from ShevchenkoSemyon import parser
    from TikhonovaMarina import lab4u
    for module in [
        Parser,
        Parsing,
        parser,
        lab4u
    ]:
        res = await get_data_from_module(module, url)
        for key, value in res.items():
            parsed_stat[key] += value
    return parsed_stat


@app.post('/parse')
async def parse(
        url: str
) -> Dict[str, int]:
    """
    Ендпонит для парсинга сайтов мед оразнизаций. Сохарянет результаты парсинга в БД.

    :param url: Путь до сайта, который надо распарсить.

    :return:
    """
    return await parse_url(url)
