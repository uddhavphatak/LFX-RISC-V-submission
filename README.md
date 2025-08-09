# RISC-V YAML ↔ C Header Round-Trip Conversion

## Overview

This submission demonstrates a **two-way data transformation pipeline** between
the [RISC-V Unified Database](https://github.com/riscv-software-src/riscv-unified-db) 
YAML instruction specifications and generated C header files.

The pipeline proves *round-trip stability*:  
- Starting from an official instruction YAML file.  
- Converting to a C header representation.  
- Emitting the C header contents back to YAML.  
- Repeating the process with the generated YAML.  

On the second round, the YAML output matches exactly with the second-round input, 
showing the transformation process is lossless for the simplified format.

---
## Problem Statement

**Goal:**  
1. Read one of the YAML instruction files from `spec/std/isa/inst` in the RISC-V Unified Database.  
2. Emit the data as a C header file in a chosen format.  
3. Write a C program that includes the generated header and emits the data as YAML.  
4. Repeat the steps using the generated YAML as input.  
5. Verify that in the second round, the YAML output matches the YAML input exactly.

---

## Implementation Details

### Languages & Tools
- **Python 3** – Parses YAML and generates C headers.
- **PyYAML** – Used for YAML parsing and serialization.
- **C (C99)** – Consumes the generated header and prints YAML.
- **Makefile** – Automates the full two-round process and comparison.

### Workflow
1. **First Round**
   - Python script (`yaml_to_c.py`) reads the original RISC-V YAML file.
   - Generates:
     - `C_header.h` – a C header with static arrays of key-value instruction data.
     - `generated.yaml` – YAML regenerated from the C header (simplified form).
   - C program (`C_header.h`) includes `C_header.h` and emits its contents in YAML → `emitted.yaml`.

2. **Second Round**
   - Python reads `emitted.yaml`.
   - Generates:
     - New `C_header.h`.
     - `re-generated.yaml`.
   - C program emits → `re-emitted.yaml`.

3. **Verification**
   - The Makefile compares `re-generated.yaml` and `re-emitted.yaml`.
   - They should match exactly, proving stable round-trip.

---

## File Descriptions

| File            | Description |
|-----------------|-------------|
| `yaml_to_c.py`  | Python script for YAML ↔ C header conversion. |
| `C_header.h`    | C program that reads generated C header and prints it as YAML. |
| `Makefile`      | Automates both conversion rounds and performs output comparison. |
| `README.md`     | Project documentation. |

---

## How to Run

### Prerequisites
- Python 3 with PyYAML:
  ```bash
  pip install pyyaml
