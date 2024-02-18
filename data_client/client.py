from typing import Optional
from sqlmodel import SQLModel, Field, create_engine, Session
from datetime import datetime


class ClientPI(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client_name: Optional[str] = Field(default="Anyone")
    hs_code: Optional[str] = Field(default=None)

    ammount: Optional[float]
    price_unit: Optional[float]
    cbm: Optional[float]
    total_kg: Optional[float]
    real: Optional[bool] = Field(default=True)

    fob: float
    cif: float

    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    __table_args__ = {"extend_existing": True}


class ClientPITaxes(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    client_name: Optional[str] = Field(default="Anyone")
    hs_code: Optional[str] = Field(default=None)

    ad_valorem: float
    igv: float
    ipm: float
    antidupping: float
    insurage: float
    perception: float

    total_taxes: float
    real: bool


class TaxesValues(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    client_name: Optional[str] = Field(default="Anyone")
    hs_code: Optional[str] = Field(default=None)

    hs_code: Optional[str] = Field(default=None)
    v_ad_valorem: float
    v_igv: float
    v_ipm: float
    v_antidupping: float
    v_perception: float
    v_insurage: float


class LogisticCost(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    client_name: Optional[str] = Field(default="Anyone")
    hs_code: Optional[str] = Field(default=None)

    freight: float
    transport_local: float

    province_transport: float
    desconsolidation: float

    total_logistic: float


sqlite_file_name = "clients.sqlite"
sqlite_url = f"sqlite:///./data/{sqlite_file_name}"


engine = create_engine(sqlite_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def add_row(value):
    db = Session(engine)
    db.add(value)
    db.commit()
    return value


if __name__ == "__main__":
    create_db_and_tables()
