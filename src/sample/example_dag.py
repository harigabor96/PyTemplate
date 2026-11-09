from dataclasses import dataclass

@dataclass
class ExampleConf:
    source_string: str

class ExampleDAG:
    def __init__(self, conf: ExampleConf): self.conf = conf

    def execute(self) -> None:
        source_data = self.extract_source()
        sink_data = self.transform_sink(source_data)
        self.load_sink(sink_data)

    def extract_source(self) -> str:
        return self.conf.source_string

    def transform_sink(self, source_data: str) -> str:
        return source_data + " POTATOO!"

    def load_sink(self, sink_data: str) -> None:
        print(sink_data)

if __name__ == "__main__":
    ExampleDAG(
        conf = ExampleConf(
            source_string = "CARRRROT!"
        )
    ).execute()
