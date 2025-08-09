#!/usr/bin/env python3
import sys
import yaml
import re


def escape_c_string(s: str) -> str:
    """
    Escape string so it can be put safely into a C string literal.
    Multiline strings will be split into multiple quoted lines.
    """
    s = s.replace("\\", "\\\\")   # escape backslash
    s = s.replace("\"", "\\\"")   # escape quote
    s = s.replace("\r\n", "\n")   # normalizing
    s = s.replace("\r", "\n")
    lines = s.split("\n")
    return "\"{}\"".format("\\n\"\n\"".join(lines))


def yaml_to_c_header(yaml_path: str, header_path: str):
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError("YAML root must be a mapping")

    entries = list(data.items())
    inst_count = len(entries)

    with open(header_path, "w", encoding="utf-8") as out:
        out.write("#pragma once\n")
        out.write("#include <stddef.h>\n\n")
        out.write("typedef struct {\n")
        out.write("    const char *key;\n")
        out.write("    const char *value;\n")
        out.write("} inst_entry_t;\n\n")
        out.write(f"#define INST_COUNT {inst_count}\n\n")
        out.write(f"static const inst_entry_t INST_DATA[INST_COUNT] = {{\n")
        for k, v in entries:
            if not isinstance(v, str):
                v = str(v)
            out.write(f"    {{\"{k}\", {escape_c_string(v)}}},\n")
        out.write("};\n")


def c_header_to_yaml(header_path: str, yaml_path: str):
    """
    Reads back the C header produced by yaml_to_c_header into a YAML file.
    Assumes the header matches the generated format exactly.
    """
    with open(header_path, "r", encoding="utf-8") as f:
        content = f.read()

    # regex to match {"key", "value"} pairs
    pattern = r'\{\s*"([^"]+)"\s*,\s*"((?:[^"\\]|\\.)*)"\s*\}'
    matches = re.findall(pattern, content)

    yaml_data = {}
    for k, v in matches:
        v = v.replace("\\n", "\n").replace("\\\"", "\"").replace("\\\\", "\\")
        yaml_data[k] = v

    with open(yaml_path, "w", encoding="utf-8") as out:
        yaml.safe_dump(yaml_data, out, sort_keys=False)


def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <input.yaml> <output.h> <regen.yaml>")
        sys.exit(1)

    yaml_in = sys.argv[1]
    header_out = sys.argv[2]
    yaml_out = sys.argv[3]

    yaml_to_c_header(yaml_in, header_out)
    c_header_to_yaml(header_out, yaml_out)


if __name__ == "__main__":
    main()

