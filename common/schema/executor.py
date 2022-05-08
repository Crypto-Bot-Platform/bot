ExecutorSchema = """
{
  "namespace": "confluent.io.examples.serialization.avro",
  "name": "ExecuteRecord",
  "type": "record",
  "fields": [
    {"name": "timestamp", "type": "long", "logicalType": "timestamp-millis"},
    {"name": "exchange", "type": "string"},
    {"name": "symbol", "type": "string"},
    {"name": "side", "type": "string"},
    {"name": "type", "type": "string"},
    {"name": "amount", "type": "float"},
    {"name": "price", "type": ["null", "float"], "default": null}
  ]
}
"""