import csv
import os
import datetime
import time
import pandas as pd


def xlsx_to_csv(input_file, output_file):
    """
    Converts an XLSX file to CSV format using pandas.
    Args:
        input_file (str): The path to the input XLSX file.
        output_file (str): The path to save the output CSV file.
    Returns:
        None
    """
    # Read the XLSX file into a pandas DataFrame
    df = pd.read_excel(input_file)
    # Save the DataFrame as a CSV file
    df.to_csv(output_file, index=False)
    # Print a success message
    print("Conversion from XLSX to CSV completed successfully.")


def getClasses(file):
    """
    Retrieves unique entries from a CSV file column.
    Args:
        file (str): The path to the CSV file.
    Returns:
        list: A list of unique entries from the specified column.
    """
    # Open the CSV file
    with open(file, 'r') as file:
        # Create a CSV reader object
        reader = csv.DictReader(file)
        # Create a set to store unique entries
        unique_entries = set()
        # Iterate over each row in the CSV file
        for row in reader:
            # Get the value from the specified column
            subject_num_desc = row['Course Offering Subject-Num Desc']
            # Add the value to the set
            unique_entries.add(subject_num_desc)
        # Convert the set to a list
        unique_entries_list = list(unique_entries)
    # Return the list of unique entries
    return unique_entries_list


def dateTime():
    """
    Retrieves the current date and time and returns it in a formatted string.
    Returns:
        str: The current date and time in the format 'MM-DD hh:mm:ss AM/PM'.
    """
    # Get the current date and time
    current_date_time = datetime.datetime.now()
    # Format the date and time into the desired string format
    formatted_date_time = current_date_time.strftime('%m-%d %I:%M:%S %p')
    # Return the formatted date and time
    return formatted_date_time


def dateTime2():
    """
    Retrieves the current date and time and returns it in a formatted string.
    Returns:
        str: The current date and time in the format 'MM-DD hh:mm:ss AM/PM'.
    """
    # Get the current date and time
    current_date_time = datetime.datetime.now()
    # Format the date and time into the desired string format
    formatted_date_time = current_date_time.strftime('%m-%d')
    # Return the formatted date and time
    return formatted_date_time


def makeDir():
    """
    Creates a directory with a timestamped name and returns its path.
    Returns:
        str: The path of the created directory.
    """
    # Get the current directory path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the current date and time
    date = dateTime()
    # Create the directory name with the timestamp
    dir_name = 'Classes' + '_' + date
    # Create the full path of the directory
    directory_path = os.path.join(current_dir, dir_name)
    # Create the directory if it doesn't exist
    os.makedirs(directory_path, exist_ok=True)
    # Print a success message
    print('Classes Folder Successfully Created on', date)
    # Return the path of the created directory
    return directory_path


def makeOneFile(file_path):
    """
    Creates a new file at the specified file path.
    Args:
        file_path (str): The path of the file to be created.
    Returns:
        None
    """
    try:
        # Create the file
        open(file_path, 'a').close()
        # Extract the file name from the file path
        file_ = file_path.split(os.sep)
        file = file_[-1]
        # Print a success message
        print(file + " created successfully.")
    except OSError as e:
        # Print an error message if file creation fails
        print(f"Error creating the file: {e}")



def makeTree(input_file):
    """
    Creates a directory and multiple files based on unique entries from an input file.
    Args:
        input_file (str): The path of the input file.
    Returns:
        tuple: A tuple containing the directory path and the list of file names created.
    """
    # Create the directory
    directory_path = makeDir()
    date = dateTime2()
    print()
    # Get the list of unique entries from the input file
    list_of_files = getClasses(input_file)
    # Iterate over each unique entry and create a file
    for file in list_of_files:
        # Construct the file path
        file_path = os.path.join(directory_path, file.replace(' ', '') + f' SCPD Roster {date}.csv')
        # Pause for a short duration (0.1 seconds)
        time.sleep(0.05)
        # Create the file
        makeOneFile(file_path)
    print()
    # Return the directory path and the list of file names
    return directory_path, list_of_files


def fillOneFile(course_name, input_file, directory_path, tuition_filter_list):
    """
    Filters rows based on the course name and writes them to a new CSV file within the specified directory.
    Args:
        course_name (str): The name of the course to filter the rows.
        input_file (str): The path of the input CSV file.
        directory_path (str): The path of the directory to save the output CSV file.
    Returns:
        None
    """
    # Construct the output file path
    date = dateTime2()
    output_file = os.path.join(directory_path, f'{course_name.replace(" ", "")} SCPD Roster {date}.csv')
    # Specify the desired columns
    desired_columns = [
                    'Course Offering Subject-Num Desc',
                    'EMPLID', 'Preferred Email Address', 
                    'Last Name', 
                    'First Name', 
                    'SUNet ID', 
                    'Tuition Group Desc', 
                    'Stu Current Acad Plan Code']
    # Create the main heading row
    main_heading_row = {
        'Course Offering Subject-Num Desc': f'Course: {course_name}',
        'EMPLID': '',
        'Preferred Email Address': '',
        'Last Name': '',
        'First Name': '',
        'SUNet ID': '',
        'Tuition Group Desc': '',
        'Stu Current Acad Plan Code': ''
    }
    # Open the input and output files
    with open(input_file, 'r') as csv_input, open(output_file, 'w', newline='') as csv_output:
        reader = csv.DictReader(csv_input)
        writer = csv.DictWriter(csv_output, fieldnames=desired_columns)
        seen = []  # Keep track of rows already written to avoid duplicates
        writer.writerow(main_heading_row)  # Write the main heading row
        writer.writeheader()  # Write the column headers
        for row in reader:
            if row['Course Offering Subject-Num Desc'] == course_name:
                # Tuition Group Filter
                if row["Tuition Group Desc"] in tuition_filter_list:
                # Split Last First Name into Last Name and First Name using ',' as the delimiter
                    last_name, first_name = row['Last First Name'].split(',', 1)
                    # Create a new dictionary with desired columns
                    output_row = {
                        'Course Offering Subject-Num Desc': row['Course Offering Subject-Num Desc'],
                        'EMPLID': row['EMPLID'],
                        'Preferred Email Address': row['Preferred Email Address'],
                        'Last Name': last_name,
                        'First Name': first_name.strip(),  # Remove leading/trailing spaces from first name
                        'SUNet ID': row['SUNet ID'],
                        'Tuition Group Desc': row['Tuition Group Desc'],
                        'Stu Current Acad Plan Code': row['Stu Current Acad Plan Code']
                    }
                    if output_row not in seen:
                        # Write the row to the output file
                        writer.writerow(output_row)
                        seen.append(output_row)
    # print(f"Data for course {course_name.replace(' ', '')} has been extracted and saved to {output_file}")


def main():
    """
    Entry point of the program.
    Returns:
        None
    """

    ###############

    # Filter in by Tuition Group Desc

    print('Filter with the following Tuition Groups: ')
    options = {"1" : "Engineering Graduate", "2": "Undergraduate Full Time", "3": "Honor's Coop - Engineering", "4": "SCPD NDO"}
    print(options)

    tuition_filter = input('Type in the number you want to filter by, separated by commas. If want to include all, just hit enter: ')
    tuition_filter_list = []

    if tuition_filter != '':
        tuition_filter_options = tuition_filter.replace(' ', '').split(',')
        
        for elem in tuition_filter_options:
            tuition_filter_list.append(options[elem])
    else:
        for elem in options:
            tuition_filter_list.append(options[elem])

    print('Filtering by: ', tuition_filter_list)

    #################

    # Prompt the user for a file name
    INPUT = input('Type in the file name: ')
    # Construct the file path
    csv = INPUT + '.csv'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv = os.path.join(current_dir, csv)
    # Create the directory tree and retrieve the list of files
    directory_path, list_of_files = makeTree(csv)
    # Iterate over each file and extract/fill its contents
    for task, file in enumerate(list_of_files):
        progress = (task + 1) / len(list_of_files)
        percentage = int(progress * 100)
        tab = '\t'
        # time.sleep(0.5)
        # Print the progress and percentage completion
        print('----------------------------------------------------------', end='\r')
        print(f"Extracting contents for {file}, {tab} {percentage}% complete", end='\r')
        # Fill the contents of the file
        fillOneFile(file, csv, directory_path, tuition_filter_list)
    print()
    print()
    print('Complete!')




if __name__ == '__main__':
    main()
