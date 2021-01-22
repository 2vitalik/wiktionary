import traceback

from shared_utils.api.slack.core import post_to_slack


def slack_status(message):
    post_to_slack('status', message)


def slack_error(message):
    post_to_slack('errors', message)


def slack_message_raw(message):
    post_to_slack('messages', message)


def slack_callback(message):
    post_to_slack('callbacks', message)


def simplify_traceback(traceback_text):
    # todo
    return traceback_text


def slack_exception(slug, exc, message_suffix='', send_traceback=True):
    exc_name = type(exc).__name__
    message = f':warning: `{slug}`  *{exc_name}*: {exc}  {message_suffix}'

    traceback_text = simplify_traceback(traceback.format_exc().strip())
    content = f'{message}\n```{traceback_text}```'

    slack_error(content if send_traceback else message)


class SilentError(Exception):
    pass


def slack(name, *, raise_error=True):
    def decorator(func):

        def wrapped(*args, **kwargs):
            result = None
            exception = None
            try:
                result = func(*args, **kwargs)
            except SilentError as e:
                exception = e
            except Exception as e:
                exception = SilentError(e)
                slack_exception(name, e)

            if exception:
                slack_error(f":no_entry: `{name}`  Failed")
                if raise_error:
                    raise exception
            return result

        return wrapped
    return decorator
