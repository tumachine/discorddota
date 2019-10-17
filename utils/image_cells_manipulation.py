from typing import List

from abc import ABC, abstractmethod

from PIL import ImageDraw
from PIL import ImageFont

from utils.util import get_full_path


class CellPosition:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.end_x = self.width + self.x
        self.end_y = self.height + self.y

    def get_xy_to_center_element(self, el_width: int, el_height: int):
        return self.x + (self.width - el_width) // 2, self.y + (self.height - el_height) // 2


class CellPositionGenerator:
    def __init__(self, x_start: int, y_start: int,
                 columns: List[int], column_spaces: List[int],
                 rows: List[int], row_spaces: List[int]):
        cells: List[CellPosition] = []
        self.columns_len = len(columns)
        self.rows_len = len(rows)

        y = y_start
        for row in range(self.rows_len):
            y += row_spaces[row]
            height = rows[row]
            x = x_start
            for column in range(self.columns_len):
                x += column_spaces[column]
                width = columns[column]
                cells.append(CellPosition(width, height, x, y))
                x += width
            y += height

        self.cells = cells


class Cell(ABC):
    @abstractmethod
    def draw(self, image_on, cell_position: CellPosition):
        pass


class ImageCell(Cell):
    def __init__(self, image, **kwargs):
        self.image = image
        self.rules = kwargs

    def draw(self, image_on, cell_position: CellPosition):
        if self.image is None:
            return

        if 'centered' not in self.rules:
            centered = True
        else:
            centered = self.rules['centered']

        if 'raw' not in self.rules:
            raw = False
        else:
            raw = self.rules['raw']

        if raw:
            self.image.resize((cell_position.width, cell_position.height))
        else:
            self.image.thumbnail((cell_position.width, cell_position.height))

        if centered:
            x, y = cell_position.get_xy_to_center_element(self.image.width, self.image.height)
        else:
            x, y = cell_position.x, cell_position.y
        image_on.paste(self.image, (x, y, x + self.image.width, y + self.image.height), self.image.convert("RGBA"))


class ColorCell(Cell):
    def __init__(self, color, **kwargs):
        self.color = color
        self.rules = kwargs

    def draw(self, image_on, cell_position: CellPosition):
        image_on.paste(self.color, (cell_position.x, cell_position.y, cell_position.end_x, cell_position.end_y))


class TextCell(Cell):
    def __init__(self, text, **kwargs):
        self.text = text
        self.rules = kwargs

    def draw(self, image_on, cell_position: CellPosition):
        text = str(self.text)
        if 'centered' not in self.rules:
            centered = True
        else:
            centered = self.rules['centered']

        if 'font_size' not in self.rules:
            font_size = 16
        else:
            font_size = self.rules['font_size']

        if 'font_color' not in self.rules:
            font_color = (255, 255, 255)
        else:
            font_color = self.rules['font_color']

        if 'font_opacity' not in self.rules:
            font_opacity = 256
        else:
            font_opacity = self.rules['font_opacity']

        if 'font_name' not in self.rules:
            font_name = 'Roboto-Medium.ttf'
        else:
            font_name = self.rules['font_name']

        fnt = ImageFont.truetype(get_full_path('fonts', font_name), font_size)
        draw = ImageDraw.Draw(image_on)
        w, h = draw.textsize(text, font=fnt)
        if centered:
            draw.text(cell_position.get_xy_to_center_element(w, h), text, font=fnt, fill=font_color + (font_opacity,))
        else:
            draw.text((cell_position.x, cell_position.y), text, font=fnt, fill=font_color + (font_opacity,))


class CellLines:
    def __init__(self, cells_positions: CellPositionGenerator):
        self.cell_positions = []
        self.positions = cells_positions

    def draw(self, td_cell_list: List[List], img):
        for i in range(len(self.cell_positions)):
            self.draw_line(self.cell_positions[i], td_cell_list[i], img)
        return img

    def draw_line(self, cell_positions: List[CellPosition], cell_list: List[Cell], img):
        for i in range(len(cell_positions)):
            if cell_list[i] is None:
                continue
            cell_list[i].draw(img, cell_positions[i])


class VerticalCellLines(CellLines):
    def __init__(self, cells_positions: CellPositionGenerator):
        super().__init__(cells_positions)

        for x in range(self.positions.columns_len):
            column = []
            for y in range(self.positions.rows_len):
                column.append(self.positions.cells[x + y * self.positions.columns_len])
            self.cell_positions.append(column)


class HorizontalCellLines(CellLines):
    def __init__(self, cells_positions: CellPositionGenerator):
        super().__init__(cells_positions)

        for y in range(cells_positions.rows_len):
            column = []
            for x in range(cells_positions.columns_len):
                column.append(self.positions.cells[y * cells_positions.columns_len + x])
            self.cell_positions.append(column)
