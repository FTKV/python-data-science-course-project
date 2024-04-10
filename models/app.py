from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/process_image")
async def process_image(image: UploadFile = File(...)):
    # Отримання зображення з запиту
    contents = await image.read()

    # Обробка зображення (додайте код обробки тут)

    # Повернення результатів
    return {"result": "Processed image"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
