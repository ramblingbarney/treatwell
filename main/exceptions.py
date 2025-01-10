import logging


def exception_handler_asyncio(loop, context):
    # get details of the exception
    exception = context["exception"]
    message = context["message"]
    # log exception
    logging.error(f"Task failed, msg={message}, exception={exception}")
