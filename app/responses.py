from json import dumps
from typing import Any

from funcy import is_seqcont
from starlette.responses import JSONResponse

from app.utils import AdvancedJsonEncoder


class AdvancedJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        return dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            cls=AdvancedJsonEncoder,
        ).encode("utf-8")


class APIResponse(AdvancedJSONResponse):
    def __init__(
        self,
        content: Any = None,
        limit: int = None,
        offset: int = None,
        count: int = None,
        **kwargs: Any,
    ) -> None:
        if is_seqcont(content):
            content = list(content)  # type: ignore
            content = {'status': 'ok', 'data': content, 'count': count or len(content)}

            if limit is not None:
                content.update(limit=limit)

            if offset is not None:
                content.update(offset=offset)
        else:
            content = {'status': 'ok', 'data': content}
        super().__init__(content, **kwargs)


class CSVResponse(APIResponse):
    media_type = 'text/csv'
