def convert(value, start_unit, des_unit, dpi) -> float:
    if start_unit == "mm" and des_unit == 'pt':
        value = value / 0.352777778

    elif start_unit == "px" and des_unit == 'pt':
        value = value

    elif start_unit == "pt" and des_unit == 'mm':
        value = value * 0.352777778

    elif start_unit == "px" and des_unit == 'mm':
        value = value * 25.4 / dpi

    elif start_unit == 'mm' and des_unit == 'px':
        value = dpi * value / 25.4

    elif start_unit == "pt" and des_unit == 'px':
        value = value

    elif start_unit == "in" and des_unit == 'pt':
        value = value * 25.4 / 0.352777778

    elif start_unit == "in" and des_unit == 'mm':
        value = value * 25.4

    elif start_unit == "in" and des_unit == 'px':
        value = dpi * value

    elif start_unit == "pt" and des_unit == 'in':
        value = value * 0.352777778 / 25.4

    elif start_unit == "mm" and des_unit == 'in':
        value = value / 25.4

    elif start_unit == "px" and des_unit == 'in':
        value = dpi / value

    return value
