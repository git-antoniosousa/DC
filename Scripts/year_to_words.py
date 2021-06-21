import calendar, time
import locale
from num2words import num2words
from datetime import datetime

locale.setlocale(locale.LC_ALL, 'pt_PT')

data_string = "2021-06-20 18:20:00"
date_object = datetime.strptime(data_string, "%Y-%m-%d %H:%M:%S")

ano = num2words(date_object.year, to='year', lang='pt_BR')
mes = calendar.month_name[date_object.month]
dia = num2words(date_object.day, to='year', lang='pt_BR')

hora = num2words(date_object.hour, to='year', lang='pt_BR')
minutos = num2words(date_object.minute, to='year', lang='pt_BR')

data_words = dia + ' dias do mês de ' + mes.lower() + ' do ano de ' + ano

hora_words = ''
if (date_object.minute > 0):
    hora_words = hora + ' horas e ' + minutos + ' minutos'
else:
    hora_words = hora + ' horas'

print(data_words + ', às ' + hora_words)

# Exemplo: 12.Jun.2021
data_str = str(date_object.day) + '.' + mes[:3] + '.' + str(date_object.year)

hora = '14:00'
# Exemplo: 14h00
hora_str = hora.replace(':', 'h')

print(data_str + ' ' + hora_str)

data_homologacao = "2021-06-20"
data_homologacao_object = datetime.strptime(data_homologacao, "%Y-%m-%d")
ano_homologacao = num2words(data_homologacao_object.year, to='year', lang='pt_BR')
mes_homologacao = calendar.month_name[data_homologacao_object.month]
dia_homologacao = num2words(data_homologacao_object.day, to='year', lang='pt_BR')

data_homologacao_words = dia + ' de ' + mes.lower() + ' de ' + ano
print(data_homologacao_words)



