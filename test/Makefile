SQLITE = sqlite3 
CAT = cat
RM = rm -f

kn.sqlite3: kn.sqlite3.dump
	$(RM) $@
	$(CAT) $< | $(SQLITE) $@

