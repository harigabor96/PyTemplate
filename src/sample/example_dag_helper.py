import pandera.pandas as pa

class User(pa.DataFrameModel):
    id: int
    name: str
    age: int

class AvgAge(pa.DataFrameModel):
    avg_age: int
