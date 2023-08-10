class Card:
    def __init__(self, color: str, value: str):
        if color not in ["Yellow", "Blue", "White", "Green", "Red", "Purple"]:
            raise AttributeError(f"color can not be {color}")
        if str(value) not in [str(i) for i in range(2, 11)] and value != "Bet":
            raise AttributeError("value must be between 2 and 10 or a Bet")
        self.color = str(color)
        self.value = str(value)

    def __str__(self) -> str:
        return f"{self.value}:{self.color}"
