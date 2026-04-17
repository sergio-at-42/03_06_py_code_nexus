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
        self.data_list: dict[int, str] = {}
        self.older: int = 0
        self.count_ingest: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        raise NotImplementedError

    @abstractmethod
    def ingest(self, data: Any) -> None:
        raise NotImplementedError

    def output(self) -> tuple[int, str]:
        data_output: tuple[int, str]
        if len(self.data_list):
            data_output = (self.older, self.data_list.pop(self.older))
            self.older += 1
        else:
            data_output = (0, "")
        return (data_output)


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
                self.data_list[self.count_ingest] = str(d)
                self.count_ingest += 1
        else:
            self.data_list[self.count_ingest] = str(data)
            self.count_ingest += 1


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
                self.data_list[self.count_ingest] = d
                self.count_ingest += 1
        else:
            self.data_list[self.count_ingest] = data
            self.count_ingest += 1


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
                self.data_list[self.count_ingest] = (
                    f"{d["log_level"]}: {d["log_message"]}")
                self.count_ingest += 1
        else:
            self.data_list[self.count_ingest] = (
                f"{data["log_level"]}: {data["log_message"]}")
            self.count_ingest += 1


class DataStream():

    def __init__(self) -> None:
        self.processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        if isinstance(proc, DataProcessor):
            self.processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        stream_not_find: bool = True
        for s in stream:
            stream_not_find = True
            for p in self.processors:
                if p.validate(s):
                    p.ingest(s)
                    stream_not_find = False
            if stream_not_find:
                print("DataStream error", end=" - ")
                print(f"Can’t process element in stream: {s}")

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if self.processors:
            for p in self.processors:
                print(type(p).__name__.replace("Proc", " Proc"), end=": ")
                print(f"total {p.count_ingest} items processed", end=", ")
                print(f"remaining {len(p.data_list)} on processor")
        else:
            print("No processor found, no data")
        print("")


def data_stream() -> None:
    stream: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [{"log_level": "WARNING",
          "log_message": "Telnet access! Use ssh instead"},
         {"log_level": "INFO",
          "log_message": "User wil is connected"}],
        42,
        ["Hi", "five"]
        ]
    print("=== Code Nexus - Data Stream ===")
    print("")
    print("Initialize Data Stream...")
    ds = DataStream()
    ds.print_processors_stats()
    print("Registering Numeric Processor")
    np = NumericProcessor()
    ds.register_processor(np)
    print(f"Send first batch of data on stream: {stream}")
    ds.process_stream(stream)
    ds.print_processors_stats()
    print("Registering other data processors")
    tp = TextProcessor()
    lp = LogProcessor()
    ds.register_processor(tp)
    ds.register_processor(lp)
    print("Send the same batch again")
    ds.process_stream(stream)
    ds.print_processors_stats()
    print("Consume some elements from the data processors:", end=" ")
    i: int = 0
    for i in range(3):
        np.output()
    print(f"Numeric {i + 1}", end=", ")
    for i in range(2):
        tp.output()
    print(f"Text {i + 1}", end=", ")
    for i in range(1):
        lp.output()
    print(f"log {i + 1}")
    ds.print_processors_stats()


if __name__ == "__main__":
    data_stream()
