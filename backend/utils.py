from datetime import datetime


class Response:
    response : object = {
        "status": "",
        "items" : [],
        "total" : {
            "summary" : 0,
            "summary_files" : 0,
            "summary_directories": 0
        }
    }

class Date:
    @staticmethod
    def convert_date(timestamp):
        d = datetime.fromtimestamp(timestamp)
        formatted_date = d.strftime("%d/%m/%Y, %H:%M:%S")
        return formatted_date