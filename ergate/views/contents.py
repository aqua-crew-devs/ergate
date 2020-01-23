from flask import Blueprint, request

from ergate.controllers.content import Content

bp = Blueprint("contents", __name__, url_prefix="/contents")


@bp.route("/", methods=["POST"])
def create_a_new_content():
    content = request.get_json()
    callback_url = content["callback_url"]
    stream_url = content["stream_url"]

    content_cnt = Content(stream_url, callback_url)
    content_cnt.record()

    return ""

