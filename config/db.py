#Este archivo tendra la conexion a la bd
############################################################
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker


engine = create_engine("mysql+pymysql://viguel:Aa3ETkC2W1QXkVL1@localhost:3306/apio")

# SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

# Base = declarative_base()

meta_data = MetaData()

 