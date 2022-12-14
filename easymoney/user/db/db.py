from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine('postgresql://znectdjz:la53JfV0KdHyLHy-9mosvm74pL_c2JJL@tiny.db.elephantsql.com/znectdjz')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()
