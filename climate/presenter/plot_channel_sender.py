from typing import List, Tuple

from climate import adapter


def plot_to_channel(file: str, channel: adapter.Channel, title: str, description: str):
    if channel == adapter.Channel.DISCORD:
        _send_to_discord(file, title, description)
    pass


def _send_to_discord(file, title, description):
    adapter.send_attachment(msg_title=title,
                            file_path=file,
                            description=description,
                            file_name=file.name)
    pass
