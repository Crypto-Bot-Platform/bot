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
    },
    { "name": "context", "type": {
        "type": "record",
        "name": "context",
        "fields": [
            {"name": "exchange", "type": "string"},
            {"name": "pair", "type": "string"}
        ]
    }}    
  ]
}
"""