# import json
import yaml
from jsonschema import validate, ValidationError


# with open('config_schema.json', 'r') as schema_file:
#     schema = json.load(schema_file)

# with open('../config.json', 'r') as some_config_file:
#     config = json.load(some_config_file)

# try:
#     validate(instance=config, schema=schema)
#     print("Configuration is valid.")
# except ValidationError as e:
#     print("Configuration is invalid:", e)


with open('config_schema.yml', 'r') as schema_file:
    schema = yaml.safe_load(schema_file)

with open('../config.yml', 'r') as some_config_file:
    config = yaml.safe_load(some_config_file)

try:
    validate(instance=config, schema=schema)
    print("Configuration is valid.")
except ValidationError as e:
    print("Configuration is invalid:", e)
