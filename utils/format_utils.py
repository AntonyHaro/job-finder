from datetime import datetime


def format_datetime(data_str):
    """Formata a data do formato da API para exibição em português"""
    try:
        data = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
        return data.strftime("%d/%m/%Y %H:%M")
    except:
        return data_str
