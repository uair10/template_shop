from flask import Blueprint, send_from_directory

from template_shop.admin_panel.app.constants import media_path, previews_folder

media_bp = Blueprint("media_bp", __name__, static_folder=media_path)


@media_bp.route("/previews/<path:filename>")
def previews(filename: str):
    return send_from_directory(
        previews_folder,
        filename,
    )
