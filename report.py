import sys
import os.path
import datetime as dt
import process as pr

file_path = sys.argv[1]
sheet = pr.data(file_path).active

def write_message(message, person):

    logging_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), ("reports/Notion-" + str(dt.datetime.today().strftime('%Y-%m-%d')) + "_" + person[:person.find(" ")] + ".txt"))
    mode = 'a' if os.path.exists(logging_file) else 'w'
    with open(logging_file, mode) as report:
        report.write(message)


def check_names(sheet):

    for index, row in enumerate(sheet.rows):

        value = row[pr.column_index(file_path, "Name") - 1].value

        person = None
        message = ""

        if (value != "Name"):

            person = row[pr.column_index(file_path, "Assign to...") - 1].value

            if (person is None):
                person = "General "

            if (value is None):
                if (person is not None):
                    message = "Please, add a name to the entry on row number " + str(index + 1) + ";\n"
                    #print(message[:-2])
                    #write_message(message, person)
                else:
                    message = "There is an entry without name or person assign to on row number " + str(index + 1) + ";\n"
                    #print(message[:-2])
                    #write_message(message, "General")
            elif (value.find('<') > -1 or value.find('>') > -1):
                message = "Please remove '<' and '>' from the following Notion entry name: " + value + ";\n"
                #print(message[:-2])
                #write_message(message, person)
            elif (value.find('TMP') == -1 and row[pr.column_index(file_path, "Template Name") -1].value is not None):
                message = "Please, add 'TMP.' to the beginning of the following Notion entry name: " + value + ";\n"
                #print(message[:-2])
                #write_message(message, person)
            elif (value.find('TMP') > -1 and row[pr.column_index(file_path, "Template Name") -1].value is None):
                message = "Please, add the template on the template field for the extraction " + value + ";\n"
                #print(message[:-2])



            if (message != ""):
                print(person, message[:-2])
                write_message(message, person)


def check_empty_cells(sheet, field_name):

    for index, row in enumerate(sheet.rows):

        entry_name = row[pr.column_index(file_path, "Name") - 1].value
        person = row[pr.column_index(file_path, "Assign to...") - 1].value
        value = row[pr.column_index(file_path, field_name) - 1].value
        status = row[pr.column_index(file_path, 'Status') - 1].value

        message = ""

        completed = {
            'Assign to...': False,
            'Project': False,
            'Template': False,
            'DOI': True,
            'Dedicated hours': True,
            'Number of Pages': True,
            'TB Reference Link': True,
            'Zenodo': True,
            'UUID': True,
            'Annotation Detail': True,
        }

        if (entry_name is None):
            entry_name = str(index + 1)

        if (person is None):
            person = "General "

        if (entry_name != "Name"):

            if (field_name == 'Date'):

                if (status == 'Completed' and value is None):
                    message = "The starting and end dates for entry " + entry_name + " are missing;\n"
                elif (value is None or status != 'Completed'): #maybe the logic of the or needs change because it gets false positives with entries that has a value but its not completed
                    message = "The starting date for entry " + entry_name + " is missing;\n"
                elif (status == 'Completed' and value.find('→') == -1):
                    message = "The end date for entry " + entry_name + " is missing;\n"

            elif (field_name == 'GBIF'):
                if (row[pr.column_index(file_path, "Treatment(s)?") -1].value == "Yes" and value is None and status == 'Completed'):
                    message = "The entry " + entry_name + " is missing value on column " + field_name + ";\n"

            elif (completed[field_name] == True and field_name != 'Date'):
                if (status == 'Completed' and value is None):
                    message = "The entry " + entry_name + " is missing value on column " + field_name + ";\n"
            else:
                if (value is None):
                    message = "The entry " + entry_name + " is missing value on column " + field_name + ";\n"

            if (message != ""):
                print(person, message[:-2])
                write_message(message, person)

"""
checking_fields = [
            'Assign to...',
            'Project',
            'DOI',
            'Dedicated hours',
            'Number of Pages',
            'TB Reference Link',
            'Zenodo',
            'UUID',
            'Date',
            'GBIF'
        ]
"""

checking_fields = ['Annotation Detail']


check_names(sheet)

for field in checking_fields:
    check_empty_cells(sheet, field)