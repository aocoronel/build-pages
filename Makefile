list:
	@echo "about -- make about page"
	@echo "all -- run everything"
	@echo "css -- make css"
	@echo "feed -- generate RSS feeds"
	@echo "index -- make index"
	@echo "list -- lists all recipes"
	@echo "posts -- make all posts"
	@echo "programs -- make programs page"
	@echo "serve -- run server"
	@echo "sitemap -- generate sitemap"

index:
	bash makeindex

about:
	bash build-pages "_pages/about.md"

programs:
	bash build-pages "_pages/programs.md"

posts:
	bash build-pages

css:
	bash build-pages -c

serve:
	cd _website && python -m http.server

feed:
	python3 ./scripts/rss_gen.py

sitemap:
	python3 ./scripts/sitemap_gen.py

all: posts about index css feed sitemap
