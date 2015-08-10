.PHONY: play_icfp2015
play_icfp2015:
	@echo "# There's probably some command I could run here to precompile"
	@echo "# the python source to byte code... but is it really worth it?"
	chmod +x play_icfp2015


perthparkour.tar.gz: *.py Makefile README play_icfp2015
	tar -cf $@ $^