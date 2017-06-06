from sqlalchemy import create_engine
engine = create_engine("sqlite:///:memory:")

from qversions._db import Base
Base.metadata.create_all(engine)
