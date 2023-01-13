from abc import ABC, abstractmethod

from bugfixpy.utils.text import colors, headers


class RunnableMode(ABC):

    __mode: str
    __test_mode: bool

    def __init__(self, mode, test_mode=False) -> None:
        self.__mode = mode
        self.__test_mode = test_mode

    def get_mode(self) -> str:
        return self.__mode

    def get_test_mode(self) -> bool:
        return self.__test_mode

    def start(self) -> None:
        self.display_headers()
        self.run()
        self.display_results()

    def display_headers(self) -> None:
        print(colors.HEADER, "### MODE: ", self.__mode, colors.ENDC, sep="")
        if self.__test_mode:
            print(colors.HEADER, headers.TEST_MODE, sep="")

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def display_results(self) -> None:
        pass
