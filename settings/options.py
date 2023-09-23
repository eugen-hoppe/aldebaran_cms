from dataclasses import dataclass

from settings import constants


@dataclass
class Website:
    name: str = "Aldebaran"
    domain: str = "localhost"
    description: str = "Example website about Aldebaran, Stars and Astronomy."
    author: str = "Arthur Dent"
    lang: str = constants.Lang.EN
    robots: str = "index, follow"
    application_name: str = "Web App"
    copyright_text: str = f"Copyright 2023, The Aldebaran Project"


@dataclass
class Static:
    path: str = "static"
    web_path: str = f"{path}/web"
