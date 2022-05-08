import uuid
from os import environ


def parse_environ(component: str):
    if 'BOT_ID' not in environ:
        environ['BOT_ID'] = "temp-" + str(uuid.uuid4())
    bot_id = environ['BOT_ID']
    kafka_host = environ['KAFKA_HOST'] if 'KAFKA_HOST' in environ else "localhost"
    kafka_port = environ['KAFKA_PORT'] if 'KAFKA_PORT' in environ else "9092"
    elastic_host = environ['ELASTIC_HOST'] if "ELASTIC_HOST" in environ else "localhost"
    elastic_port = environ['ELASTIC_PORT'] if "ELASTIC_PORT" in environ else "9200",
    mongo_host = environ['MONGODB_HOST'] if 'MONGODB_HOST' in environ else "localhost"
    mongo_port = environ['MONGODB_PORT'] if 'MONGODB_PORT' in environ else "27017"
    db_name = environ['SQLDB_NAME'] if 'SQLDB_NAME' in environ else "cbp"
    db_user = environ['SQLDB_USER'] if 'SQLDB_USER' in environ else "cbp_user"
    db_pass = environ['SQLDB_PASS'] if 'SQLDB_PASS' in environ else "Password1234"
    db_host = environ['SQLDB_HOST'] if 'SQLDB_HOST' in environ else "localhost"
    db_port = environ['SQLDB_PORT'] if 'SQLDB_PORT' in environ else "5432"
    my_vars = dict([(k, environ[k]) for k in environ if k in ['BOT_ID', 'KAFKA_HOST', 'KAFKA_PORT', "ELASTIC_HOST",
                                                              "ELASTIC_PORT", "MONGODB_HOST", "MONGODB_PORT",
                                                              "SQLDB_NAME", "SQLDB_USER", "SQLDB_PASS", "SQLDB_HOST",
                                                              "SQLDB_PORT"]])
    print(f"*** {component}: Environment variables: {my_vars}")
    return {
        "bot_id": bot_id,
        "kafka_host": kafka_host,
        "kafka_port": kafka_port,
        "elastic_host": elastic_host,
        "elastic_port": elastic_port[0] if type(elastic_port) == tuple else elastic_port,
        "mongo_host": mongo_host,
        "mongo_port": mongo_port,
        "db_name": db_name,
        "db_user": db_user,
        "db_pass": db_pass,
        "db_host": db_host,
        "db_port": db_port
    }
