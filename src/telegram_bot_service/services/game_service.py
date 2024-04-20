from typing import List, Dict
from database.database import games
from services.utils import async_wait
from callbacks.callback_data import Screen, Transfer


@async_wait()
async def get_games_with_filters(filters: Dict):
    print(filters, flush=True)
    offset = filters.get("offset", 0)
    limit = filters.get("limit", 3)
    title = filters.get("title", None)

    res = games
    if title:
        res = await get_games_by_str_in_title(title)

    total = len(res)
    from_ = offset * limit
    to_ = from_ + limit
    has_prev = offset > 0
    has_next = to_ < total

    return dict(
        games=res[from_:to_],
        has_prev=has_prev,
        has_next=has_next,
        total=total,
        offset=offset,
        limit=limit,
    )


@async_wait()
async def get_game_by_id(id: str) -> Dict:
    return list(filter(lambda x: x["id"] == id, games))[0]


@async_wait()
async def get_games_by_str_in_title(title: str) -> List[Dict]:
    title = title.strip().lower()
    return list(filter(lambda x: title in x["title"].lower(), games))


def pritify_game_info(game: Dict):
    return (
        f'Title: {game["title"]}, {game["year"]}\n\n'
        f'Genre: {game["genre"]}\n'
        f'Players {game["minPlayers"]}-{game["maxPlayers"]}\n'
        f'Min age: {game["minAge"]}\n'
        f'Complexity: {game["gameComplexity"]}\n'
        f'Status: {game["status"]}\n'
        f'Description: {game["gameShortDescription"]}\n'
    )