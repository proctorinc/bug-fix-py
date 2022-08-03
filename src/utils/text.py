from src import constants

class Text:
    def __init__(self, text, color_fmt):
        self.__validate_color(color_fmt)
        self.__value = f'{color_fmt}{text}{constants.ENDC}'

    def __init__(self, pre_text, text, color_fmt):
        self.__validate_color(color_fmt)
        self.__value = f'{pre_text} {color_fmt}{text}{constants.ENDC}'


    def __validate_color(color_fmt):
        # Make sure color is a valid text color
        if color_fmt not in constants.COLORS:
            raise ValueError(f'Color {color_fmt} is not a valid color')

    def __str__(self):
        return self.__value