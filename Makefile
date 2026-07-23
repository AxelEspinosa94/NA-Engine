# ============================
# NA-Engine Release Automation
# ============================

# Get latest tag (e.g., v0.1.1)
CURRENT_TAG := $(shell git describe --tags --abbrev=0)

# Extract numeric version (remove leading "v")
VERSION := $(shell echo $(CURRENT_TAG) | sed 's/v//')

# Split version into components
MAJOR := $(word 1,$(subst ., ,$(VERSION)))
MINOR := $(word 2,$(subst ., ,$(VERSION)))
PATCH := $(word 3,$(subst ., ,$(VERSION)))

# Increment patch version
NEXT_PATCH := $(shell echo $$(($(PATCH)+1)))
NEXT_PATCH_TAG := v$(MAJOR).$(MINOR).$(NEXT_PATCH)

# Increment minor version
NEXT_MINOR := $(shell echo $$(($(MINOR)+1)))
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
