from abc import ABC, abstractmethod

from bugfixpy.utils.text import colors, headers, Text


class RunnableMode(ABC):

    test_mode = bool

    def __init__(self, test_mode=False) -> None:
        self.test_mode = test_mode

    def start(self) -> None:
        self.display_headers()
        self.run()
        self.display_results()

    def display_headers(self) -> None:
        if self.test_mode:
            Text(headers.TEST_MODE, colors.HEADER).display()

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def display_results(self) -> None:
        pass
