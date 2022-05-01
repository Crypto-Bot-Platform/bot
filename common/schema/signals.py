SignalsSchema = """
{
  "namespace": "confluent.io.examples.serialization.avro",
  "name": "SignalRecord",
  "type": "record",
  "fields": [
    {"name": "timestamp", "type": "long", "logicalType": "timestamp-millis"},
    {
      "name": "indicators",
      "type": {
        "type": "array",
        "items": {
          "type": "record",
          "name": "indicator",
          "fields": [
            {
              "name": "name",
              "type": "string"
            },
            {
              "name": "value",
              "type": "float"
            }
          ]
        }
      }
    }
  ]
}
"""