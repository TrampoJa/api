from re import sub


class Formater:

    def __new__(self, data):
        formaterData = []
        for field in data:
            formaterData.append(Formater.formater(field))
        return formaterData

    def formater(data):
        regex = r'\s+'
        data = sub(regex, ' ', data)
        data = data.strip().capitalize()
        return data
