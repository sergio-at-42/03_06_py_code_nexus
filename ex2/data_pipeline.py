#!/usr/bin/env python3


from abc import ABC, abstractmethod
from typing import Any, Protocol


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


class ExportPlugin(Protocol):
    
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class ExportCsv():
    
    def process_output(self, data: list[tuple[int, str]]) -> None:
        csv_output: str = ",".join(list(d[1] for d in data))
        print("CSV Output:")
        print(csv_output)


class ExportJson():
    
    def process_output(self, data: list[tuple[int, str]]) -> None:
        json_output: dict[str, str] = {}
        for d in data:
            json_output["item_" + str(d[0])] = d[1]
        print("JSON Output:")
        print(json_output)


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
                print(f"Can't process element in stream: {s}")

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

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        list_for_plugin: list[tuple[int, str]] = []
        for proc in self.processors:
            nb_output:int = 0
            list_for_plugin.clear()
            while nb_output < nb and proc.data_list:
                list_for_plugin.append(proc.output())
                nb_output += 1
            plugin.process_output(list_for_plugin)


def data_pipeline() -> None:
    stream1: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [{"log_level": "WARNING",
          "log_message": "Telnet access! Use ssh instead"},
         {"log_level": "INFO",
          "log_message": "User wil is connected"}],
        42,
        ["Hi", "five"]
        ]
    stream2: list[Any] = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [{"log_level": "ERROR",
          "log_message": "500 server crash"},
         {"log_level": "NOTICE",
          "log_message": "Certificate expires in 10 days"}],
        [32, 42, 64, 84, 128, 168],
        "World hello"
    ]
    print("=== Code Nexus - Data Pipeline ===")
    print("")
    print("Initialize Data Stream...")
    print("")
    ds = DataStream()
    ds.print_processors_stats()
    print("Registering Processor")
    print("")
    np = NumericProcessor()
    tp = TextProcessor()
    lp = LogProcessor()
    ds.register_processor(np)
    ds.register_processor(tp)
    ds.register_processor(lp)
    print(f"Send first batch of data on stream: {stream1}")
    ds.process_stream(stream1)
    print("")
    ds.print_processors_stats()
    print("Send 3 processed data from each processor to a CSV plugin:")
    ds.output_pipeline(3, ExportCsv())
    print("")
    ds.print_processors_stats()
    print(f"Send another batch of data: {stream2}")
    ds.process_stream(stream2)
    print("")
    ds.print_processors_stats()
    print("Send 5 processed data from each processor to a JSON plugin:")
    ds.output_pipeline(5, ExportJson())
    print("")
    ds.print_processors_stats()


if __name__ == "__main__":
    data_pipeline()
