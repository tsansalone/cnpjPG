import pandas as pd
"""
Dados retirados do conjunto de dados "Cadastro Nacional da Pessoa Júridica - CNPJ
https://dados.gov.br/dados/conjuntos-dados/cadastro-nacional-da-pessoa-juridica---cnpj
"""
source_csv_paths = [
    'Dados\Raw\K3241.K03200Y0.D20514.ESTABELE',
    'Dados\Raw\K3241.K03200Y1.D20514.ESTABELE',
    'Dados\Raw\K3241.K03200Y2.D20514.ESTABELE',
    'Dados\Raw\K3241.K03200Y3.D20514.ESTABELE',
    'Dados\Raw\K3241.K03200Y4.D20514.ESTABELE',
    'Dados\Raw\K3241.K03200Y5.D20514.ESTABELE',
    'Dados\Raw\K3241.K03200Y6.D20514.ESTABELE',
    'Dados\Raw\K3241.K03200Y7.D20514.ESTABELE',
    'Dados\Raw\K3241.K03200Y8.D20514.ESTABELE',
    'Dados\Raw\K3241.K03200Y9.D20514.ESTABELE'
]

target_csv_path = 'dataset_cnpj_praia_grande_01.csv'

for source_csv_path in source_csv_paths:
    try:
     
        #Engine python solucionou o problema na leitura de dados com a engine C        
        df = pd.read_csv(source_csv_path, encoding="ISO-8859-1", sep=';', dtype='str', on_bad_lines='skip', engine = 'python')
        
        """
        cod_munic 6921 - Praia Grande
        https://www.fazenda.mg.gov.br/governo/assuntos_municipais/codigomunicipio/codmunicoutest_sp.html
        situação cadastral 02 - Empresa Ativa
        https://www.gov.br/receitafederal/dados/cnpj-metadados.pdf
        """
        filtered_rows = df[df['cod_munic'] == '6921']
        filtered_rows = df[df['situacao_cadastral'] == '02']
        df.drop(['cod_munic', 'situacao_cadastral'], axis=1, inplace=True)
        filtered_rows.to_csv(target_csv_path, sep=';', mode='a', header=False, index=False)

        print(f"Data from {source_csv_path} appended successfully.")
    except Exception as e:
        print(f"Error processing {source_csv_path}: {e}")