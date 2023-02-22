#Este archivo tendra la conexion a la bd
############################################################
from sqlalchemy import create_engine, MetaData
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import select


engine = create_engine("mysql+pymysql://viguel:Aa3ETkC2W1QXkVL1@localhost:3306/apio", echo=True)

# session = Session(engine)

# SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

# Base = declarative_base()

meta_data = MetaData()

 