 .ONESHELL:

python := python3

package_dir := template_shop

code_dir := $(package_dir)


define setup_env
    $(eval ENV_FILE := $(1))
    @echo " - setup env $(ENV_FILE)"
    $(eval include $(1))
    $(eval export)
endef

.PHONY: reformat
reformat:
	black $(package_dir)
	isort $(package_dir) --profile black --filter-files
	ruff check --select I,COM812 --fix

.PHONY: dev-bot
dev-bot:
	$(call setup_env, .env.dev)
	python3 -m template_shop.bot

.PHONY: dev-admin
dev-admin:
	$(call setup_env, .env)
	gunicorn template_shop.admin_panel.wsgi:app --workers=4 --threads=4 --preload -b 0.0.0.0:5000

.PHONY: dev-worker
dev-worker:
	$(call setup_env, .env.dev)
	python3 -m template_shop.worker
