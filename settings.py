class Settings:
    def __init__(self, file_name):
        self._file_name = file_name

    def read_file(self):
        config_settings = []
        try:
            f_settings = open(self._file_name)
            lines = f_settings.readlines()
            for line in lines:
                line = line.strip('\n')
                line = line.split('=')
                for part in line:
                    part = part.strip()
                if line[1][0] == '"':
                    line[1] = line[1][1:-1]
                config_settings.append(line)
            f_settings.close()
        except IOError:
            print('Error reading settings file')
        return config_settings[:]

    def get_config_settings(self):
        config_settings = self.read_file()
        try:
            repo_type = config_settings[0][1]
            repo_stud_path = config_settings[1][1]
            repo_assign_path = config_settings[2][1]
            repo_grades_path = config_settings[3][1]
            ui_type = config_settings[4][1]
            return repo_type, repo_stud_path, repo_assign_path, repo_grades_path, ui_type
        except IndexError:
            print('Invalid input in settings file')

