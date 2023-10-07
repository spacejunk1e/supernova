import requests
from typing import Any, Optional, Union, List


class OverwatchAPI:
    BASE_URL = "https://overfast-api.tekrop.fr/"

    DEFAULT_INCLUDE_FILTER = [
        "name", "description", "portrait", "role", "location",
        "hitpoints.health", "hitpoints.armor", "hitpoints.shields",
        "hitpoints.total", "abilities.name", "abilities.description",
        "story.summary", "story.media.type", "story.media.link",
        "story.chapters.title", "story.chapters.content", "story.chapters.picture"
    ]

    def _get(self, endpoint: str, params: dict = None) -> str:
        url = f"{self.BASE_URL}/{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def role_list(self, locale: str = "en-us") -> List[dict]:
        """Get a list of available Overwatch roles."""
        params = {"locale": locale}
        return self._get("roles", params=params)

    def hero_list(self, role: Union[str, None] = None, locale: str = "en-us") -> str:
        """Get a list of Overwatch heroes by role and locale."""
        params = {"role": role, "locale": locale} if role else {"locale": locale}
        return self._get("heroes", params=params)

    def hero_details(self, hero_key: str, locale: str = "en-us", include_filter: Union[List[str], None] = None) -> dict:
        """Retrieve details about an Overwatch hero."""
        params = {"locale": locale}
        details = self._get(f"heroes/{hero_key}", params=params)
        if include_filter is None:
            include_filter = self.DEFAULT_INCLUDE_FILTER
        return self._include_keys(details, include_filter)

    def _include_keys(self, data: dict, keys: List[str]) -> dict:
        result = {}
        for key in keys:
            parts = key.split(".")
            target = data
            for part in parts[:-1]:
                target = target.get(part, {})
            if parts[-1] in target:
                self._set_nested_key(result, parts, target[parts[-1]])
        return result

    @staticmethod
    def _set_nested_key(data: dict, keys: List[str], value: Any) -> None:
        for key in keys[:-1]:
            data = data.setdefault(key, {})
        data[keys[-1]] = value

    def get_player_summary(self, player_id: str) -> dict:
        """
        Get player summary including name, avatar, competitive ranks, etc.

        Args:
            player_id (str): Identifier of the player : BattleTag (with "#" replaced by "-"). Case-sensitive!

        Returns:
            dict: Player summary data including username, avatar, namecard, title, endorsement, competitive ranks, and privacy.
        """
        url = f"{self.BASE_URL}/players/{player_id}/summary"

        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching player summary: {response.text}")

    def search_player(self, name: str, privacy: Optional[str] = None,
                      order_by: Optional[str] = "name:asc", offset: int = 0, limit: int = 20) -> dict:
        """
        Search for a given player by using their username.

        Args:
            name (str): Player nickname to search.
            privacy (Optional[str], optional): Privacy settings of the player career ("public", "private"). Defaults to None.
            order_by (Optional[str], optional): Ordering field and way it's arranged. Defaults to "name:asc".
            offset (Optional[int], optional): Offset of the results. Defaults to 0.
            limit (Optional[int], optional): Limit of results per page. Defaults to 20.

        Returns:
            dict: Total number of results and list of players found.
        """
        url = f"{self.BASE_URL}/players"
        params = {
            "name": name,
            "order_by": order_by,
            "offset": offset,
            "limit": limit
        }

        if privacy:
            params["privacy"] = privacy

        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 422:
            detail = response.json().get('detail')
            raise ValueError(f"Validation error: {detail}")
        elif response.status_code == 500:
            error = response.json().get('error')
            raise Exception(f"Internal server error: {error}")
        elif response.status_code == 504:
            error = response.json().get('error')
            raise Exception(f"Blizzard server error: {error}")
        else:
            raise Exception(f"Unexpected error: {response.text}")

    def get_player_stats_summary(self, player_id: str, gamemode: str = None, platform: str = None) -> dict:
        """
        Get player statistics summary, including winrate, kda, damage, healing, etc.

        Args:
            player_id (str): Identifier of the player : BattleTag (with "#" replaced by "-"). Case-sensitive!
            gamemode (str, optional): Filter on "quickplay" or "competitive". If not specified, combines all.
            platform (str, optional): Filter on "console" or "pc". If not specified, combines all.

        Returns:
            dict: Player statistics summary including general, roles, and heroes.
        """
        url = f"{self.BASE_URL}/players/{player_id}/stats/summary"
        params = {}
        if gamemode:
            params['gamemode'] = gamemode
        if platform:
            params['platform'] = platform

        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching player stats summary: {response.text}")


# Usage
api = OverwatchAPI()
roles = api.role_list()
hero_details = api.hero_details('tracer')
print(hero_details)

# Search
import json

search_result = api.search_player("SpaceJunkie", privacy="private")
print(json.dumps(search_result, indent=4))
