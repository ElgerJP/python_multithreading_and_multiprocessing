import os
import time
from pathlib import Path
import concurrent.futures
import glob
import requests
from PIL import Image, ImageFilter


IMAGE_URLS = [
    "https://images.unsplash.com/photo-1635088173181-673ff547a555",
    "https://images.unsplash.com/photo-1635481712720-a1b30952ed4b",
    "https://images.unsplash.com/photo-1635420280816-c0dc0ee8a7a7",
    "https://images.unsplash.com/photo-1632269826291-2cb3009bf43d",
    "https://images.unsplash.com/photo-1617137604160-fc923f3173d0",
    "https://images.unsplash.com/photo-1635398517284-2f3c7fef7fee",
    "https://images.unsplash.com/photo-1635417073744-0b09b9ac4dfc",
    "https://images.unsplash.com/photo-1604854657221-42873468254c",
    "https://images.unsplash.com/photo-1615762325085-8babbbce2c43",
    "https://images.unsplash.com/photo-1635317224525-19c1d33f9036",
    "https://images.unsplash.com/photo-1635333702118-b53d15341ed4",
    "https://images.unsplash.com/photo-1635269941799-665d1618d5d8",
    "https://images.unsplash.com/photo-1635297383087-8842f98f908a",
    "https://images.unsplash.com/photo-1610898404424-1439b7006e1c",
    "https://images.unsplash.com/photo-1634692804775-67207ea81cc5",
    "https://images.unsplash.com/photo-1633410229020-938fdaefd884",
    "https://images.unsplash.com/photo-1632085847101-028ec1b2abeb",
    "https://images.unsplash.com/photo-1627142625827-1d7e65635b18",
    "https://images.unsplash.com/photo-1629129207344-6a452eea1ea5",
    "https://images.unsplash.com/photo-1628258867160-f11ee22397c5",
    "https://images.unsplash.com/photo-1635342242063-a64d654fbfbe",
]
IMAGE_FOLDER = os.path.join(os.getcwd(), "images")
PROCESSED_FOLDER = os.path.join(IMAGE_FOLDER, "processed")


def create_folder(folder_path: str) -> None:
    """
    Create the image folder
    :return: None
    """
    path = Path(os.path.join(os.getcwd(), folder_path))
    path.mkdir(parents=True, exist_ok=True)


# Function that will download a image from an url
def download_image(image_url: str) -> None:
    """
    Download an image from an url
    :param image_url: The url of the image
    :return: None
    """
    img_name = image_url.split("/")[-1].split("?")[0] + ".jpg"
    print(f"Downloading image from {img_name}")
    img_content = requests.get(image_url).content
    with open(os.path.join(IMAGE_FOLDER, img_name), "wb") as img_file:
        img_file.write(img_content)

    print(f"Downloaded image from {img_name}")


def process_image(image_path: str) -> None:
    """
    Process an image
    :param image_path: The path of the image
    :return: None
    """
    img_name = os.path.split(image_path)[-1]
    print(f"Processing image {img_name}")
    thumb_size = (300, 300)
    img = Image.open(image_path)
    img = img.filter(ImageFilter.GaussianBlur(radius=15))
    img.thumbnail(thumb_size)

    img.save(os.path.join(PROCESSED_FOLDER, f"thumb_{img_name}"), "JPEG")
    print(f"Processed image {img_name}")


def main(*args, **kwargs) -> None:
    time_start = time.perf_counter()
    create_folder(IMAGE_FOLDER)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_image, IMAGE_URLS)

    create_folder(PROCESSED_FOLDER)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(process_image, glob.glob(os.path.join(IMAGE_FOLDER, "*.jpg")))

    time_end = time.perf_counter()
    print(f"Time taken: {time_end - time_start}")


if __name__ == "__main__":
    main()
