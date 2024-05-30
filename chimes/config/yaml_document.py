import yaml


def document_property(name, details, indent=0):
    lines = []
    prop_type = details.get('type', 'N/A')
    default = details.get('default', 'No default value provided')
    description = details.get('description', 'Description not provided.')

    # Format the default value for complex types
    if isinstance(default, (dict, list)):
        default = yaml.dump(default, default_flow_style=True).strip()

    indent_str = '    ' * indent
    lines.append(f"{indent_str}- **{name}**")
    lines.append(f"{indent_str}  - **Type:** `{prop_type}`")
    lines.append(f"{indent_str}  - **Default:** `{default}`")
    lines.append(f"{indent_str}  - **Description:** {description}")

    return lines


def generate_documentation(schema_path, output_path):
    with open(schema_path, 'r') as file:
        schema = yaml.safe_load(file)

    properties = schema.get('properties', {})
    documentation_lines = [
        "# Configuration Schema Documentation",
        "\n## Configuration Options\n"
    ]

    for prop, details in properties.items():
        documentation_lines.extend(document_property(prop, details))

    documentation = "\n".join(documentation_lines)

    with open(output_path, 'w') as output_file:
        output_file.write(documentation)

    print(f"Documentation generated at {output_path}")


# Specify the path to your schema and where you want the documentation to be saved
schema_path = 'config_schema.yml'
output_path = 'CONFIG_SCHEMA_DOCUMENTATION.md'

generate_documentation(schema_path, output_path)
