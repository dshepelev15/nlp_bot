import os

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from aiocqlengine.session import aiosession_for_cqlengine
from cassandra.cluster import Cluster
from cassandra.cqlengine import connection, management

from utils import config
from utils.models import CharacterUserHistory, ChatMessage

KEYSPACE = 'chat_messages'


def create_session():
    auth_provider = PlainTextAuthProvider(username=config.CASSANDRA_USER, password=config.CASSANDRA_PASSWORD)

    cluster = Cluster(config.CASSANDRA_NODES, auth_provider=auth_provider)
    session = cluster.connect()

    # Create keyspace, if already have keyspace your can skip this
    os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = 'true'
    connection.register_connection('cqlengine', session=session, default=True)

    management.create_keyspace_simple(KEYSPACE, replication_factor=1)
    management.sync_table(ChatMessage, keyspaces=[KEYSPACE])
    management.sync_table(CharacterUserHistory, keyspaces=[KEYSPACE])

    # Wrap cqlengine connection
    aiosession_for_cqlengine(session)
    session.set_keyspace(KEYSPACE)
    connection.set_session(session)
    return session
