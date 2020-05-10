import process as pr
import pull as pu
import sys
import datetime as dt

#file_path = sys.argv[1]
file_path = 'data/Plazi_Poa_Article_Extractions_2020-05_5.xlsx'

fields = ["ContTreatCount",
    "ContTreatCitCount",
    "ContMatCitCount",
    "ContFigCount",
    "ContTabCount",
    "ContBibRefCount",
    "MatSpecimenCount",
    "ContPageCount",
    "DocUploadDate"
    ]

wb = pr.data(file_path)
sheet = wb.active

timestamp = dt.datetime.now().timestamp()

for field in fields:
    if pr.column_index(file_path, field) == None:
        pr.add_field(file_path, field)

for index, row in enumerate(sheet.rows):
    if (row[pr.column_index(file_path, "Status") - 1].value == "Completed"):
        UUID = row[pr.column_index(file_path, "UUID") - 1].value

        data = pu.process_tb_data(pu.get_tb_data(UUID), UUID, timestamp)

        if data != None:
                for key in list(data.keys()):
                    if key != "DocCount" and key != "DocArticleUuid" and key != 'DocUploadDate':
                        pr.write_value(file_path, key, index + 1, int(data[key]))
                    elif key == 'DocUploadDate':
                        pr.write_value(file_path, key, index + 1, data[key])
        else:
            next

        """
        try:
            for key in list(data.keys()):
                if key != "DocCount" and key != "DocArticleUuid":
                    print(key, index + 1, data[key])
                    pr.write_value(file_path, key, index + 1, int(data[key]))
        except AttributeError:
            print(UUID, "Doesn't has treatments")
            next
        """