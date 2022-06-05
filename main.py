import main_window, manage_files

def main():
    mf = manage_files.DefaultLocations()
    mf.check_defaults_file()
    main_window.main()

if __name__ == '__main__':
    main()