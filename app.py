# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 14:20:11 2021

@author: Acer
"""

#%%
import streamlit as st
import pandas as pd
import plotly_express as px

st.set_page_config(page_title='Sales of Video Games',
                   page_icon=":sunny:",
                   layout='wide')

st.subheader("Importing the dataset")

st.set_option('deprecation.showfileUploaderEncoding', False)

uploaded_file = st.file_uploader(label="Upload your csv or excel file. (200 MB max)",
                         type=['csv','xlsx'])

global df
if uploaded_file is not None:
    print(uploaded_file)
    print("hello! file is uploaded")
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        print(e)
        df = pd.read_excel(uploaded_file)
        
try:
    st.write("uploaded file will show above")
except Exception as e:
    print(e)
    st.subheader("Error shows because dataset is not uploaded yet or need to upload to correct file type.")

#df = pd.read_csv(uploaded_file)
#st.write(df)
#st.dataframe(df=df)


check = st.sidebar.checkbox('reveal data')
print(check)
if check:
    st.write(df)

# @st.cache 
# def get_data():
#     df = pd.read_csv(r"D:\projects dataset\vgsales.csv")
    
# # df['hour'] = pd.to_datetime(df['TimeStamp'], format="%H:%M:%S").dt.hour
#     return df

# df = get_data()
#st.write(df)

st.sidebar.header("Please Filter the data here:")
genre = st.sidebar.multiselect(
    "Select the Genre:",
    options=df['Genre'].unique(),
    default=["Sports",'Racing']
)


year = st.sidebar.multiselect(
    "Select the Year:",
    options=df['Year'].unique(),
    default=2006,
)


publisher = st.sidebar.multiselect(
    "Select the Publisher:",
    options=df['Publisher'].unique(),
    default=["Nintendo","Ubisoft"]
)


game_platform = st.sidebar.multiselect(
    "Select the platform:",
    options=df['Platform'].unique(),
    default = ['Wii','NES']
)


df_selection = df.query(
    "Genre == @genre & Year == @year & Publisher == @publisher & Platform == @game_platform"
)


st.title("Graph Representation of: Video Game's Sales")
st.markdown("##")
    
total_sales = int(df_selection['Global_Sales'].sum())
average_NA_sales = round(df_selection['NA_Sales'].mean(),1)
total_NA_sales = int(df_selection['NA_Sales'].sum())
average_EU_sales = round(df_selection['EU_Sales'].mean(),1)
total_EU_sales = int(df_selection["EU_Sales"].sum())
total_average_sale = round(df_selection['Global_Sales'].mean(),1)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales World Wide:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Total Sales in North America: ")
    st.subheader(f"US $ {total_NA_sales:,}")
with middle_column:
    st.subheader("Average Sales in North America: ")
    st.subheader(f"US $ {average_NA_sales:,}")
with right_column:
    st.subheader("Total Sales in European Union: ")
    st.subheader(f"US $ {total_EU_sales:,}")
with right_column:
    st.subheader("Average Sales in European Union: ")
    st.subheader(f"US $ {average_EU_sales:,}")
with left_column:
    st.subheader("Total World Wide Average Sale: ")
    st.subheader(f"US $ {total_average_sale:,}")
    
st.markdown("""---------------""")
    
check1 = st.checkbox("To look at the Bar Chart chick the button:")
print(check1)
if check1:
    # SALES BY PRODUCT GENRE [BAR CHART]
    sales_by_product_genre = (
    df_selection.groupby(by=['Genre']).sum()[['Global_Sales']].sort_values(by='Global_Sales')
    )
    
    fig_game_sale = px.bar(
        sales_by_product_genre,
        x='Global_Sales',
        y=sales_by_product_genre.index,
        orientation="h",
        title="<b>Sales by Video Game Genre</b>",
        #color_discrete_sequence=["#0083B8"] * len(sales_by_product_genre),
        color = 'Global_Sales',
        template="plotly_white",
        )
    
    fig_game_sale.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=(dict(showgrid=False))
        )
        
        
    sales_by_publisher = (
        df_selection.groupby(by=['Publisher']).sum()[['Global_Sales']].sort_values(by='Global_Sales')
        )
        
    fig_publisher_sale = px.bar(
        sales_by_publisher,
        x='Global_Sales',
        y=sales_by_publisher.index,
        orientation="h",
        title="<b>Sales by Video Game According to Publisher </b>",
        #color_discrete_sequence=["#0083B8"] * len(sales_by_publisher),
        color = 'Global_Sales',
        template="plotly_white",
        )
        
    fig_publisher_sale.update_layout(
        #xaxis=dict(tickmode="linear"),
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=(dict(showgrid=False))
        )
        
        
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_game_sale, use_container_width=True)
    right_column.plotly_chart(fig_publisher_sale, use_container_width=True)
   
st.markdown("----------------------------")
    
check2 = st.checkbox("To look at the Line Plot chick the button:")
print(check2)
if check2:
    
    sales_by_product_genre = (
        df_selection.groupby(by=['Genre']).sum()[['Global_Sales']].sort_values(by='Global_Sales')
        )
        
    fig_game_sale = px.line(
        sales_by_product_genre,
        x='Global_Sales',
        y=sales_by_product_genre.index,
        orientation="h",
        title="<b>Sales by Video Game Genre</b>",
        color_discrete_sequence=["#0083B8"] * len(sales_by_product_genre),
        template="plotly_white",
        )
        
    fig_game_sale.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=(dict(showgrid=False))
        )
        
        
    sales_by_publisher = (
        df_selection.groupby(by=['Publisher']).sum()[['Global_Sales']].sort_values(by='Global_Sales')
        )
        
    fig_publisher_sale = px.line(
        sales_by_publisher,
        x='Global_Sales',
        y=sales_by_publisher.index,
        orientation="h",
        title="<b>Sales by Video Game According to Publisher </b>",
        color_discrete_sequence=["#0083B8"] * len(sales_by_publisher),
        template="plotly_white",
        )
        
    fig_publisher_sale.update_layout(
        #xaxis=dict(tickmode="linear"),
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=(dict(showgrid=False))
        )
        
        
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_game_sale, use_container_width=True)
    right_column.plotly_chart(fig_publisher_sale, use_container_width=True)
    
st.markdown("-------")

check3 = st.checkbox("To look at the Area Chart chick the button:")
print(check3)
if check3:
    
    sales_by_product_genre = (
        df_selection.groupby(by=['Genre']).sum()[['Global_Sales']].sort_values(by='Global_Sales')
        )
        
    fig_game_sale = px.area(
        sales_by_product_genre,
        x='Global_Sales',
        y=sales_by_product_genre.index,
        orientation="h",
        title="<b>Sales by Video Game Genre</b>",
            
        color_discrete_sequence=["#0083B8"] * len(sales_by_product_genre),
        template="plotly_white",
        )
        
    fig_game_sale.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=(dict(showgrid=False))
        )
        
        
    sales_by_publisher = (
        df_selection.groupby(by=['Publisher']).sum()[['Global_Sales']].sort_values(by='Global_Sales')
        )
        
    fig_publisher_sale = px.area(
        sales_by_publisher,
        x='Global_Sales',
        y=sales_by_publisher.index,
        orientation="h",
        title="<b>Sales by Video Game According to Publisher </b>",
        color_discrete_sequence=["#0083B8"] * len(sales_by_publisher),
        template="plotly_white",
        )
        
    fig_publisher_sale.update_layout(
        #xaxis=dict(tickmode="linear"),
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=(dict(showgrid=False))
        )
        
        
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_game_sale, use_container_width=True)
    right_column.plotly_chart(fig_publisher_sale, use_container_width=True)
    
    
st.markdown("-----")


check4 = st.checkbox("To look at the Sactter Plot chick the button:")
print(check4)
if check4:
    
    
    sales_by_product_genre = (
        df_selection.groupby(by=['Genre']).sum()[['Global_Sales']].sort_values(by='Global_Sales')
        )
        
    fig_game_sale = px.scatter(
        sales_by_product_genre,
        y='Global_Sales',
        x=sales_by_product_genre.index,
        orientation="h",
        title="<b>Sales by Video Game Genre</b>",
        #color_discrete_sequence=["#0083B8"] * len(sales_by_product_genre),
        template="plotly_white",
        )
        
    fig_game_sale.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=(dict(showgrid=False))
        )
        
        
    sales_by_publisher = (
        df_selection.groupby(by=['Publisher']).sum()[['Global_Sales']].sort_values(by='Global_Sales')
    )
        
    fig_publisher_sale = px.scatter(
        sales_by_publisher,
        y='Global_Sales',
        x=sales_by_publisher.index,
        orientation="h",
        title="<b>Sales by Video Game According to Publisher </b>",
        #color_discrete_sequence=["#0083B8"] * len(sales_by_publisher),
        template="plotly_white",
    )

    fig_publisher_sale.update_layout(
        #xaxis=dict(tickmode="linear"),
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=(dict(showgrid=False))
    )
    
        
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_game_sale, use_container_width=True)
    right_column.plotly_chart(fig_publisher_sale, use_container_width=True)
    
st.markdown("-------")

check6 = st.checkbox("To look at the Pie Chart chick the button:")
print(check6)
if check6:
    
    sales_by_product_genre = (
        df_selection.groupby(by=['Genre']).sum()[['Global_Sales']].sort_values(by='Global_Sales')
    )
        
    fig_game_sale = px.pie(
        sales_by_product_genre,
        values='Global_Sales',
        names=sales_by_product_genre.index,
        # orientation="h",
        title="<b>Sales by Video Game Genre</b>",
        #color_discrete_sequence=["#0083B8"] * len(sales_by_product_genre),
        template="plotly_white",
    )
        
    fig_game_sale.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=(dict(showgrid=False))
    )
        
    sales_by_publisher = (
        df_selection.groupby(by=['Publisher']).sum()[['Global_Sales']].sort_values(by='Global_Sales')
    )
        
    fig_publisher_sale = px.pie(
        sales_by_publisher,
        values='Global_Sales',
        names=sales_by_publisher.index,
        #orientation="h",
        title="<b>Sales by Video Game According to Publisher </b>",
        #color_discrete_sequence=["#0083B8"] * len(sales_by_publisher),
        template="plotly_white",
    )
        
    fig_publisher_sale.update_layout(
        #xaxis=dict(tickmode="linear"),
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=(dict(showgrid=False))
    )
    
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_game_sale, use_container_width=True)
    right_column.plotly_chart(fig_publisher_sale, use_container_width=True)
    
st.markdown("---")

check8 = st.checkbox("To look at the Histogram chick the button:")
print(check8)
if check8:
    
    sales_by_product_genre = (
        df_selection.groupby(by=['Genre']).sum()[['Global_Sales']].sort_values(by='Global_Sales')
    )
        
    fig_game_sale = px.histogram(sales_by_product_genre,y='Global_Sales',
        x=sales_by_product_genre.index,title="<b>Sales by Video Game Genre</b>",color='Global_Sales')
    
    sales_by_publisher = (
        df_selection.groupby(by=['Publisher']).sum()[['Global_Sales']].sort_values(by='Global_Sales')
    )

    fig_publisher_sale = px.histogram(sales_by_publisher, y='Global_Sales',
        x=sales_by_publisher.index,title="<b>Sales by Video Game According to Publisher </b>",color='Global_Sales')
    
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_game_sale, use_container_width=True)
    right_column.plotly_chart(fig_publisher_sale, use_container_width=True)
    
st.markdown("---")

check9 = st.checkbox("To look at the Plotly-Line Chart (Transpose) chick the button:")
print(check9)
if check9:
    
    sales_by_product_genre = (
        df_selection.groupby(by=['Genre']).sum()[['Global_Sales']].sort_values(by='Global_Sales')
    )
        
    fig_game_sale = px.line(sales_by_product_genre,title="<b>Sales by Video Game Genre</b>")
    
    sales_by_publisher = (
        df_selection.groupby(by=['Publisher']).sum()[['Global_Sales']].sort_values(by='Global_Sales')
    )
        
    fig_publisher_sale = px.line(sales_by_publisher,title="<b>Sales by Video Game According to Publisher </b>")
    
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_game_sale, use_container_width=True)
    right_column.plotly_chart(fig_publisher_sale, use_container_width=True)
    
st.markdown("----")

check10 = st.checkbox("To look at the Box Plot chick the button:")
print(check10)
if check10:
    
    sales_by_product_genre = (
        df_selection.groupby(by=['Genre']).sum()[['Global_Sales']].sort_values(by='Global_Sales')
        )
        
    fig_game_sale = px.box(sales_by_product_genre,title="<b>Sales by Video Game Genre</b>")
        
    sales_by_publisher = (
        df_selection.groupby(by=['Publisher']).sum()[['Global_Sales']].sort_values(by='Global_Sales')
    )
        
    fig_publisher_sale = px.box(sales_by_publisher,title="<b>Sales by Video Game According to Publisher </b>")
        
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_game_sale, use_container_width=True)
    right_column.plotly_chart(fig_publisher_sale, use_container_width=True)
    
st.markdown("---")


