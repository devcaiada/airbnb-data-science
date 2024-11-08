import matplotlib.pyplot as plt
import pandas as pd
import pathlib
import numpy as np
import seaborn as sns


MESES = {'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4,
         'mai': 5, 'jun': 6, 'jul': 7, 'ago': 8,
         'set': 9, 'out': 10, 'nov': 11, 'dez': 12}
CAMINHO_BASES = pathlib.Path('dataset')

base_airbnb = pd.DataFrame()

for arquivo in CAMINHO_BASES.iterdir():
    if arquivo.suffix == '.csv':
        nome_mes = arquivo.name[:3]
        mes = MESES[nome_mes]
        ano = arquivo.name[-8:]
        ano = int(ano.replace('.csv', ''))

        df = pd.read_csv(arquivo)
        df['ano'] = ano
        df['mes'] = mes
        base_airbnb = pd.concat([base_airbnb, df])

base_airbnb.head(1000).to_excel('base_airbnb.xlsx', index=False)

# Criar DF a partir das colunas que interessam. - Análise manual através do Excel.
colunas = ['host_response_time', 'host_response_rate', 'host_is_superhost', 'host_listings_count', 'latitude',
           'longitude', 'property_type', 'room_type', 'accommodates', 'bathrooms', 'bedrooms', 'beds', 'bed_type',
           'amenities', 'price', 'security_deposit', 'cleaning_fee', 'guests_included', 'extra_people',
           'minimum_nights', 'maximum_nights', 'number_of_reviews', 'review_scores_rating', 'review_scores_accuracy',
           'review_scores_cleanliness', 'review_scores_checkin', 'review_scores_communication',
           'review_scores_location', 'review_scores_value', 'instant_bookable', 'is_business_travel_ready',
           'cancellation_policy', 'ano', 'mes']

base_airbnb = base_airbnb.loc[:, colunas]

print(base_airbnb.isnull().sum())

# Limpar as colunas com mais de 300.000 registros NaN.
for coluna in base_airbnb:
    if base_airbnb[coluna].isnull().sum() > 300000:
        base_airbnb = base_airbnb.drop(coluna, axis=1)

print(base_airbnb.isnull().sum())

base_airbnb = base_airbnb.dropna()

# Tratamento de variáveis categóricas.
print(base_airbnb.dtypes)
print(60*'-')
print(base_airbnb.iloc[0])

# price
base_airbnb['price'] = base_airbnb['price'].apply(lambda x: float(x.replace('$', '').replace(',', '')))

# extra_people
base_airbnb['extra_people'] = base_airbnb['extra_people'].apply(lambda x: float(x.replace('$', '').replace(',', '')))

print(base_airbnb.dtypes)

plt.figure(figsize=(15, 5))
sns.heatmap(base_airbnb.corr(numeric_only=True), annot=True, cmap='Blues')
plt.show()
