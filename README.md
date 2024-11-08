# Projeto Data Sceience AirBnB - Rio de Janeiro

A Data Science project with AirBnB Rio de Janeiro open data.

### Contexto

No Airbnb, qualquer pessoa que tenha um quarto ou um imóvel de qualquer tipo (apartamento, casa, chalé, pousada, etc.) pode ofertar o seu imóvel para ser alugado por diária.

Você cria o seu perfil de host (pessoa que disponibiliza um imóvel para aluguel por diária) e cria o anúncio do seu imóvel.

Nesse anúncio, o host deve descrever as características do imóvel da forma mais completa possível, de forma a ajudar os locadores/viajantes a escolherem o melhor imóvel para eles (e de forma a tornar o seu anúncio mais atrativo)

Existem dezenas de personalizações possíveis no seu anúncio, desde quantidade mínima de diária, preço, quantidade de quartos, até regras de cancelamento, taxa extra para hóspedes extras, exigência de verificação de identidade do locador, etc.

### Objetivo

Construir um modelo de previsão de preço que permita uma pessoa comum que possui um imóvel possa saber quanto deve cobrar pela diária do seu imóvel.

Ou ainda, para o locador comum, dado o imóvel que ele está buscando, ajudar a saber se aquele imóvel está com preço atrativo (abaixo da média para imóveis com as mesmas características) ou não.

### O que temos disponível, inspirações e créditos

As bases de dados foram retiradas do site kaggle: https://www.kaggle.com/allanbruno/airbnb-rio-de-janeiro

Elas estão disponíveis para download abaixo da aula (se você puxar os dados direto do Kaggle pode ser que encontre resultados diferentes dos meus, afinal as bases de dados podem ter sido atualizadas).

Caso queira uma outra solução, podemos olhar como referência a solução do usuário Allan Bruno do kaggle no Notebook: https://www.kaggle.com/allanbruno/helping-regular-people-price-listings-on-airbnb

Você vai perceber semelhanças entre a solução que vamos desenvolver aqui e a dele, mas também algumas diferenças significativas no processo de construção do projeto.

- As bases de dados são os preços dos imóveis obtidos e suas respectivas características em cada mês.
- Os preços são dados em reais (R$)
- Temos bases de abril de 2018 a maio de 2020, com exceção de junho de 2018 que não possui base de dados

### Expectativas Iniciais

- Acredito que a sazonalidade pode ser um fator importante, visto que meses como dezembro costumam ser bem caros no RJ
- A localização do imóvel deve fazer muita diferença no preço, já que no Rio de Janeiro a localização pode mudar completamente as características do lugar (segurança, beleza natural, pontos turísticos)
- Adicionais/Comodidades podem ter um impacto significativo, visto que temos muitos prédios e casas antigos no Rio de Janeiro.

Vamos descobrir o quanto esses fatores impactam e se temos outros fatores não tão intuitivos que são extremamente importantes.

# Tratamento e limpeza dos dados

### Criação do DataFrame a partir dos arquivos .csv

```python
import pandas as pd
import pathlib


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

# Criação de um arquivo Excel para análise visual das colunas.
base_airbnb.head(1000).to_excel('base_airbnb.xlsx', index=False)
```

Após análise visual das colunas que mais interessam para o nosso estudo de ciência de dados, criamos um novo DF a partir delas.

```python
colunas = ['host_response_time', 'host_response_rate', 'host_is_superhost', 'host_listings_count', 'latitude',
           'longitude', 'property_type', 'room_type', 'accommodates', 'bathrooms', 'bedrooms', 'beds', 'bed_type',
           'amenities', 'price', 'security_deposit', 'cleaning_fee', 'guests_included', 'extra_people',
           'minimum_nights', 'maximum_nights', 'number_of_reviews', 'review_scores_rating', 'review_scores_accuracy',
           'review_scores_cleanliness', 'review_scores_checkin', 'review_scores_communication',
           'review_scores_location', 'review_scores_value', 'instant_bookable', 'is_business_travel_ready',
           'cancellation_policy', 'ano', 'mes']

base_airbnb = base_airbnb.loc[:, colunas]
```

## Limpeza de dados NaN

A partir do comando abaixo em python, podemos analisar quantas linhas com o valor NaN temos em cada coluna referente.

```python
print(base_airbnb.isnull().sum())
```

### Resposta terminal

```
host_response_time             401843
host_response_rate             401846
host_is_superhost                 460
host_listings_count               460
latitude                            0
longitude                           0
property_type                       0
room_type                           0
accommodates                        0
bathrooms                        1724
bedrooms                          850
beds                             2502
bed_type                            0
amenities                           0
price                               0
security_deposit               421280
cleaning_fee                   313506
guests_included                     0
extra_people                        0
minimum_nights                      0
maximum_nights                      0
number_of_reviews                   0
review_scores_rating           448016
review_scores_accuracy         448586
review_scores_cleanliness      448413
review_scores_checkin          448650
review_scores_communication    448415
review_scores_location         448553
review_scores_value            448551
instant_bookable                    0
is_business_travel_ready            0
cancellation_policy                 0
ano                                 0
mes                                 0
dtype: int64
host_response_time             401843
host_response_rate             401846
host_is_superhost                 460
host_listings_count               460
latitude                            0
longitude                           0
property_type                       0
room_type                           0
accommodates                        0
bathrooms                        1724
bedrooms                          850
beds                             2502
bed_type                            0
amenities                           0
price                               0
security_deposit               421280
cleaning_fee                   313506
guests_included                     0
extra_people                        0
minimum_nights                      0
maximum_nights                      0
number_of_reviews                   0
review_scores_rating           448016
review_scores_accuracy         448586
review_scores_cleanliness      448413
review_scores_checkin          448650
review_scores_communication    448415
review_scores_location         448553
review_scores_value            448551
instant_bookable                    0
is_business_travel_ready            0
cancellation_policy                 0
ano                                 0
mes                                 0
dtype: int64
(228209, 34)
```

Dado que as colunas possuem mais de 300.000 linhas em branco, podemos concluir que sua influência em nosso estudo será mínima. Portanto, optaremos por excluir essas colunas completamente.

```python
for coluna in base_airbnb:
    if base_airbnb[coluna].isnull().sum() > 300000:
        base_airbnb.drop(coluna, axis=1)
```

Com o código acima podemos excluir todas as colunas que possuem mais de 300.000 linhas em branco, resultando nas seguintes colunas em nosso DataFrame.

```
host_is_superhost            460
host_listings_count          460
latitude                       0
longitude                      0
property_type                  0
room_type                      0
accommodates                   0
bathrooms                   1724
bedrooms                     850
beds                        2502
bed_type                       0
amenities                      0
price                          0
guests_included                0
extra_people                   0
minimum_nights                 0
maximum_nights                 0
number_of_reviews              0
instant_bookable               0
is_business_travel_ready       0
cancellation_policy            0
ano                            0
mes                            0
```

Percebemos que as colunas que sobraram ainda possuem um número considerável de linhas NaN, mas que podemos excluir para aprimorar ainda mais nosso estudo.

```python
base_airbnb = base_airbnb.dropna()
```

Esse comando _dropa_ todas as linhas com valores NaN, resultando no seguinte retorno.

```
host_is_superhost           0
host_listings_count         0
latitude                    0
longitude                   0
property_type               0
room_type                   0
accommodates                0
bathrooms                   0
bedrooms                    0
beds                        0
bed_type                    0
amenities                   0
price                       0
guests_included             0
extra_people                0
minimum_nights              0
maximum_nights              0
number_of_reviews           0
instant_bookable            0
is_business_travel_ready    0
cancellation_policy         0
ano                         0
mes                         0
dtype: int64
```

## Tratando os tipos de dados

Agora precisamos verificar se os tipos de dados em cada coluna estão corretos em relação aos valores que contêm. Podemos usar o método .dtypes para identificar os tipos de dados de cada coluna e o método .iloc[0] para inspecionar o conteúdo das primeiras linhas.

```python
# Verificar os tipos de dados
print(base_airbnb.dtypes)

# Consultar os dados da primeira linha
print(base_airbnb.iloc[0])
```

### Resultados para as consultas

DTypes

```
host_is_superhost            object
host_listings_count         float64
latitude                    float64
longitude                   float64
property_type                object
room_type                    object
accommodates                  int64
bathrooms                   float64
bedrooms                    float64
beds                        float64
bed_type                     object
amenities                    object
price                        object
guests_included               int64
extra_people                 object
minimum_nights                int64
maximum_nights                int64
number_of_reviews             int64
instant_bookable             object
is_business_travel_ready     object
cancellation_policy          object
ano                           int64
mes                           int64
```

iloc[0]

```
host_is_superhost                                                           f
host_listings_count                                                       1.0
latitude                                                           -22.946854
longitude                                                          -43.182737
property_type                                                       Apartment
room_type                                                     Entire home/apt
accommodates                                                                4
bathrooms                                                                 1.0
bedrooms                                                                  0.0
beds                                                                      2.0
bed_type                                                             Real Bed
amenities                   {TV,Internet,"Air conditioning",Kitchen,Doorma...
price                                                                 $133.00
guests_included                                                             2
extra_people                                                           $34.00
minimum_nights                                                             60
maximum_nights                                                            365
number_of_reviews                                                          38
instant_bookable                                                            f
is_business_travel_ready                                                    f
cancellation_policy                               strict_14_with_grace_period
ano                                                                      2018
mes                                                                         4
```

Através dessas informações, percebemos que as colunas **price** e **extra_people** estão com o tipo **object**, que é o mesmo que uma string, mas por serem valores monetários, precisamos convertê-los para float, limpando os separadores e os cifrões $.

Podemos realizar o tratamento através de 2 formas utilizando o python, a primeira usando o replace e depois o Numpy para converter os dados para float, e a outra através da lambda, onde passamos todas as intruções em uma única linha de código.

> Uma dica é converter para float32, uma vez que usa menos memório.

**NP**

```python
# price
base_airbnb['price'] = base_airbnb['price'].str.replace('$', '')
base_airbnb['price'] = base_airbnb['price'].str.replace(',', '')
base_airbnb['price'] = base_airbnb['price'].astype(np.float32, copy=False)

# extra_people
base_airbnb['extra_people'] = base_airbnb['extra_people'].str.replace('$', '')
base_airbnb['extra_people'] = base_airbnb['extra_people'].str.replace(',', '')
base_airbnb['extra_people'] = base_airbnb['extra_people'].astype(np.float32, copy=False)
```

**Lambda**

```python
# price
base_airbnb['price'] = base_airbnb['price'].apply(lambda x: float(x.replace('$', '').replace(',', '')))

# extra_people
base_airbnb['extra_people'] = base_airbnb['extra_people'].apply(lambda x: float(x.replace('$', '').replace(',', '')))
```

Ao executarmos uma das sequências de código acima, obtemos o seguinte resultado agora:

```
host_is_superhost            object
host_listings_count         float64
latitude                    float64
longitude                   float64
property_type                object
room_type                    object
accommodates                  int64
bathrooms                   float64
bedrooms                    float64
beds                        float64
bed_type                     object
amenities                    object
price                       float64
guests_included               int64
extra_people                float64
minimum_nights                int64
maximum_nights                int64
number_of_reviews             int64
instant_bookable             object
is_business_travel_ready     object
cancellation_policy          object
ano                           int64
mes                           int64
```
