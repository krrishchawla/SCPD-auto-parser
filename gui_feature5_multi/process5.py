import csv
import os
import datetime
import time
import pandas as pd
import sys
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed

def get_classes(file):
    """Retrieve unique class names from a CSV file."""
    try:
        with open(file, 'r') as f:
            reader = csv.DictReader(f)
            unique_entries = {row['Course Offering Subject-Num Desc'] for row in reader}
        return list(unique_entries)
    except Exception as e:
        print(f"Error reading classes: {e}")
        raise

def get_current_datetime(fmt='%m-%d %I:%M:%S %p'):
    """Get the current date and time formatted according to the provided format."""
    return datetime.datetime.now().strftime(fmt)

def make_dir():
    """Create a directory for storing class files."""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dir_name = 'Classes_' + get_current_datetime()
        directory_path = os.path.join(current_dir, dir_name)
        os.makedirs(directory_path, exist_ok=True)
        print('Classes Folder Successfully Created on', get_current_datetime())
        return directory_path
    except Exception as e:
        print(f"Error creating directory: {e}")
        raise

def make_one_file(file_path):
    """Create a single empty file at the specified path."""
    try:
        open(file_path, 'a').close()
    except OSError as e:
        print(f"Error creating the file: {e}")
        raise

def create_file(file, directory_path, date):
    """Helper function to create a single file."""
    file_path = os.path.join(directory_path, file.replace(' ', '') + f' SCPD Roster {date}.csv')
    make_one_file(file_path)
    return file_path

def make_tree(input_file):
    """Create a directory and a set of files based on the classes listed in the input CSV."""
    try:
        directory_path = make_dir()
        date = get_current_datetime('%m-%d')
        list_of_files = get_classes(input_file)
        
        # Use ProcessPoolExecutor to create files concurrently
        with ProcessPoolExecutor() as executor:
            futures = {executor.submit(create_file, file, directory_path, date): file for file in list_of_files}
            for future in tqdm(as_completed(futures), total=len(futures), desc="Creating CSV files", unit="file"):
                try:
                    future.result()  # Check for exceptions
                except Exception as e:
                    print(f"Error creating file {futures[future]}: {e}")
        
        return directory_path, list_of_files
    except Exception as e:
        print(f"Error creating tree: {e}")
        raise

def fill_one_file(course_name, input_file, directory_path, tuition_filter_list):
    """Fill a single class file with filtered student data from the input CSV."""
    date = get_current_datetime('%m-%d')
    output_file = os.path.join(directory_path, f'{course_name.replace(" ", "")} SCPD Roster {date}.csv')
    desired_columns = [
        'Course Offering Subject-Num Desc', 'EMPLID', 'Preferred Email Address',
        'Last Name', 'First Name', 'SUNet ID', 'Tuition Group Desc',
        'Stu Current Acad Plan Code', 'Study Agreement Code'
    ]
    main_heading_row = {
        'Course Offering Subject-Num Desc': f'Course: {course_name}',
        'EMPLID': '', 'Preferred Email Address': '',
        'Last Name': '', 'First Name': '',
        'SUNet ID': '', 'Tuition Group Desc': '',
        'Stu Current Acad Plan Code': '', 'Study Agreement Code': ''
    }

    bosp_filter = 'BOSP' in tuition_filter_list

    if bosp_filter:
        tuition_filter_list.remove('BOSP')

    filter_on = bool(tuition_filter_list)

    try:
        with open(input_file, 'r') as csv_input, open(output_file, 'w', newline='') as csv_output:
            reader = csv.DictReader(csv_input)
            writer = csv.DictWriter(csv_output, fieldnames=desired_columns)
            seen = set()
            writer.writerow(main_heading_row)
            writer.writeheader()
            for row in reader:
                if row['Course Offering Subject-Num Desc'] == course_name:

                    if (filter_on and row["Tuition Group Desc"] in tuition_filter_list) or (bosp_filter and row['Study Agreement Code'][0] in ['O', 'X']):

                        last_name, first_name = row['Last First Name'].split(',', 1)
                        bosp = ''
                        if row['Study Agreement Code'][0] in ['O', 'X']:
                            bosp = 'BOSP'
                        output_row = {
                            'Course Offering Subject-Num Desc': row['Course Offering Subject-Num Desc'],
                            'EMPLID': row['EMPLID'],
                            'Preferred Email Address': row['Preferred Email Address'],
                            'Last Name': last_name,
                            'First Name': first_name.strip(),
                            'SUNet ID': row['SUNet ID'],
                            'Tuition Group Desc': row['Tuition Group Desc'],
                            'Stu Current Acad Plan Code': row['Stu Current Acad Plan Code'],
                            'Study Agreement Code': bosp
                        }
                        compare_row = (
                            row['Course Offering Subject-Num Desc'],
                            row['EMPLID'],
                            row['Preferred Email Address'],
                            last_name,
                            first_name.strip(),
                            row['SUNet ID']
                        )
                        if compare_row not in seen:
                            writer.writerow(output_row)
                            seen.add(compare_row)
                    elif not filter_on and not bosp_filter:
                        last_name, first_name = row['Last First Name'].split(',', 1)
                        bosp = ''
                        if row['Study Agreement Code'][0] in ['O', 'X']:
                            bosp = 'BOSP'
                        output_row = {
                            'Course Offering Subject-Num Desc': row['Course Offering Subject-Num Desc'],
                            'EMPLID': row['EMPLID'],
                            'Preferred Email Address': row['Preferred Email Address'],
                            'Last Name': last_name,
                            'First Name': first_name.strip(),
                            'SUNet ID': row['SUNet ID'],
                            'Tuition Group Desc': row['Tuition Group Desc'],
                            'Stu Current Acad Plan Code': row['Stu Current Acad Plan Code'],
                            'Study Agreement Code': bosp
                        }
                        compare_row = (
                            row['Course Offering Subject-Num Desc'],
                            row['EMPLID'],
                            row['Preferred Email Address'],
                            last_name,
                            first_name.strip(),
                            row['SUNet ID']
                        )
                        if compare_row not in seen:
                            writer.writerow(output_row)
                            seen.add(compare_row)

    except Exception as e:
        print(f"Error filling file {course_name}: {e}")
        raise

def compute(name_of_file, tuition_filter_list):
    """Main computation function to create and fill class files based on input and filters."""
    if not name_of_file:
        sys.exit("ERROR: Filename not provided.")
    
    csv_file = f"{name_of_file}.csv"
    if not os.path.isfile(csv_file):
        sys.exit(f"ERROR: File {csv_file} not found in directory.")

    try:
        print(f'Operating on file {csv_file}')
        print(f'Filtering by: {tuition_filter_list}')
        directory_path, list_of_files = make_tree(csv_file)

        # Use ProcessPoolExecutor to fill files concurrently
        with ProcessPoolExecutor() as executor:
            futures = {executor.submit(fill_one_file, file, csv_file, directory_path, tuition_filter_list): file for file in list_of_files}
            for future in tqdm(as_completed(futures), total=len(futures), desc="Filling CSV files", unit="file"):
                try:
                    future.result()  # Check for exceptions
                except Exception as e:
                    print(f"Error processing file {futures[future]}: {e}")

        print("\nComplete!")
    except Exception as e:
        print(f"Error during computation: {e}")
        raise

def main():
    """Entry point for the script."""
    if len(sys.argv) < 2:
        print("No Arguments")
        return
    name_of_file = sys.argv[1]
    filters = sys.argv[2:]
    compute(name_of_file, filters)

if __name__ == '__main__':
    main()
