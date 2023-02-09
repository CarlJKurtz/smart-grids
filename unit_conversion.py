def convert(value, start_unit, des_unit) -> float:
    if start_unit == "mm" and des_unit == 'pt':
        value = value / 0.352777778

    elif start_unit == "px" and des_unit == 'pt':
        value = value

    elif start_unit == "pt" and des_unit == 'mm':
        value = value * 0.352777778

    elif start_unit == "px" and des_unit == 'mm':
        value = value * 25.4 / 300, 3

    elif start_unit == 'mm' and des_unit == 'px':
        value = 300 * value / 25.4, 3

    elif start_unit == "pt" and des_unit == 'px':
        value = value

    return value
