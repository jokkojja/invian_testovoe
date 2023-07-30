from pymongo import MongoClient
import os
from dotenv import load_dotenv

#load env
load_dotenv()

#config params
TTL = 0
MIN_TRESHHOLD = 0.2
NMS = 0

#database
MONGODB_ADDON_USER = os.environ['MONGODB_ADDON_USER']
MONGODB_ADDON_PASSWORD = os.environ['MONGODB_ADDON_PASSWORD']
MONGODB_ADDON_HOST = os.environ['MONGODB_ADDON_HOST']
MONGODB_ADDON_PORT=os.environ['MONGODB_ADDON_PORT']
MONGODB_ADDON_DB = os.environ['MONGODB_ADDON_DB']

CLIENT = MongoClient("mongodb://{}:{}@{}:{}/{}".format(MONGODB_ADDON_USER, MONGODB_ADDON_PASSWORD,
                                                       MONGODB_ADDON_HOST, MONGODB_ADDON_PORT, MONGODB_ADDON_DB))
MYDB = CLIENT[MONGODB_ADDON_DB]
MYCOL = MYDB.fire
