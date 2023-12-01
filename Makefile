.PHONY: build
build:
	@gittuf clone ../gittuf-delegation
	@$(cd gittuf-delegation && gittuf verify-ref -f main)
	@make build -C gittuf-delegation
