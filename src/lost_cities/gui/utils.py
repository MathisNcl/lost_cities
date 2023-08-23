from PIL import Image


import numpy as np

image: np.ndarray = np.array(Image.open("src/lost_cities/gui/assets/cards.webp").convert("RGB"))
size: tuple[int, int] = (85, 133)


def extract_card(color: str, value: int) -> np.ndarray:
    """extract card image from the original image

    Args:
        color (str): card color to extrcat
        value (int): card value to extract

    Returns:
        np.ndarray: graphical card
    """
    index_color = ["Yellow", "Blue", "White", "Green", "Red", "Back"].index(color)
    if value == 0:
        value = 11
    value -= 2

    return image[size[1] * index_color : size[1] * (index_color + 1), size[0] * value : size[0] * (value + 1)]
