import re
import traceback

from shared_utils.api.slack.core import post_to_slack


def slack_status(text):
    post_to_slack('status', text)


def slack_error(text):
    post_to_slack('errors', text)


def slack_message_raw(text):
    post_to_slack('messages', text)


def slack_callback_raw(text):
    post_to_slack('callbacks', text)


def get_message_header(user, chat):
    username = in_chat = in_chat_id = ''
    if chat.id != user.id:
        in_chat = f' in *{chat.title}*'
        in_chat_id = f' in {chat.id}'
    if user.username:
        username = f' (<https://t.me/{user.username}|{user.username}>)'
    return f'👤 *{user.full_name}*{username}{in_chat}   ' \
           f' _// {user.id}{in_chat_id}_'


def html_to_markdown(text):
    text = text.replace('<b>', '*').replace('</b>', '*'). \
        replace('<i>', '_').replace('</i>', '_')
    text = re.sub('<a href="([^"]+)">([^<]+)</a>', r'<\1|\2>', text)
    return text


def add_quote(text):
    return text.replace('\n', '\n> ')


def slack_message(message, reply_text):
    chat = message.chat
    user = message.from_user
    header = get_message_header(user, chat)
    reply_text = add_quote(html_to_markdown(reply_text))

    slack_message_raw(f'{header}\n\n' 
                      f'🈂️ `{message.text}`\n\n' 
                      f'> {reply_text}')


def slack_callback(query, new_text):
    message = query.message
    user = query.from_user
    chat = message.chat
    header = get_message_header(user, chat)
    old_text = add_quote(html_to_markdown(query.message.text_html))
    new_text = add_quote(html_to_markdown(new_text))

    slack_callback_raw(':red_circle:')
    slack_callback_raw(f'{header}\n\n'
                       f'> {old_text}\n\n'
                       f'㊗️ `{query.data}`\n\n'
                       f'> {new_text}')


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
