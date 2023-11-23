.PHONY: build
build:
	@gittuf clone ../gittuf-delegation
	@make -C gittuf-delegation
