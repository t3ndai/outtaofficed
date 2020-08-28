import httpx

import logging


def comment_update(chanid):
    logging.info("updated item")
    headers = {"X-EventSource-Event": "new_comment"}

    httpx.post(
        f"http://localhost:8001/pub?chanid={chanid}",
        data={"message": "new_comment"},
        headers=headers,
    )
    return

