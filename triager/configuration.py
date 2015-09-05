import os

from ConfigParser import SafeConfigParser


class Configuration(object):
    def __init__(self, config_dir):
        self.config_file = os.path.join(config_dir, "settings.cfg")
        self.config = SafeConfigParser()

        if os.path.isfile(self.config_file):
            self.reload()
        else:
            self._setup_config()

    def save(self):
        with open(self.config_file, 'w') as f:
            self.config.write(f)

    def reload(self):
        self.config.read([self.config_file])

    def _setup_config(self):
        self.general__ticket_limit = "3000"
        self.general__min_class_occur = "30"

        self.defaults__schedule = "0 0 * * *"

        self.svm__coefficient = "240.0"
        self.svm__cache_size = "2000"

        self.jira__default_resolutions = "Fixed"
        self.jira__default_status = "Resolved,Closed"

        self.auth__admin = "admin"

        self.save()

    def __getattr__(self, name):
        section_option = name.split("__", 1)
        if len(section_option) == 2 and section_option[0]:
            section, option = section_option

            if self.config.has_section(section) \
                    and self.config.has_option(section, option):
                return self.config.get(section, option)

        raise AttributeError("%s has no attribute '%s'"
                             % (self.__class__.__name__, name))

    def __setattr__(self, name, value):
        section_option = name.split("__", 1)
        if len(section_option) == 2 and section_option[0]:
            section, option = section_option

            if not self.config.has_section(section):
                self.config.add_section(section)

            self.config.set(section, option, str(value))
        elif name in ['config_file', 'config']:
            super(Configuration, self).__setattr__(name, value)
        else:
            raise AttributeError("%s has no attribute '%s'"
                                 % (self.__class__.__name__, name))
