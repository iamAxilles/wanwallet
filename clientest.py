
from sqlmodel import Field, Session, SQLModel, create_engine, select

from fastapi import APIRouter, FastAPI

import os, json, pytest
 
import toke
from toke import app
# from dotenv import load_dotenv

# load_dotenv()
from fastapi.testclient import TestClient
from contextlib import asynccontextmanager 



def test_create_hero():

        cli = TestClient(app) 
        # with TestClient(ap) as client: 

        response = cli.get("/transfers")

        data = response.json()

        assert response.status_code == 200  
        assert "token_name" in data[0]   
        assert any("log_index" in row for row in data) is not None
  

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
# baza = "postgresql://VNR@localhost:5432/wallet"
baza = "postgresql://baza_ew62_user:eSORUmw29D5y5Q54lpnXSTYEtNQrcLpN@dpg-datait59fdbs738c4hvg-a.singapore-postgres.render.com/baza_ew62"
engine = create_engine(baza, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def test_database_connection():
    with Session(engine) as session:
        result = session.execute(text("SELECT 1")).scalar_one()
        assert result == 1

def test_balance_col():
    with Session(engine) as session:
        result = session.execute(text("SELECT * FROM tokens LIMIT 0"))
        assert "balance" in result.keys()









