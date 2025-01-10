from os import environ
from flask import Flask

from clients.async_base_api import AsyncBaseApi

from main.file_operations import FileOperations

app = Flask(__name__)
client = AsyncBaseApi()


@app.route("/", methods=["GET"])
async def category_and_extract():

    categories = environ.get("CATEGORIES").split(",")
    url = environ.get("API_URL")
    full_urls = []
    file_created = []

    for cat in categories:
        full_urls.append(f"{url}/{cat}")

    for single_url in full_urls:
        response = await get_data(url=single_url)
        file_created.append(response)

    return f"<h1>Executing Movie Category Extract To File & Cloud Storage For {file_created}</h2>"


async def get_data(url: str) -> None:
    file_operations: FileOperations = FileOperations.get_class()
    result = await client.get(url)

    category = url.rsplit("/", 1)[-1]
    file_name = f"{category}.parquet"
    request_status = result[0].get("status_code")
    request_error = result[0].get("error")

    if request_status == 200 and request_error is None:
        file_operations.write_to_file(data=result, file_name=file_name)
        file = file_operations.read_file_to_bytes(file_name=file_name)
        file_operations.upload_to_cloud(file_object=file, file_key=file_name)
        return category


if __name__ == "__main__":
    app.run(debug=True)
