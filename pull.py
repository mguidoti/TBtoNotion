import os.path
import requests
import json

def get_tb_data(UUID):

    url = ("http://tb.plazi.org/GgServer/dioStats/stats?outputFields=doc.articleUuid+doc.uploadDate+"
        "cont.treatCount+cont.treatCitCount+cont.matCitCount+cont.figCount+cont.tabCount+"
        "cont.bibRefCount+mat.specimenCount+cont.pageCount&groupingFields=doc.articleUuid+doc.uploadDate+"
        "cont.treatCount+cont.treatCitCount+cont.matCitCount+cont.figCount+cont.tabCount+"
        "cont.bibRefCount+cont.pageCount&FP-doc.articleUuid=" + str(UUID) + "&format=JSON")

    r = requests.get(url)

    if r.status_code == 200:

        try:
            return r.json()["data"][0]

        except:
            url = ("http://tb.plazi.org/GgServer/dioStats/stats?outputFields=doc.articleUuid+doc.uploadDate+"
                "cont.figCount+cont.tabCount+cont.bibRefCount+cont.pageCount&groupingFields=doc.articleUuid+doc.uploadDate+"
                "cont.figCount+cont.tabCount+cont.bibRefCount+cont.pageCount&FP-doc.articleUuid=" + str(UUID) + "&format=JSON")

            r = requests.get(url)

            if (r.status_code == 200):

                try:
                    return r.json()["data"][0]
                except:
                    return None
    else:
        return None


def process_tb_data (data, UUID, timestamp):
    #print(data)
    logging_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), ("logs/" + str(timestamp) + ".txt"))

    mode = 'a' if os.path.exists(logging_file) else 'w'

    count = 0

    if data != None:
        if ("ContTreatCount" in data):
            message = str(count) + " - " + UUID + " succesfully done, number of treatments: " + data["ContTreatCount"]
            print(message)
            count += 1
            return data
        elif ("ContTreatCount" not in data and "ContPageCount" in data):
            with open(logging_file, mode) as logger:
                message = ">>> NO TREATMENTS on " + UUID + ".\n"
                print(message[:-2])
                logger.write(message)
            return data
        else:
            with open(logging_file, mode) as logger:
                message = ">>> NO DATA on " + UUID + ", no idea what could have happened.\n"
                print(message[:-2])
                logger.write(message)
            return None
    else:
        with open(logging_file, mode) as logger:
            message = ">>> CONNECTION PROBLEM with " + UUID + "\n"
            print(message[:-2])
            logger.write(message)
        return None

"""
def get_tb_data (UUID, timestamp):

    url = ("http://tb.plazi.org/GgServer/dioStats/stats?outputFields=doc.articleUuid+"
        "cont.treatCount+cont.treatCitCount+cont.matCitCount+cont.figCount+cont.tabCount+"
        "cont.bibRefCount+mat.specimenCount+cont.pageCount&groupingFields=doc.articleUuid+"
        "cont.treatCount+cont.treatCitCount+cont.matCitCount+cont.figCount+cont.tabCount+"
        "cont.bibRefCount+cont.pageCount&FP-doc.articleUuid=" + UUID + "&format=JSON")

    logging_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), ("logs/" + str(timestamp) + ".txt"))

    mode = 'a' if os.path.exists(logging_file) else 'w'

    r = requests.get(url)

    if r.status_code == 200:
        try:
            message = UUID + " succesfully done, number of treatments: " + r.json()["data"][0]["ContTreatCount"]
            print(message)
            return r.json()["data"][0]
        except:
            url = ("http://tb.plazi.org/GgServer/dioStats/stats?outputFields=doc.articleUuid+"
                "cont.figCount+cont.tabCount+cont.bibRefCount+cont.pageCount&groupingFields=doc.articleUuid+"
                "cont.figCount+cont.tabCount+cont.bibRefCount+cont.pageCount&FP-doc.articleUuid=" + UUID + "&format=JSON")
            
            r.requests.get(url)

            if r.status_code == 200:
                with open(logging_file, mode) as logger:
                    message = ">>> NO TREATMENTS on " + UUID + ".\n"
                    print(message[:-2])
                    logger.write(message)
                return r.json()["data"][0]
            else:
                with open(logging_file, mode) as logger:
                    message = ">>> NO DATA on " + UUID + ", no idea what could have happened.\n"
                    print(message[:-2])
                    logger.write(message)
                return None
    else:
        with open(logging_file, mode) as logger:
            message = ">>> CONNECTION PROBLEM with " + UUID + ", " + r.status_code + "\n"
            print(message[:-2])
            logger.write(message)
        return None
"""
"""
#UUID = "FFA3B7374B2567283611FF97FFB25D79"
UUID = "5A7DFFBDFFADB046FFAAD970FF807400"

data = get_tb_data(UUID)

if data != None:
    print(list(data.keys()))
"""