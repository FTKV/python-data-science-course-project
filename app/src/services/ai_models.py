"""
Module to work with AI models
"""

from httpx import AsyncClient

from src.conf.config import settings


async def process_image(img_file):
    """
    Generates a PNG image with a QR code from the url of the image:

    :param img_file: The image file
    :type img_file: file.
    :return: The recognized text from image
    :rtype: str
    """
    client = AsyncClient(
        base_url=f"{settings.api_protocol}://{settings.tensorflow_container_name}:{settings.tensorflow_port}",
    )
    response = await client.post(
        "/process_image",
        files={"img_file": img_file},
    )
    data = response.json()
    return data.get("result")
