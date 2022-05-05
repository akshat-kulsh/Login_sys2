from models import *
import pandas as pd
from flask import request, jsonify
import json

def mk_session(fun):
    def wrapper(*args, **kwargs):
        s = session()
        kwargs['session'] = s
        try:
            res = fun(*args, **kwargs)
        except Exception as e:
            s.rollback()
            s.close()
            raise e

        s.close()
        return res
    wrapper.__name__ = fun.__name__
    return wrapper

@mk_session
def dbGetUserByEmail(email, session=None):
    query = session.query(User).filter(User.email== email).statement
    df = pd.read_sql( query, engine)
    print(df)
    if(not df.empty):
        return df.at[0,'idusers'], df.at[0, 'pssword']

@mk_session
def dbGetUser(email, session=None):
    query = session.query(User).filter(User.email== email).statement
    df = pd.read_sql( query, engine)
    print(df)
    if(not df.empty):
        return df.at[0,'idusers']

@mk_session
def dbSaveAdUnit(data, user_id, session=None):
    save_ad = adUnit(page_name=data['page_name'], adUnitSize=data['adUnitSize'], adLink=data['adLink'], user_id= user_id )
    session.add(save_ad)
    session.commit()


@mk_session
def dbLoadAdUnit(page_name, session=None):
    query =  session.query(adUnit).filter(adUnit.page_name==page_name).statement
    df = pd.read_sql(query,engine)
    print(df)
    return jsonify({"adUnitSize": df.at[0,'adUnitSize'], "adLink": df.at[0, 'adLink']})
    
@mk_session
def dbEmptyLoadAdUnit(session=None):
    query = session.query(adUnit).statement
    df = pd.read_sql(query,engine)
    sample_dict = df.set_index('id')[['page_name','adUnitSize','adLink']].to_dict(orient='index')
    print(list(sample_dict.values()))
    x = json.dumps(list(sample_dict.values()))
    print(x)
    return(x)