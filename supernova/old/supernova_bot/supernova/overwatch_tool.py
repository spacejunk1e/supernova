## CUSTOM TOOL OW
from langchain.tools import BaseTool
from overwatch_api.core import AsyncOWAPI
from typing import Optional, Type, Any, Union
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.schema.runnable.config import RunnableConfig
import asyncio
from overwatch_api.constants import PC, EUROPE
from pydantic import BaseModel, Field

from langchain.tools import tool

client = AsyncOWAPI()

import requests

BASE_URL = "https://overfast-api.tekrop.fr/"

from enum import Enum


class HeroRoles(Enum):
    DAMAGE = "damage"
    TANK = "tank"
    SUPPORT = "support"


@tool
def overwatch_hero_list(
    role: Union[str, None] = None,
    locale: str = "en-us",
) -> str:
    """Get a list of Overwatch heroes.

    Args:
        role: The role of the hero. Allowed values are "damage", "tank", and "support".
        locale: The locale to use for the hero names. Defaults to "en-us". Allowed: "de-de", "en-gb", "en-us", "es-es", "es-mx", "fr-fr", "it-it", "ja-jp", "ko-kr", "pl-pl", "pt-br", "ru-ru", "zh-cn", "zh-tw".

    """
    url = f"{BASE_URL}/heroes"
    query_params = []
    if role:
        query_params.append(f"role={role}")
    if locale:
        query_params.append(f"locale={locale}")

    if query_params:
        url += "?" + "&".join(query_params)

    response = requests.get(url)
    if response.status_code != 200:
        if response.status_code == 422:
            raise Exception(f"Validation error: {response.text}")
        elif response.status_code == 500:
            raise Exception(f"Internal server error: {response.text}")
        elif response.status_code == 504:
            raise Exception(f"Blizzard server error: {response.text}")
        raise Exception(f"Error retrieving hero list: {response.text}")
    return response.json()


# Observation: {
#     "name": "Ana",
#     "description": "One of the founding members of Overwatch, Ana uses her skills and expertise to defend her home and the people she cares for.",
#     "portrait": "https://d15f34w2p8l1cc.cloudfront.net/overwatch/3429c394716364bbef802180e9763d04812757c205e1b4568bc321772096ed86.png",
#     "role": "support",
#     "location": "Cairo, Egypt",
#     "hitpoints": {"health": 200, "armor": 0, "shields": 0, "total": 200},
#     "abilities": [
#         {
#             "name": "Biotic Rifle",
#             "description": "Long-range rifle that heals allies and damages enemies.  Hold to zoom in.",
#             "icon": "https://d15f34w2p8l1cc.cloudfront.net/overwatch/efe0ebb135e87dc26b60f0d20500dcd7553ad121ab2b10cd4ffb5db17be9c977.png",
#             "video": {
#                 "thumbnail": "https://images.blz-contentstack.com/v3/assets/blt2477dcaf4ebd440c/bltc56d4d9789a018d0/63390487ed7dcc6a0028039c/ANA_BIOTICRIFLE.jpg",
#                 "link": {
#                     "mp4": "https://assets.blz-contentstack.com/v3/assets/blt2477dcaf4ebd440c/blt7f91fa726d903e78/6339047ee3c2a2741688cb9f/OVERWATCH_WEBSITE_CHARACTER_CAPTURE_AnaBioticRifle_WEB_16x9_1920x1080p30_H264.mp4",
#                     "webm": "https://assets.blz-contentstack.com/v3/assets/blt2477dcaf4ebd440c/blt90138e57c4b91c94/6339047e64fe5a7d4481a05c/OVERWATCH_WEBSITE_CHARACTER_CAPTURE_AnaBioticRifle_WEB_16x9_1920x1080p30_WEBM.webm",
#                 },
#             },
#         },
#         {
#             "name": "Sleep Dart",
#             "description": "Fires a dart that puts an enemy to sleep.",
#             "icon": "https://d15f34w2p8l1cc.cloudfront.net/overwatch/20707fd82265412fdc6d2353daa88ec7558cd71c89aa3ac6cf0e78bbbfcabd80.png",
#             "video": {
#                 "thumbnail": "https://images.blz-contentstack.com/v3/assets/blt2477dcaf4ebd440c/bltb27e2783f517c7fe/63390487e3c2a2741688cba3/ANA_SLEEPDART.jpg",
#                 "link": {
#                     "mp4": "https://assets.blz-contentstack.com/v3/assets/blt2477dcaf4ebd440c/blt35fa57c9d35027cf/6339047eed7dcc6a00280398/OVERWATCH_WEBSITE_CHARACTER_CAPTURE_AnaSleepDart_WEB_16x9_1920x1080p30_H264.mp4",
#                     "webm": "https://assets.blz-contentstack.com/v3/assets/blt2477dcaf4ebd440c/bltb6b9ecf5d9a2ec69/6339047ef87c00687e8ef222/OVERWATCH_WEBSITE_CHARACTER_CAPTURE_AnaSleepDart_WEB_16x9_1920x1080p30_WEBM.webm",
#                 },
#             },
#         },
#         {
#             "name": "Biotic Grenade",
#             "description": "Throws a grenade that heals and increases healing on allies, while damaging and preventing healing on enemies.",
#             "icon": "https://d15f34w2p8l1cc.cloudfront.net/overwatch/c8190b234bf0a0e28eecffe162d0c942e6b8656e95f4688c6ca3b025fa5a487d.png",
#             "video": {
#                 "thumbnail": "https://images.blz-contentstack.com/v3/assets/blt2477dcaf4ebd440c/bltcd66dcc6eb196187/633904873922a2677fc88cfa/ANA_BIOTICGRENADE.jpg",
#                 "link": {
#                     "mp4": "https://assets.blz-contentstack.com/v3/assets/blt2477dcaf4ebd440c/blt808b8a165c19d2e6/6339047eb8dbde69f52798e8/OVERWATCH_WEBSITE_CHARACTER_CAPTURE_AnaBioticGrenade_WEB_16x9_1920x1080p30_H264.mp4",
#                     "webm": "https://assets.blz-contentstack.com/v3/assets/blt2477dcaf4ebd440c/blt73fcfa06c4272760/6339047d3922a2677fc88cf6/OVERWATCH_WEBSITE_CHARACTER_CAPTURE_AnaBioticGrenade_WEB_16x9_1920x1080p30_WEBM.webm",
#                 },
#             },
#         },
#         {
#             "name": "Nano Boost",
#             "description": "Increases an ally's damage, while reducing damage taken.",
#             "icon": "https://d15f34w2p8l1cc.cloudfront.net/overwatch/6fda18b343f3fd0e8dc50fa5a91589e1ca9ed7471a354f61dfc9f22b27b19497.png",
#             "video": {
#                 "thumbnail": "https://images.blz-contentstack.com/v3/assets/blt2477dcaf4ebd440c/blt5901c5f790bb82f9/63390487da1d806602f83eee/ANA_NANOBOOST.jpg",
#                 "link": {
#                     "mp4": "https://assets.blz-contentstack.com/v3/assets/blt2477dcaf4ebd440c/blta81ab58fade9b59b/6339047e8537f87bfbcdc3f8/OVERWATCH_WEBSITE_CHARACTER_CAPTURE_AnaNanoBoost_WEB_16x9_1920x1080p30_H264.mp4",
#                     "webm": "https://assets.blz-contentstack.com/v3/assets/blt2477dcaf4ebd440c/blt557e93a659cf572c/6339047e1a0b5e7d3d1ec595/OVERWATCH_WEBSITE_CHARACTER_CAPTURE_AnaNanoBoost_WEB_16x9_1920x1080p30_WEBM.webm",
#                 },
#             },
#         },
#     ],
#     "story": {
#         "summary": "A founding member of Overwatch and once renowned as the greatest sniper in the world, Ana Amari comes from a long line of decorated military veterans. Though she was thought to have perished in a firefight with Talon, Ana has rejoined the fray to protect her country, family, and closest allies.",
#         "media": {"type": "video", "link": "https://youtu.be/yzFWIw7wV8Q"},
#         "chapters": [
#             {
#                 "title": "Overwatch",
#                 "content": "As the Omnic Crisis inflicted a heavy toll on Egypt, the country's depleted and undermanned armed forces relied on elite snipers for support. Among them was Ana Amari, who was widely considered to be the world's best. Her superior marksmanship, decision-making, and instincts made her a natural selection to join the Overwatch strike team that would end the war. Following the success of Overwatch's original mission, Ana served for many years as Strike Commander Morrison's second-in-command. Despite her responsibilities in leading the organization, Ana refused to step away from combat operations. She remained on active duty well into her fifties, until she was believed to have been killed during a hostage rescue mission by the Talon operative known as Widowmaker.",
#                 "picture": "https://images.blz-contentstack.com/v3/assets/blt2477dcaf4ebd440c/blt26f888b741ac09bb/638807c1113983111ba8cfa9/ana_00.jpg",
#             },
#             {
#                 "title": "Post overwatch",
#                 "content": "In truth, Ana survived that encounter, despite being gravely wounded and losing her right eye. During her recovery, she wrestled with the weight of a life spent in combat, and she chose to stay out of the world's growing conflicts. However, as time passed, she realized she could not sit on the sidelines while people threatened her city and the innocents around her. Ana rejoined the fight, this time as a healer, and dedicated herself to monitoring global security threats. Prior to disrupting Talon operations in Cairo, she intercepted an unlikely broadcast: the Overwatch Recall from her former friend, Winston.",
#                 "picture": "https://images.blz-contentstack.com/v3/assets/blt2477dcaf4ebd440c/blt337560e347894727/638807fa6663180e7cbbcf88/ana_01.jpg",
#             },
#             {
#                 "title": "Recall",
#                 "content": "Ana remained uncertain about the Recall, but she had decided to help her comrades from the shadows. She sent word to Cole Cassidy, knowing that he had survived the demise of Overwatch and returned as a gunslinger for hire. Ana knew the organization needed new blood—people like Cassidy and her daughter, Pharah—were it to stand a chance, and worried the old guard would only poison the agency’s return. She shared as much with her daughter in an overdue reunion, before embarking on her own mission with Soldier: 76. With no regrets left, Ana travels the world tracking down Talon and the ghosts that haunt her former allies. And while she didn’t rejoin Overwatch, Ana keeps her eye on their exploits just in case.",
#                 "picture": "https://images.blz-contentstack.com/v3/assets/blt2477dcaf4ebd440c/bltc1bd29f5c953e0f4/638807fa3b13b1106f74ec4c/ana_02.jpg",
#             },
#         ],
#     },
# }

def exclude_keys(data, keys):
    for key in keys:
        parts = key.split(".")
        target = data
        for part_index, part in enumerate(parts[:-1]):
            if part.endswith("[]"):
                # This is a list operation; iterate over the items
                part = part[:-2]
                target = target.get(part, [])
                if isinstance(target, list):
                    for item in target:
                        exclude_keys(item, [".".join(parts[part_index+1:])])
                break
            else:
                target = target.get(part, {})
        else:
            if parts[-1] in target:
                del target[parts[-1]]


@tool
def overwatch_hero_details(
    hero_key: str,
    locale: str = "en-us",
    exclude_filter: Union[list[str], None] = ["abilities[].icon", "abilities[].video"],
) -> str:
    """
    Retrieves details about an Overwatch hero.

    Args:
        hero_key (str): Key of the hero (must be lowercase).
        locale (str, optional): Locale for hero names, e.g., "en-us". Defaults to "en-us".
        exclude_filter (Union[list[str], None], optional): Fields to exclude from the result.

    Returns:
        str: JSON string with details about the hero:
            - name, description, portrait, role, location
            - hitpoints: health, armor, shields, total
            - abilities: name, description, icon, video (thumbnail, mp4, webm)
            - story: summary, media (type, link), chapters (title, content, picture)
    """
    url = f"{BASE_URL}/heroes/{hero_key}"
    query_params = []
    if locale:
        query_params.append(f"locale={locale}")

    if query_params:
        url += "?" + "&".join(query_params)

    response = requests.get(url)
    if response.status_code != 200:
        if response.status_code == 422:
            raise Exception(f"Validation error: {response.text}")
        elif response.status_code == 500:
            raise Exception(f"Internal server error: {response.text}")
        elif response.status_code == 504:
            raise Exception(f"Blizzard server error: {response.text}")
        raise Exception(f"Error retrieving hero details: {response.text}")

    json_response = response.json()
    if exclude_filter:
        exclude_keys(json_response, exclude_filter)
    
    return json_response


from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

tools = [
    overwatch_hero_list,
    overwatch_hero_details,
]

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
)


if __name__ == "__main__":
    from langchain.agents import initialize_agent, Tool
    from langchain.agents import AgentType
    from langchain.llms import OpenAI
    from langchain.chat_models import ChatOpenAI

    tools = [
        overwatch_hero_list,
        overwatch_hero_details,
    ]

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

    agent = initialize_agent(
        tools,
        llm,
        # prompt="ddd",
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
    )
    print(
        agent.run(
            # "Compare the hero stats for Ana and Kiriko."
            # "How do the stats of Reinhardt and Winston differ?"
            # "Try explain the difference in playstyle between Winston and Reinhardt given their abilities and stats"
            "Which tank is the most unique, "
        )
    )
    # print(agent.run("Please find my hero stats for SilverWolf#22356"))
