# Need for annotations work https://github.com/Delgan/loguru/issues/206
from __future__ import annotations

import sys
from traceback import format_exc
from typing import Optional

import loguru

from app.utils import advanced_dumps


class TJBaseLogSink:
    def __call__(self, message: loguru.Message) -> None:
        serialized_record = self._serialize_record(message)
        self._write_record(serialized_record)

    def _serialize_record(self, message: loguru.Message) -> str:
        record: loguru.Record = message.record
        serializable_data = self._prepare_data(record)
        return advanced_dumps(serializable_data) + '\n'

    def _prepare_data(self, record: loguru.Record) -> dict:
        serializable_data = {
            'level': record['level'].no,
            'log_level': record['level'].name,
            'time': record['time'],
            'log': record['message'],
            'error': {},
            'params': {},
        }

        exception: Optional[loguru.RecordException] = record['exception']

        if exception:
            # If exception exists (RecordException), but exception.type == None
            # -> log.exception call outside except block
            if not exception.type:
                raise ValueError('log.exception call outside except block')

            # If record from third-part libraries, value can be empty.
            message = str(getattr(exception, 'value', '')) or record['message']

            serializable_data['error'] = {
                'code': exception.type.__name__,
                'message': message,
                'stack': format_exc(),
                'params': {},
            }
        return serializable_data

    @staticmethod
    def _write_record(message: str) -> None:
        sys.stderr.write(message)


class TJRequestLogSink(TJBaseLogSink):
    def _prepare_data(self, record: loguru.Record) -> dict:
        serializable_data = super()._prepare_data(record)
        extra = record['extra']
        request_context = {
            'request': {
                'id': extra['request']['id'],
                'method': extra['request']['method'],
                'path': extra['request']['path'],
            },
            'response': {'status_code': extra['response']['status_code']},
        }
        serializable_data.update(request_context)

        return serializable_data
