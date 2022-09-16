import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.db_models.base_model import SqlAlchemyBase

__factory = None


def global_init(db_file: str):
    global __factory

    # if factory has already been called, no need to call it again, so return
    if __factory:
        return

    # validate db_file is not whitespace or omitted altogether
    if not db_file or not db_file.strip():
        raise Exception('You must specify a db file.')

    # specify the db dialect and the database API
    connection_str = db_file.strip()

    # sqlalchemy engine
    engine = sa.create_engine(connection_str, echo=False, connect_args={"check_same_thread": False})  # set echo=True to see what sqlalchemy is doing

    # Create the session and reference the engine
    __factory = orm.sessionmaker(bind=engine)

    # noinspection PyUnresolvedReferences
    import src.db_models.__all_models

    SqlAlchemyBase.metadata.create_all(engine)


# noinspection PyCallingNonCallable
def create_session() -> orm.Session:
    global __factory

    session: orm.Session = __factory()
    session.expire_on_commit = False

    return session
