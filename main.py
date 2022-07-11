import fastapi
import datetime
import UTILS.models as models
import UTILS.utils as utils
import UTILS.database as db

app = fastapi.FastAPI(
    title="URL-Shortener",
    description=models.Settings.description,
    openapi_url="/openapi.json",
    openapi_tags=models.Settings.tags_metadata,
    docs_url="/docs",
    redoc_url=None,
    version=models.Settings.version,
    contact={
        "name": "Ocayy",
        "url": "https://github.com/Ocayy",
        "email": "contact@jaco13.com",
    },
    license={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)
database = db.Database()

@app.get("/", tags=["Default"])
def read_root():
    return {
        "Project": "URL-Shortener",
        "Description": "A URL Shortener API",
        "Version": models.Settings.version,
        "Author": "Jakub Nowosad",
        "Github Repository": models.Settings.github_repository
    }

@app.get("/{short_url}", tags=["Default"])
def redirect_to_main_url(short_url: str):
    data = database.get_data_from_short_url(short_url)
    if data is None:
        return {"error": "URL not found"}
    else:
        database.add_visits(short_url, datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        return fastapi.responses.RedirectResponse(data["long_url"])

@app.post("/create", tags=["Manage"])
def create_url(data: models.Post_CreateShortUrl):
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    short_url = utils.generate_short_url(data.url, timestamp)
    
    database.add_short_url(short_url, data.url, timestamp)

    return {"generated_url": short_url}

@app.delete("/delete/{short_url}", tags=["Manage"])
def delete_url(short_url: str):
    database.delete_url(short_url)

    return {"success": True}

@app.get("/stats/", tags=["Stats"])
def get_stats():
    number_of_urls = database.get_stats()
    return {"total_urls": number_of_urls}

@app.get("/stats/{short_url}", tags=["Stats"])
def get_stats_about_short_url(short_url: str):
    data = database.get_data_from_short_url(short_url)
    if data is None:
        return {"error": "URL not found"}
    else:
        return {
            "short_url": short_url,
            "long_url": data["long_url"],
            "created_date": data["created_date"],
            "last_visit": data["last_visit"],
            "visits": data["visits"]
        }

@app.get("/stats/all", tags=["Stats"])
def get_stats_about_all_urls():
    data = database.get_all_data()
    return data

