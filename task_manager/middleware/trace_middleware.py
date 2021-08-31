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
    """Parse main information from string."""

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
                                                                      value=getattr(value, param, None))
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




# Георгий Рымаренко, [12 авг. 2021 г., 18:56:22]:
# class RequestIdMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         request_id = request.headers.get('x-request-id', str(uuid.uuid4()))
#         set_request_id(request_id)

#     def process_response(self, request, response):
#         del_request_id()
#         return response

# def set_request_id(request_id: Optional[str] = None):
#     if not request_id:
#         request_id = str(uuid.uuid4())
#     setattr(_thread_locals, 'request_id', request_id) <--------- CHECK IT OUT


# def del_request_id():
#     setattr(_thread_locals, 'request_id', None)


# def get_request_id():
#     return getattr(_thread_locals, 'request_id', None)

# import threading

# _thread_locals = threading.local()

# class CustomFormatter(logging.Formatter):
#     def format(self, record: LogRecord) -> str:
#         extra = {'user': get_current_user(), 'request_id': get_request_id()}
#         for k, v in extra.items():
#             setattr(record, k, v)
#         return super().format(record)

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s:%(lineno)d - %(message)s'
#         },
#         'custom': {
#             'format': '[{asctime}][{levelname}][{name}.{funcName}({filename}:{lineno})][{request_id}][{user}] - {message}',
#             'class': 'common.logging.CustomFormatter',
#             'style': '{',
#         },
#     },