import json
from datetime import datetime, date
from json import JSONEncoder
from typing import Any
from uuid import UUID

import pytz as pytz
from funcy import is_seqcont, partial
from pydantic.color import Color


def now_in_utc() -> datetime:
    return datetime.now(pytz.utc)


class AdvancedJsonEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, UUID):
            return str(o)
        elif is_seqcont(o) or isinstance(o, set):
            return list(o)
        elif isinstance(o, (date, datetime)):
            return o.isoformat()
        elif isinstance(o, Color):
            return o.original()
        return super().default(o)


advanced_dumps = partial(json.dumps, cls=AdvancedJsonEncoder)
