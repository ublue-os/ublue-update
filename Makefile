UBLUE_ROOT := /tmp/ublue-os
TARGET := ublue-updater
SOURCE_DIR := $(UBLUE_ROOT)/rpms/$(TARGET)
RPMBUILD := $(UBLUE_ROOT)/rpmbuild

all: build-rpm

tarball:
	mkdir -p $(SOURCE_DIR) $(UBLUE_ROOT)/rpms $(SOURCE_DIR)/src $(RPMBUILD)/SOURCES
	cp -r \
		LICENSE Makefile README.md update-ublue \
		$(SOURCE_DIR)/src
	tar czf $(RPMBUILD)/SOURCES/$(TARGET).tar.gz -C $(UBLUE_ROOT)/$(TARGET)/src .	
	cp -r ./files $(SOURCE_DIR)
	tar czf $(RPMBUILD)/SOURCES/$(TARGET)-data.tar.gz -C $(UBLUE_ROOT)/$(TARGET)/files .
	
build-rpm: tarball
	cp ./*.spec $(UBLUE_ROOT)/rpms/
	mkdir -p $(RPMBUILD)
	rpmbuild -ba \
    	--define '_topdir $(RPMBUILD)' \
    	--define '%_tmppath %{_topdir}/tmp' \
    	$(UBLUE_ROOT)/rpms/$(TARGET).spec

clean: $(SOURCE_DIR) $(RPMBUILD)
	rm -rf $^
