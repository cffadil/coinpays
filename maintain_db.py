import time

from sqlalchemy.engine import create_engine

url = 'mysql+mysqlconnector://root:@localhost:3306/coinpays'
engine = create_engine(url, pool_recycle=1)

query = 'SELECT NOW();'

while True:
    print('Q1', engine.execute(query).fetchall())
    engine.execute('SET wait_timeout=2')
    time.sleep(3)
    print('Q2', engine.execute(query).fetchall())