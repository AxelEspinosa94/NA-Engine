# ============================
# NA-Engine Release Automation
# ============================

ifeq ($(OS),Windows_NT)
WSL := wsl
PY := python.exe
PIP := pip.exe
else
WSL :=
PY := python3
PIP := pip3
endif

# Get latest tag (e.g., v0.1.1)
CURRENT_TAG := $(shell git describe --tags --abbrev=0)

# Extract numeric version (remove leading "v")
VERSION := $(subst v,,$(CURRENT_TAG))

# Split version into components
MAJOR := $(word 1,$(subst ., ,$(VERSION)))
MINOR := $(word 2,$(subst ., ,$(VERSION)))
PATCH := $(word 3,$(subst ., ,$(VERSION)))

ifeq ($(OS),Windows_NT)
INC_PATCH = $(shell powershell -Command "$(PATCH) + 1")
INC_MINOR = $(shell powershell -Command "$(MINOR) + 1")
else
INC_PATCH = $(shell echo $$(($(PATCH)+1)))
INC_MINOR = $(shell echo $$(($(MINOR)+1)))
endif

NEXT_PATCH := $(INC_PATCH)
NEXT_PATCH_TAG := v$(MAJOR).$(MINOR).$(NEXT_PATCH)

NEXT_MINOR := $(INC_MINOR)
NEXT_MINOR_TAG := v$(MAJOR).$(NEXT_MINOR).0

# ============================
# Commands
# ============================

# Create a PATCH release (0.x.(y+1))
release-patch:
	@echo "Current tag: $(CURRENT_TAG)"
	@echo "Next patch tag: $(NEXT_PATCH_TAG)"
	git tag -a $(NEXT_PATCH_TAG) -m "Release $(NEXT_PATCH_TAG)"
	git push origin $(NEXT_PATCH_TAG)
	@echo "Patch release created."

# Create a MINOR release (0.(x+1).0)
release-minor:
	@echo "Current tag: $(CURRENT_TAG)"
	@echo "Next minor tag: $(NEXT_MINOR_TAG)"
	git tag -a $(NEXT_MINOR_TAG) -m "Release $(NEXT_MINOR_TAG)"
	git push origin $(NEXT_MINOR_TAG)
	@echo "Minor release created."

release-patch-dry:
	@echo "Current tag: $(CURRENT_TAG)"
	@echo "Next patch tag: $(NEXT_PATCH_TAG)"
	@echo "[DRY RUN] Would run: git tag -a $(NEXT_PATCH_TAG) -m 'Release $(NEXT_PATCH_TAG)'"
	@echo "[DRY RUN] Would run: git push origin $(NEXT_PATCH_TAG)"
	@echo "Dry run completed."

# ============================
# Code Formatting (Python)
# ============================
format:
	$(PY) -m black core strategies app tests
	$(PY) -m isort core strategies app tests

check-format:
	$(PY) -m black --check core strategies app tests
	$(PY) -m isort --check-only core strategies app tests

lint:
	@echo "Running flake8..."
	$(PY) -m flake8 app core strategies tests

