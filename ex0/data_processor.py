#!/usr/bin/env python3


from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        return ()


class NumericProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        return (isinstance(data, int))
        
    def ingest(self, data: Any) -> Any:
        return (data)


class TextProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        return (isinstance(data, str))
        
    def ingest(self, data: Any) -> Any:
        return (data)


class LogProcessor(DataProcessor):
    
    def validate(self, data: Any) -> bool:
        return (isinstance(data, int))
        
    def ingest(self, data: Any) -> Any:
        return (data)


def data_processor() -> None:
    print("=== Code Nexus - Data Processor ===")
    print("")
    print("Testing Numeric Processor...")



if __name__ == "__main__":
    data_processor()
