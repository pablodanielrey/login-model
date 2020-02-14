
def create_tables():
    import os
    from sqlalchemy import create_engine
    from .entities import Base
    from .entities.Login import UsuarioClave, LoginLog, Device, UserHash, UserPositionLog

    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
        os.environ['DB_USER'],
        os.environ['DB_PASSWORD'],
        os.environ['DB_HOST'],
        os.environ.get('DB_PORT',5432),
        os.environ['DB_NAME']
    ), echo=True)
    Base.metadata.create_all(engine)


create_tables()