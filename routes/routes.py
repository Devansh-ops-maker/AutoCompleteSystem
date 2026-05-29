from fastapi import APIRouter, Query
from Controllers.suggestionController import get_suggestions
 
router = APIRouter()
 
@router.get("/suggestions", response_model=list[str])
async def suggestions_route(
    current_word:  str = Query(default=""),
    previous_word: str = Query(default=""),
):
    result = await get_suggestions(current_word=current_word, previous_word=previous_word)
    return result["suggestions"]
 