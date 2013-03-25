APP_PATH = opac
MANAGE = manage.py
SETTINGS_TEST = opac.settings_tests
SETTINGS = opac.settings
FIXTURES_DIR = $(APP_PATH)/fixtures


deps:
	@pip install -r requirements.txt
	@pip install -r requirements-tests.txt

clean:
	@find . -name "*.pyc" -delete

test: clean
	@cd $(APP_PATH) && python $(MANAGE) test --settings=$(SETTINGS_TEST)

dbsetup:
	@cd $(APP_PATH) && python $(MANAGE) syncdb --settings=$(SETTINGS)

loaddata:
	@cd $(APP_PATH) && python $(MANAGE) loaddata text_home_flatpage.json --settings=$(SETTINGS)

dbmigrate:
	@cd $(APP_PATH) && python $(MANAGE) migrate --settings=$(SETTINGS)

compilemessages:
	@cd $(APP_PATH) && python manage.py compilemessages --settings=$(SETTINGS)

setup: deps dbsetup dbmigrate loaddata compilemessages test refreshsecretkey

upgrade: deps dbmigrate compilemessages test

refreshsecretkey:
	@sed -e 's:^\(SECRET_KEY\).*$$:\1 = '" '`openssl rand -base64 32`' "':g' -i $(APP_PATH)/opac/settings.py
