# All SQLAlchemy models placed here for model preloading.
# db_session.py can reference this one file, and eliminates
# the need to muck around in the global init.

# noinspection PyUnresolvedReferences
import src.db_models.users
# noinspection PyUnresolvedReferences
import src.db_models.unregistered_users
# noinspection PyUnresolvedReferences
import src.db_models.completions
