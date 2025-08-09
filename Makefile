PYTHON = python3
PY_SCRIPT = yaml_to_c.py
C_PROG = emit_yaml
C_SRC = emit_yaml.c
HEADER = C_header.h

YAML_INPUT = addi.yaml
GEN1_YAML = generated.yaml
EMIT1_YAML = emitted.yaml

GEN2_YAML = re-generated.yaml
EMIT2_YAML = re-emitted.yaml

all: first_round second_round

first_round: $(YAML_INPUT) $(PY_SCRIPT) $(C_SRC)
	$(PYTHON) $(PY_SCRIPT) $(YAML_INPUT) $(HEADER) $(GEN1_YAML)
	$(CC) $(C_SRC) -o $(C_PROG)
	./$(C_PROG) > $(EMIT1_YAML)
	@echo "First round complete. Files: $(HEADER), $(GEN1_YAML), $(EMIT1_YAML)"

second_round: $(GEN1_YAML) $(PY_SCRIPT) $(C_SRC)
	$(PYTHON) $(PY_SCRIPT) $(GEN1_YAML) $(HEADER) $(GEN2_YAML)
	$(CC) $(C_SRC) -o $(C_PROG)
	./$(C_PROG) > $(EMIT2_YAML)
	@echo "Second round complete. Files: $(HEADER), $(GEN2_YAML), $(EMIT2_YAML)"
	@diff -u $(GEN2_YAML) $(EMIT2_YAML) && echo "Second round YAMLs match!" || echo "Mismatch!"

clean:
	rm -f $(HEADER) $(C_PROG) $(GEN1_YAML) $(EMIT1_YAML) $(GEN2_YAML) $(EMIT2_YAML)

.PHONY: all first_round second_round clean

