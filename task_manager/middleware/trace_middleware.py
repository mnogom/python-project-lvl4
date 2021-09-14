"""Trace middleware"""

import sys
import logging
import secrets

from django.core.handlers.wsgi import WSGIRequest
from django.conf import settings

from .logger import get_logger


STRING_TEMP = ('\n'
               '  ──> rr_id: {rr_id}\n'
               '  ─────> frame {frame}\n'
               '  ─────> from {back}\n'
               '  ─────> call {call}\n'
               '          └─> function: {function}\n'
               '              └─> code line: {line}\n'
               '              └─> stack size: {stack_size}\n'
               '              └─> f_locals: ')

SUB_STRING_TEMP = '{indent}└─> {name}: {value}'
get_logger(settings.DEBUG)


def _parse_frame(frame, _id):
    """Parse main information from string.
    :param frame: frame
    :param _id": request-response id
    """

    trace_string = ''

    filename = frame.f_code.co_filename
    if any(filename.find(app) != -1 for app in settings.APPS_TO_TRACE):
        trace_string = STRING_TEMP.format(rr_id=_id,
                                          frame=frame,
                                          back=frame.f_back.f_code.co_filename,
                                          call=frame.f_code.co_filename,
                                          function=frame.f_code.co_name,
                                          line=frame.f_lineno,
                                          stack_size=frame.f_code.co_stacksize)

        for key, value in frame.f_locals.items():
            if not key.startswith('__') and key != 'self':
                if isinstance(value, (WSGIRequest, )) and settings.REQUEST_PARAMS_TO_LOG:
                    trace_string += '\n' + SUB_STRING_TEMP.format(indent=' ' * 18,
                                                                  name=key,
                                                                  value='')
                    for param in settings.REQUEST_PARAMS_TO_LOG:
                        trace_string += '\n' + SUB_STRING_TEMP.format(indent=' ' * 22,
                                                                      name=param,
                                                                      value=getattr(value,
                                                                                    param,
                                                                                    None))
                else:
                    trace_string += '\n' + SUB_STRING_TEMP.format(indent=' ' * 18,
                                                                  name=key,
                                                                  value=value)
    return trace_string


def trace_middleware(get_response):
    """Trace middleware function."""

    def middleware(request):
        logging.info('-' * 150)
        """Middleware inner function."""

        # Generate request-response id
        rr_id = secrets.token_urlsafe(10)

        def _tracer(frame, event, arg, _id=rr_id):
            """Tracer function."""

            trace_string = _parse_frame(frame, _id)
            if trace_string:
                logging.info(trace_string)

        sys.settrace(_tracer)
        response = get_response(request)
        response['rr_id'] = rr_id
        return response
    return middleware
