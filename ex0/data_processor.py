#!/usr/bin/env python3


from abc import ABC, abstractmethod
from typing import Any


class ImproperNumericDataError(Exception):

    def __init__(self) -> None:
        super().__init__("Improper numeric data")


class ImproperTextDataError(Exception):

    def __init__(self) -> None:
        super().__init__("Improper text data")


class ImproperLogDataError(Exception):

    def __init__(self) -> None:
        super().__init__("Improper Log data")


class DataProcessor(ABC):

    def __init__(self) -> None:
        self.data_list: list[str] = []

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        return (0, self.data_list.pop(0) if len(self.data_list) else "")


class NumericProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        validate_ok: bool = True
        if not isinstance(data, (int, float, list)):
            validate_ok = False
        elif isinstance(data, list):
            for d in data:
                if validate_ok:
                    validate_ok = validate_ok and isinstance(d, (int, float))
        return (validate_ok)

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ImproperNumericDataError
        if isinstance(data, (list)):
            for d in data:
                self.data_list.append(str(d))
        else:
            self.data_list.append(str(data))


class TextProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        validate_ok: bool = True
        if not isinstance(data, (str, list)):
            validate_ok = False
        elif isinstance(data, list):
            for d in data:
                if validate_ok:
                    validate_ok = validate_ok and isinstance(d, (str))
        return (validate_ok)

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ImproperTextDataError
        if isinstance(data, (list)):
            for d in data:
                self.data_list.append(d)
        else:
            self.data_list.append(data)


class LogProcessor(DataProcessor):

    def validate_log(self, log_element: dict[str, str]) -> bool:
        return (
            isinstance(log_element, dict)
            and "log_level" in log_element
            and "log_message" in log_element
        )

    def validate(self, data: Any) -> bool:
        validate_ok: bool = True
        if not isinstance(data, (dict, list)):
            validate_ok = False
        elif isinstance(data, list):
            for d in data:
                if validate_ok:
                    validate_ok = validate_ok and self.validate_log(d)
        else:
            self.validate_log(data)
        return (validate_ok)

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ImproperLogDataError
        if isinstance(data, (list)):
            for d in data:
                self.data_list.append(f"{d["log_level"]}: {d["log_message"]}")
        else:
            self.data_list.append(
                f"{data["log_level"]}: {data["log_message"]}")


def data_processor() -> None:
    print("=== Code Nexus - Data Processor ===")
    print("")
    print("Testing Numeric Processor...")
    n1: int = 42
    n2: str = "Hello"
    n3: str = "foo"
    n4: list[float] = [1, 2, 3, 4, 5]
    nb_extract: int = 0
    np = NumericProcessor()
    print(f"Try to validate input '{n1}: '{np.validate(n1)}")
    print(f"Try to validate input '{n2}: '{np.validate(n2)}")
    print(f"Test invalid ingestion of string ’{n3}’ without prior validation:")
    try:
        np.ingest(n3)  # type: ignore
    except ImproperNumericDataError as e:
        print(f"Got exception: {e}")
    print(f"Processing data: {n4}")
    np.ingest(n4)
    nb_extract = 3
    print(f"Extracting {nb_extract} values...")
    for i in range(nb_extract):
        print(f"Numeric value {i}: {np.output()[1]}")
    print("")
    print("Testing Text Processor...")
    t1: int = 42
    t2: list[str] = ["Hello", "Nexus", "World"]
    t3: float = 3.14
    tp = TextProcessor()
    print(f"Try to validate input '{t1}: '{tp.validate(t1)}")
    print(f"Test invalid ingestion of float ’{t3}’ without prior validation:")
    try:
        tp.ingest(t1)  # type: ignore
        tp.ingest(t3)  # type: ignore
    except ImproperTextDataError as e:
        print(f"Got exception: {e}")
    print(f"Processing data: {t2}")
    tp.ingest(t2)
    nb_extract = 1
    print(f"Extracting {nb_extract} values...")
    for i in range(nb_extract):
        print(f"Text value {i}: {tp.output()[1]}")
    print("")
    print("Testing Log Processor...")
    l1: str = "Hello"
    l2: list[dict[str, str]] = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"}]
    l3: float = 3.14
    lp = LogProcessor()
    print(f"Try to validate input '{l1}: '{lp.validate(l1)}")
    print(f"Test invalid ingestion of float ’{l3}’ without prior validation:")
    try:
        lp.ingest(l3)  # type: ignore
    except ImproperLogDataError as e:
        print(f"Got exception: {e}")
    print(f"Processing data: {l2}")
    lp.ingest(l2)
    nb_extract = 2
    print(f"Extracting {nb_extract} values...")
    for i in range(nb_extract):
        print(f"Log entry {i}: {lp.output()[1]}")
    print("")


if __name__ == "__main__":
    data_processor()
