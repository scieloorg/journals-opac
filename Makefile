APP_PATH = opac
MANAGE = $(APP_PATH)/manage.py
SETTINGS_TEST = opac.settings_tests
SETTINGS = opac.settings
FIXTURES_DIR = $(APP_PATH)/fixtures

deps:
	@pip install -r requirements.txt
	@pip install -r requirements-tests.txt

clean:
	@find . -name "*.pyc" -delete

test: clean
	@python $(MANAGE) test --settings=$(SETTINGS_TEST)

dbsetup:
	@python $(MANAGE) syncdb --settings=$(SETTINGS)

loaddata:
	@python $(MANAGE) loaddata $(FIXTURES_DIR)/text_home_flatpage.json --settings=$(SETTINGS)

dbmigrate:
	@python $(MANAGE) migrate --settings=$(SETTINGS)

compilemessages:
	@cd $(APP_PATH) && python manage.py compilemessages --settings=$(SETTINGS)

setup: deps dbsetup dbmigrate loaddata compilemessages test refreshsecretkey

upgrade: deps dbmigrate compilemessages test

refreshsecretkey:
	@sed -e 's:^\(SECRET_KEY\).*$$:\1 = '" '`openssl rand -base64 32`' "':g' -i $(APP_PATH)/opac/settings.py
