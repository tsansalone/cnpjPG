import pandas as pd
import re


def remove_caracter_especial(text):
    return re.sub(r'\W+', '', text)

def formatar_cnpj(row):
    #12345789 0001 23 -> 12.345.789/0001-23
    cnpj_base_formatted = f"{row['CNPJ_base'][:2]}.{row['CNPJ_base'][2:5]}.{row['CNPJ_base'][5:]}"
    cnpj_natural = f"{cnpj_base_formatted}/{row['CNPJ_ordem']}-{row['CNPJ_dv']}"
    return cnpj_natural

df = pd.read_csv('dataset_cnpj_praia_grande_01.csv', delimiter=';', encoding='ISO-8859-1', dtype='str')
df = df.str.strip()
df.fillna('', inplace=True)

cols_endereco = ['tipo_logradouro', 'logradouro', 'numero_logradouro', 'complemento_logradouro', 'bairro', 'CEP', 'UF']

for col in cols_endereco:
    df = df.apply(remove_caracter_especial)

df['endereco_completo'] = df[cols_endereco].apply(lambda row: ', '.join(row.values.astype(str)), axis=1)
df['CNPJ_natural'] = df.apply(formatar_cnpj, axis=1)

df.to_csv('dataset_cnpj_praia_grande_02.csv', index=False, sep=';', encoding='ISO-8859-1')