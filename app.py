# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 14:20:11 2021

@author: Acer
"""

#%%
import numpy as np
import streamlit as st
import pandas as pd
import seaborn as sns
import plotly_express as px
import matplotlib.pyplot as plt

st.set_page_config(page_title='Sales of Video Games',
                   page_icon=":sunny:",
                   layout='wide')

st.subheader("Importing the dataset :mortar_board: ")

#st.set_option('deprecation.showfileUploaderEncoding', False)

uploaded_file = st.file_uploader(label="Upload your csv or excel (schema) file of vsales. (200 MB max)",
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


check_raw = st.sidebar.checkbox("data cleaning and preprossing")
print(check_raw)
if check_raw:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.subheader('Rows')
        st.subheader(df.shape[0])

    with col2:
        st.subheader('Columns')
        st.subheader(df.shape[1])
            
    # with col3:
    #     st.header('NullValues')
    # #     st.title(len(df[df.isnull()].value_counts()))
    #     st.title(df.isnull().value_counts())
    with col3:
        st.subheader("Null Values")
        st.subheader(df.isnull().sum().sum())
    with col4:
        st.subheader('DuplicateRows')
        st.subheader(df.duplicated().sum())
        
    with col1: 
        st.subheader("Class Distribution")
        st.dataframe(df['Platform'].value_counts())
    with col2:
        st.subheader('Median Values')
        st.dataframe(df.median())
    with col3:
        st.subheader("Standard Deviation sales")
        st.dataframe(df.std())

    with col4: 
        st.subheader("Columns")
        st.dataframe(df.columns)

    with st.expander("Data Describe"):
        st.dataframe(df.describe().T)
        
        
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
    
    
    st.header("Video Game's Sales comparision between world, European Union, North America and Japan :flashlight: ")
    st.markdown("##")
        
    total_sales = int(df_selection['Global_Sales'].sum())
    average_NA_sales = round(df_selection['NA_Sales'].mean(),1)
    total_NA_sales = int(df_selection['NA_Sales'].sum())
    average_EU_sales = round(df_selection['EU_Sales'].mean(),1)
    total_EU_sales = int(df_selection["EU_Sales"].sum())
    total_average_sale = round(df_selection['Global_Sales'].mean(),1)
    total_JP_Sales = int(df_selection['JP_Sales'].sum())
    average_JP_Sales = round(df_selection['JP_Sales'].mean(),1)
    
    left_column, left_middle_column, right_middle_column, right_column = st.columns(4)
    with left_column:
        st.subheader("Total Sales World Wide:")
        st.subheader(f"US $ {total_sales:,}")
    with left_middle_column:
        st.subheader("Total Sales in North America: ")
        st.subheader(f"US $ {total_NA_sales:,}")
    with left_middle_column:
        st.subheader("Average Sales in North America: ")
        st.subheader(f"US $ {average_NA_sales:,}")
    with right_middle_column:
        st.subheader("Total Sales in Japan: ")
        st.subheader(f"US $ {total_JP_Sales:,}")
    with right_middle_column:
        st.subheader("Average Sales in Japan: ")
        st.subheader(f"US $ {average_JP_Sales:,}")
    with right_column:
        st.subheader("Total Sales in European Union: ")
        st.subheader(f"US $ {total_EU_sales:,}")
    with right_column:
        st.subheader("Average Sales in European Union: ")
        st.subheader(f"US $ {average_EU_sales:,}")
    with left_column:
        st.subheader("Total World Wide Average Sale: ")
        st.subheader(f"US $ {total_average_sale:,}")
        
    st.markdown("""---------""")
        

   
    st.subheader("From here you can select the options from sidebar multiselect menu. :bar_chart: ")
    check1 = st.expander("To look at the Bar Chart chick the button:")
    print(check1)
    with check1:
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
       
        
   
        
    
    check6 = st.expander("To look at the Pie Chart chick the button:")
    print(check6)
    with check6:
        
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
        
    
    check8 = st.expander("To look at the Histogram chick the button:")
    print(check8)
    with check8:
        
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
        
    
    st.markdown("-------")
    
    st.subheader("Whole data Visualization :sunny:")
    check11 = st.checkbox("Visualize the data")
    print(check11)
    if check11:
        st.subheader('Now Time To Understand Our Whole Data By Seeing It :clipboard: ')
        if st.checkbox('Which Brand is Highest Product value'):
            st.title('See The Distribution')
            st.set_option('deprecation.showPyplotGlobalUse', False)
            sns.barplot(x='Platform', y='Global_Sales', data=df)
            plt.xticks(rotation='vertical')
            st.pyplot()
    
        if st.checkbox('Check Which Genre is The Best Seller'):
            st.title('See The Best Selling Genre')
            st.bar_chart(df['Genre'].value_counts())
            
        if st.checkbox('See Distribution of our Global_Sales_Price'):
            st.set_option('deprecation.showPyplotGlobalUse', False)
            sns.distplot(np.log(df['Global_Sales']))
            st.pyplot()
                
        if st.checkbox('See How The Other Sell Help to Growing the GlobalPrice'):
            if st.checkbox('See How Na Sales Varies for Global Sales'):
                st.set_option('deprecation.showPyplotGlobalUse', False)
                sns.lmplot(x='NA_Sales', y='Global_Sales', data=df)
                plt.xticks(rotation='vertical')
                st.pyplot()
    
            if st.checkbox('See How EU Sales Varies for Global Sales'):
                st.set_option('deprecation.showPyplotGlobalUse', False)
                sns.lmplot(x='EU_Sales', y='Global_Sales', data=df)
                plt.xticks(rotation='vertical')
                st.pyplot()
    
            if st.checkbox('See How JP Sales Varies for Global Sales'):
                st.set_option('deprecation.showPyplotGlobalUse', False)
                sns.lmplot(x='JP_Sales', y='Global_Sales', data=df)
                plt.xticks(rotation='vertical')
                st.pyplot()
    
            if st.checkbox('See How Other Sales Varies for Global Sales'):
                st.set_option('deprecation.showPyplotGlobalUse', False)
                sns.lmplot(x='Other_Sales', y='Global_Sales', data=df)
                plt.xticks(rotation='vertical')
                st.pyplot()
                        
                
            
    st.markdown("------")           
            
    st.subheader("Outlier Detection Using Box Plot. :art:")
    with st.expander("Outlier Detection Plot for North America Sales using Genre"):
        fig = plt.figure()
        sns.boxplot(df['NA_Sales'])
        st.pyplot(fig)
            
        p3 = px.box(df,x='NA_Sales',color='Genre')
        st.plotly_chart(p3,use_container_width=True)
                    
    with st.expander("Outlier Detection Plot for Japan Sales using Genre"):
        fig = plt.figure()
        sns.boxplot(df['JP_Sales'])
        st.pyplot(fig)
        
        p3 = px.box(df,x='JP_Sales',color='Genre')
        st.plotly_chart(p3,use_container_width=True)
                    
    with st.expander('Outlier Detection plot for Eeropean Union Sales using Genre'):
        fig = plt.figure()
        sns.boxplot(df['EU_Sales'])
        st.pyplot(fig)
        
        p3 = px.box(df,x='EU_Sales',color='Genre')
        st.plotly_chart(p3,use_container_width=True)
                
    with st.expander("Outlier detection plot for Global Sales using Genre"):
        fig = plt.figure()
        sns.boxplot(df['Global_Sales'])
        st.pyplot(fig)
        
        p3 = px.box(df,x='Global_Sales',color='Genre')
        st.plotly_chart(p3,use_container_width=True)
                    
    st.markdown("------") 
    
    st.subheader("Correlation Plot. :art:")
    with st.expander("correlation Plot"):
        corr_matrix = df.corr()
        fig = plt.figure(figsize=(20,10))
        sns.heatmap(corr_matrix,annot=True)
        st.pyplot(fig)
                   
        p4 = px.imshow(corr_matrix)
        st.write("Correlation matrix using plotly below. :memo:")
        st.plotly_chart(p4,use_container_width=True)
    
           
        
