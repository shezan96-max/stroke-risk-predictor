def calculate_bmi(weight: float | None, height: float | None):
    if not weight or not height:
        return None

    height_m = height / 100
    return round(weight / (height_m ** 2), 2)
