import json 
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

from models import User, UserState
from core import StateManager, AppRouter
from core.handlers import ChoosingThemeHandler, HelloHandler, ChoosingOptionHandler, NameHandler, AgeHandler, QuestionHandler


app = FastAPI()

state_manager = StateManager()
router = AppRouter(state_manager)

router.register_handler(None, HelloHandler())
router.register_handler(UserState.CHOOSING_THEME.value, ChoosingThemeHandler())
router.register_handler(UserState.CHOOSING_OPTION.value, ChoosingOptionHandler())
router.register_handler(UserState.SETTING_NAME.value, NameHandler())
router.register_handler(UserState.SETTING_AGE.value, AgeHandler())
router.register_handler(UserState.ASKED_QUESTION.value, QuestionHandler())


@app.post("/app-connector")
async def handle_request(request: Request, user: User):
    answer = await router.route(user)
    return answer.model_dump()


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(8000))
