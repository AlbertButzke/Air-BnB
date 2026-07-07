import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from pathlib import Path
from streamlit_plotly_events import plotly_events
import plotly.graph_objects as go

st.set_page_config(
    page_title="Dashboard de Anúncios no AirBnB",
    page_icon="📊",
    layout="wide",
)

# st.logo(
#     image="https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Airbnb_Logo_B%C3%A9lo.svg/3840px-Airbnb_Logo_B%C3%A9lo.svg.png",
#     link="https://www.airbnb.com.br",
#     size='large', 
#     # width=180
# )

    

CAMINHO_ATUAL = Path(__file__).parent


# --- Métricas Principais (KPIs) ---

st.markdown(
    """
    <style>
    [data-testid="stVerticalBlock"] {
        gap: 0.5rem !important;
    }
    h1, h2, h3 {
        color: #FA8072 !important;
        margin-top: 10px !important;
        margin-bottom: 10px !important;
        padding-bottom: 0px !important;
    }
    [data-testid="stMetric"] {
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        
        /* Estilo da caixinha */
        border: 2px solid #FFA07A; /* Borda salmão claro */
        border-radius: 10px;       /* Cantos arredondados */
        padding: 6px 15px !important;             Espaço interno para não sufocar o texto */
        background-color: #FFF5EE; /* Fundo suave (Seashell) para destacar a caixinha */
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05); /* Sombra de leve */
    }
    
    [data-testid="stMetricLabel"] {
        display: flex;
        justify-content: center;
        text-align: center;
        width: 100%;
        margin-bottom: -5px !important;
    }
    
    [data-testid="stMetricLabel"] > div {
        color: #FA8072 !important; 
        text-align: center;
    }
    
    [data-testid="stMetricValue"] > div {
        color: #FA8072 !important; 
        font-weight: bold;
    }
    div[data-testid="stSegmentedControl"] {
        width: 100%;
    }
    div[data-testid="stSegmentedControl"] > div {
        width: 100%;
        display: flex;
    }
    div[data-testid="stSegmentedControl"] button {
        flex: 1;
    }
    div[data-testid="stSegmentedControl"] [data-testid="stWidgetLabel"] p {
        color: #FA8072 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

df = pd.read_csv(CAMINHO_ATUAL / 'data' / 'AirBnBLimpo.csv')
col_logo_esq, col_botoes = st.columns([1, 3])

with col_logo_esq:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Airbnb_Logo_B%C3%A9lo.svg/3840px-Airbnb_Logo_B%C3%A9lo.svg.png", 
        width=200
    )

opcoes_quartos = ["Todo o espaço", "Quarto privativo", "Quarto compartilhado"]

with col_botoes:
    selecao = st.segmented_control(
        "Tipo de Acomodação", 
        options=opcoes_quartos, 
        selection_mode="multi",
        label_visibility="collapsed",
        width="stretch"
    )

df_filtrado = df.copy()

if selecao:
    # df_filtrado = df_filtrado[df_filtrado["room_type"] == selecao]
    df_filtrado = df_filtrado[df_filtrado["room_type"].isin(selecao)]


st.subheader("Métricas gerais")
if not df_filtrado.empty:
    total_listing = len(df_filtrado)
    preco_medio = df_filtrado['price_cleaned'].mean()
    media_noites = df_filtrado['minimum_nights'].mean()
    bairro_mais_listado = df_filtrado['neighbourhood_cleansed'].value_counts().idxmax()
    quantidade_bairro_mais_listado = df_filtrado['neighbourhood_cleansed'].value_counts().max()
else:
    total_host, preco_medio, review_medio, _ = 0, 0, 0, "Nenhum dado encontrado"

col1, col2, col3 = st.columns(3)
col1.metric("Total de anúncios", f"{total_listing:}")
col2.metric("Preço médio", f"R${preco_medio:,.2f}")
col3.metric("Média de noites mínimas", f"{media_noites:,.0f}")

col4 = st.columns(1)


col4[0].metric(
    label="Bairro com mais anúncios", 
    value=f"{bairro_mais_listado}: {quantidade_bairro_mais_listado}"
)


st.markdown("---")

col_graf1, col_graf2 = st.columns([2.5,1])

with col_graf1:
    if not df_filtrado.empty:
        df_tratamento = df_filtrado.dropna(subset=['price_cleaned', 'latitude', 'longitude', 'neighbourhood_cleansed']).copy()

        df_bairros = (
            df_tratamento.groupby("neighbourhood_cleansed")
            .agg(
                latitude=("latitude", "mean"),
                longitude=("longitude", "mean"),
                total_anuncios=("neighbourhood_cleansed", "count"),
                preco_medio=("price_cleaned", "mean"),
            )
            .reset_index()
        )

        limits = [(0, 10), (10, 50), (50, 100), (100, 1000), (1000, 20000)]
        colors = ["#D1C7BD", "#FFC0A8", "#FFA07A", "#FA8072", "#D96B52"]

        marker_sizes = [10, 15, 20, 25, 35]

        fig = go.Figure()


        for i in range(len(limits)):
            lim_inf, lim_sup = limits[i]

            df_sub = df_bairros[
                (df_bairros["total_anuncios"] >= lim_inf)
                & (df_bairros["total_anuncios"] < lim_sup)
            ]

            hover_text = [
                f"<b>{row['neighbourhood_cleansed']}</b><br>"
                f"Total de Anúncios: {row['total_anuncios']}<br>"
                f"Preço Médio: R$ {row['preco_medio']:.2f}"
                for _, row in df_sub.iterrows()
            ]

            fig.add_trace(
                go.Scattermapbox(
                    lat=df_sub["latitude"],
                    lon=df_sub["longitude"],
                    mode="markers",
                    marker=dict(
                        size=marker_sizes[i],
                        color=colors[i],
                        opacity=0.8,
                    ),
                    name=f"{lim_inf} - {lim_sup}",
                    text=hover_text,
                    hoverinfo="text",
                )
            )

        fig.update_layout(
            title={'text': "Anúncios do Airbnb por Bairro no Rio de Janeiro (Por Categoria)",
                   'font': {'color': '#FA8072', 'size': 20},
                    'x': 0.5,
                    'xanchor': 'center'},
            autosize=True,
            hovermode="closest",
            showlegend=True,
            legend=dict(title="Intervalo de Anúncios", traceorder="normal"),
            mapbox=dict(
                style="carto-positron",
                zoom=9.5,
                center=dict(lat=-22.9, lon=-43.45),
            ),
            height=500,
            margin={"r": 0, "t": 50, "l": 0, "b": 0},
        )

        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.warning("Nenhum dado para exibir no gráfico.")


with col_graf2:
    if not df_filtrado.empty:
        quantidade_anuncios = df_filtrado['room_type'].value_counts(ascending=False).reset_index()
        grafico_remoto = px.pie(
            quantidade_anuncios,
            names='room_type',
            values='count',
            title="Proporção dos anúncios por tipo de quarto",
            hole=0.5,
            color='room_type', # Garante que o mapeamento de cores seja explícito
            color_discrete_sequence=px.colors.sequential.Peach_r,
            labels={
                'room_type': 'Tipo de Quarto', 
                'count': 'Quantidade'
            }
        )
        grafico_remoto.update_traces(rotation=30,textinfo='percent+label', pull=[0.05, 0, 0, 0], textposition='outside', insidetextorientation='horizontal')
        grafico_remoto.update_layout(title={
                                            'font': {'color': '#FA8072', 'size': 20}},
                                     legend={
                                            'orientation': 'h',  # Deixa a legenda na horizontal
                                            'yanchor': 'top',    # Alinha o topo da legenda com a coordenada Y
                                            'y': -0.1,           # Empurra a legenda para baixo do gráfico (valores negativos saem do gráfico)
                                            'xanchor': 'center', # Alinha o centro da legenda com a coordenada X
                                            'x': 0.5             # Centraliza horizontalmente
                                        }
    )


        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")
    

st.title("Anúncios por Bairro e Tipo de Quarto")
with st.container():
    if not df_filtrado.empty:
        df_agrupado = df_filtrado.groupby(['neighbourhood_cleansed', 'room_type']).size().reset_index(name='Quantidade')
        
        df_pivot = df_agrupado.pivot(
            index='neighbourhood_cleansed', 
            columns='room_type', 
            values='Quantidade'
        ).fillna(0)
        
        for col in ["Todo o espaço", "Quarto privativo", "Quarto compartilhado"]:
            if col not in df_pivot.columns:
                df_pivot[col] = 0
                
        df_pivot['Total'] = df_pivot["Todo o espaço"] + df_pivot["Quarto privativo"] + df_pivot["Quarto compartilhado"]
        
        df_pivot = df_pivot.sort_values(
            by=['Total', "Todo o espaço", "Quarto compartilhado", "Quarto privativo"], 
            ascending=False
        )
        
        ordem_bairros = df_pivot.index.tolist()
        
        df_plot = df_pivot.drop(columns=['Total']).reset_index().melt(
            id_vars='neighbourhood_cleansed', 
            var_name='room_type', 
            value_name='Quantidade'
        )
        
        df_plot['neighbourhood_cleansed'] = pd.Categorical(
            df_plot['neighbourhood_cleansed'], 
            categories=ordem_bairros, 
            ordered=True
        )
        df_plot['room_type'] = pd.Categorical(
                    df_plot['room_type'],
                    categories=["Todo o espaço", "Quarto privativo", "Quarto compartilhado"],
                    ordered=True
                )
        
        df_plot = df_plot.sort_values(['neighbourhood_cleansed', 'room_type'])

        grafico_aluguei_por_bairro = px.bar(
            df_plot,  
            y='Quantidade',
            x='neighbourhood_cleansed',
            # orientation='v',
            color='room_type',
            color_discrete_sequence=px.colors.sequential.Peach_r,
            labels={
                'Quantidade': 'Quantidade de Anúncios',  
                'neighbourhood_cleansed': 'Bairro',        
                'room_type': 'Tipo de Quarto'            
            }
        )

        totais_por_bairro = df_pivot['Total'].to_dict()

        
        for bairro, total in totais_por_bairro.items():
            grafico_aluguei_por_bairro.add_annotation(
                y=total,
                x=bairro,
                text=f" {int(total)}",
                showarrow=False,
                yanchor='bottom',
                font=dict(size=12)
            )

        grafico_aluguei_por_bairro.update_layout(
            xaxis_title=None,
            yaxis_title=None,
            legend=None,
            xaxis=dict(
                range=[-0.5, 19.5],
                showgrid=False
            ),
            yaxis=dict(
                fixedrange=True,
                showgrid=False,
                zeroline=False,
                showticklabels=False
            ),
        )

        grafico_aluguei_por_bairro.update_traces(
            marker_line_width=0,
            marker_line_color="rgba(0,0,0,0)"
        )
        
        
        st.plotly_chart(grafico_aluguei_por_bairro, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico.")

# st.title("Quantidade reviews por anúncios")
# with st.container():
#     if not df_filtrado.empty:

#         grafico_review = px.histogram(
#             df_filtrado,
#             x='number_of_reviews',
#             labels={
#                 'count': 'Quantidade de Anúncios',  
#                 'number_of_reviews': 'Número de Reviews',        
#                 'room_type': 'Tipo de Quarto'            
#             },
#             )
#         grafico_review.update_yaxes(title_text="Quantidade")

        
#         grafico_review.update_traces(
#             hovertemplate="Faixa de Valor: %{x}<br>Quantidade: %{y}"
#         )

#         st.plotly_chart(grafico_review, use_container_width=True)
#     else:
#         st.warning("Nenhum dado para exibir no gráfico.")