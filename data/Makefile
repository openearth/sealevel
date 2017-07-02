# two targets
TOPTARGETS := all clean

# look for subdirectories
SUBDIRS := $(wildcard */.)
# depend target on each directory
$(TOPTARGETS): $(SUBDIRS)
# make in each directory
$(SUBDIRS):
	$(MAKE) -C $@ $(MAKECMDGOALS)
# dependencies
.PHONY: $(TOPTARGETS) $(SUBDIRS)
