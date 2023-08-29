import numpy as np
from PIL import Image

image: np.ndarray = np.array(Image.open("src/lost_cities/gui/assets/cards.webp"))
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

    return rgba2rgb(image[size[1] * index_color : size[1] * (index_color + 1), size[0] * value : size[0] * (value + 1)])


def rgba2rgb(rgba: np.ndarray, background: tuple[int, int, int] = (255, 255, 255)) -> np.ndarray:
    """transform a rgba image into a rgb with right opacity pixel

    Args:
        rgba (np.ndarray): rgba image (4D)
        background (tuple[int, int, int], optional): Inital background of the image rgba. Defaults to (255, 255, 255).

    Returns:
        np.ndarray: rgb image (3D)
    """
    row, col, ch = rgba.shape

    assert ch == 4, "RGBA image has 4 channels."

    rgb: np.ndarray = np.zeros((row, col, 3), dtype="float32")
    r, g, b, a = rgba[:, :, 0], rgba[:, :, 1], rgba[:, :, 2], rgba[:, :, 3]

    a = np.asarray(a, dtype="float32") / 255.0

    R, G, B = background

    rgb[:, :, 0] = r * a + (1.0 - a) * R
    rgb[:, :, 1] = g * a + (1.0 - a) * G
    rgb[:, :, 2] = b * a + (1.0 - a) * B

    return np.asarray(rgb, dtype="uint8")
