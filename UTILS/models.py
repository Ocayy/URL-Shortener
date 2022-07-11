import pydantic

class Settings:
    version : str = "1.0.0"
    github_repository : str = ""

    description : str = """
    URL-Shortener is a simple URL shortener that allows you to shorten long URLs.
    """

    tags_metadata : str = [
        {
            "name": "Default",
            "description": "Default tag"
        },
        {
            "name": "Manage",
            "description": "Manage URL-Shortener - create new URLs, delete URLs, etc."
        },
        {
            "name": "Stats",
            "description": "Get stats about URL-Shortener or a specific URL"
        }
    ]

class Post_CreateShortUrl(pydantic.BaseModel):
    url: str

