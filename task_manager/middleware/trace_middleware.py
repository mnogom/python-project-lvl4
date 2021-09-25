"""Trace middleware"""

import sys
import logging
import secrets

from django.core.handlers.wsgi import WSGIRequest
from django.conf import settings

from .logger import get_logger

get_logger(settings.DEBUG)


def _parse_frame(frame, _id):
    """Parse main information from string.
    :param frame: frame
    :param _id": request-response id
    """

    trace_string = ''
    filename = frame.f_code.co_filename
    if any(filename.find(app) != -1 for app in settings.APPS_TO_TRACE):
        print(frame.f_back.f_code.co_filename)
        trace_string += f'\n -> rr_id: {_id}'
        trace_string += f'\n -> filename: {frame.f_code.co_filename}'
        trace_string += f'\n -> locals: {frame.f_locals}'
        for name, obj in frame.f_locals.items():
            if isinstance(obj, WSGIRequest):
                if obj.GET:
                    trace_string += f'\n --> GET: {obj.GET}'
                if obj.POST:
                    trace_string += f'\n --> POST: {obj.POST}'
        trace_string += f'\n {"-" * 50}'
        return trace_string


def trace_middleware(get_response):
    """Trace middleware function."""

    def middleware(request):
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
