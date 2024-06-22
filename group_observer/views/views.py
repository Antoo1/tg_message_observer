from fastapi_utils.cbv import cbv
from fastapi import Depends, Query, APIRouter, Request

from group_observer.app.dependencies import get_db_session
from group_observer.common.db import MongoSession
from group_observer.services import RulesSaver

router = APIRouter()


@cbv(router)
class OrderCBV:
    db_session: MongoSession = Depends(get_db_session)

    @router.post("/webhook")
    async def webhook(self, request: Request) -> None:
        await RulesSaver().save_rule(request)