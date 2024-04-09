from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/process_image")
async def process_image(image: UploadFile = File(...)):
    # Отримання зображення з запиту
    contents = await image.read()

    # Обробка зображення (додайте код обробки тут)

    # Повернення результатів
    return {"result": "Processed image"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """
    Handles a GET-operation to get favicon.ico.

    :return: The favicon.ico.
    :rtype: FileResponse
    """
    return FileResponse("/favicon.ico")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
