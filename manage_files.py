from datetime import datetime
from itertools import islice
from pathlib import Path
import json
import main_window


class DefaultLocations:
    def __init__(self):
        # default values
        self.file = 'default_locations.txt'
        self.defaults_dict = {
            "outputdir_initial": '.',
            "itunesdir": '.',
            "historyfile": 'history.txt',
            "genres_file": 'genres.txt'
        }

    def read_file(self):
        with open(self.file, 'r') as rf:
            a = rf.read()
            df_contents = json.loads(a)
        return df_contents

    def check_defaults_file(self):
        if not Path(self.file).is_file():
            self.create_file()
            return self.read_file()
        else:
            return self.read_file()

    def create_file(self):
        json_encode = json.dumps(self.defaults_dict)
        with open(self.file, 'w') as fp:
            fp.write(json_encode)

    def load_vars(self):
        with open(self.file, 'r') as rf:
            data = json.load(rf)
        return data


class EditGenre:
    def __init__(self, genre_file):
        self.file = genre_file

    def get_genre(self):
        with open(self.file, "r") as f:
            genres = f.readlines()
            return sorted(genres, key=str.casefold)

    def save_genre(self, lines):
        with open(self.file, "w") as f:
            f.write(lines)


class History:
    def __init__(self, file):
        self.file = file

    def check_file_exists(self):
        pf = Path(self.file)
        return pf.exists()

    def save_history(self, url, object_name):
        curr_dt = datetime.now().strftime("%x %X")
        line = curr_dt + "; " + url + "; " + object_name + "\n"
        if not self.check_file_exists():
            self.write_file(line)
        else:
            with open(self.file, "r+") as f:
                existing_lines = f.readlines()
                f.seek(0)
                f.write(line)
                f.writelines(existing_lines)
                # for l in fileinput.input(files=self.file, inplace=True):
            #     if fileinput.isfirstline():
            #         print(line)
            #     else:
            #         print(l)
            # fileinput.close()

    def write_file(self, lines):
        with open(self.file, "w") as wf:
            wf.writelines(lines)

    def read_history(self, max_num_of_lines=0):
        if not isinstance(max_num_of_lines, int):
            return "max number of lines must be an integer"

        if not self.check_file_exists():
            return "no history exists"

        if max_num_of_lines == 0:
            # return all lines
            with open(self.file, "r") as f:
                all_lines = f.readlines()
                return ''.join(all_lines)
        else:
            with open(self.file, "r") as f:
                some_lines = list(islice(f, max_num_of_lines))
                return ''.join(some_lines)
