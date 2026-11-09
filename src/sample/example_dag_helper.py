import pandera.pandas as pa

class User(pa.DataFrameModel):
    id: int
    name: str
    age: int
    class Config:  # pyright: ignore [reportIncompatibleVariableOverride]
        strict = True
        coerce = False

class AvgAge(pa.DataFrameModel):
    avg_age: float
    class Config: # pyright: ignore [reportIncompatibleVariableOverride]
        strict = True
        coerce = False
