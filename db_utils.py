import pymongo
import pandas as pd
import streamlit as st

class MongoDBClient:
    def __init__(self, db_name = "fixed_fortune", collection_name = "risk_data"):
        self.client = pymongo.MongoClient('mongodb://localhost:27017')
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def saveRiskData(self, risk_data):
        if len(list(self.collection.find())) != 0:
            self.collection.delete_many({})
        risk_data.insert(0, "_id", risk_data.index, True)
        self.collection.insert_many(risk_data.to_dict('records'))

    def get_risk_data(self, bond_name):
        return self.collection.find_one({'asset_id': bond_name}, {'_id': 0})


