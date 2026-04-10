#!/usr/bin/env python3


from abc import ABC
from typing import Any


class DataProcessor(ABC):
    def validate(self, data: Any) -> bool:
        return (True)
        
    def ingest(self, data: Any) -> Any:
        return (data)


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        return (True)
        
    def ingest(self, data: Any) -> Any:
        return (data)


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        return (True)
        
    def ingest(self, data: Any) -> Any:
        return (data)


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        return (True)
        
    def ingest(self, data: Any) -> Any:
        return (data)


def data_processor() -> None:
    print("=== Code Nexus - Data Processor ===")
    print("")
    print("Testing Numeric Processor...")



if __name__ == "__main__":
    data_processor()
