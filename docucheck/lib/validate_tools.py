import re
import os


def validate_email(email):
    email_valido = re.search(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email.lower())
    return bool(email_valido)


def validate_cnpj(cnpj):
    cnpj = re.sub(r'\D', '', cnpj)
    if len(cnpj) != 14:
        return False
    soma = 0
    peso = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    for i in range(12):
        soma += int(cnpj[i]) * peso[i]
    resto = soma % 11
    if resto < 2:
        digito_1 = 0
    else:
        digito_1 = 11 - resto
    if int(cnpj[12]) != digito_1:
        return False
    soma = 0
    peso = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    for i in range(13):
        soma += int(cnpj[i]) * peso[i]
    resto = soma % 11
    if resto < 2:
        digito_2 = 0
    else:
        digito_2 = 11 - resto
    return int(cnpj[13]) == digito_2
