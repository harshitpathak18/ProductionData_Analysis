import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def product_target_achieved():
    m=df['Month target in nos']
    c=df['Cummalative ']

    # Monthly Target > Cummalative
    target_greater_than_cummalative= df[['Rating','Month target in nos','Cummalative ' ]].where(m >= c).dropna()

    # Monthly Target < Cummalative
    Cummalative_greater_than_target=df[['Rating','Month target in nos','Cummalative ' ]].where(m < c).dropna()

    
    return target_greater_than_cummalative,Cummalative_greater_than_target


st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 0rem;
                    padding-right: 0rem;
                }
        </style>
        """, unsafe_allow_html=True)

# -----------------------------------------------------
st.title("Production Data Analysis")


# -------------------------------------------------------
col1,col2=st.columns(2)
with col1:
    year=st.selectbox("Select Year",options=['2022','2023'])

with col2:
    if year=='2022':
        month=st.selectbox("Select Month",options=['Oct','Nov','Dec'])

    elif year=='2023':
        month=st.selectbox("Select Month",options=['Jan','Feb'])

# ---------------------------------------------------
string=f'{month}_{year}.xlsx'
df=pd.read_excel(string)
df.fillna(0,inplace=True)


# ---------------------------------------------------------
st.write("")
st.write("")
st.write("")
st.header(f"Top 5 Production Of {month} Month ")

top5_monthly=df[['Rating','Cummalative ']].sort_values(by='Cummalative ',ascending=False).head(5)
rt=[ i for i in top5_monthly['Rating']]
dd=[ i for i in top5_monthly['Cummalative ']]

col1,col2,col3,col4,col5=st.columns(5)
with col1:
    st.metric(label=rt[0], value=dd[0])
with col2:
    st.metric(label=rt[1], value=dd[1])
with col3:
    st.metric(label=rt[2], value=dd[2])
with col4:
    st.metric(label=rt[3], value=dd[3])
with col5:
    st.metric(label=rt[4], value=dd[4])

fig = px.pie(top5_monthly, values='Cummalative ', names='Rating',title="Top 5 Production of the month")
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig)

# ---------------------------------------------------------
st.write("")
st.write("")
st.write("")
st.subheader(f"Top 5 Productions For a Particular Day In {month} Month")
dates=[i for i in df.columns if type(i)==int]
dt=st.selectbox("Select Date",options=dates)

top5=df[['Rating',dt]].sort_values(by=dt,ascending=False).head(5)
rt=[i for i in top5['Rating']]
dd=[i for i in top5[dt]]

col1,col2,col3,col4,col5=st.columns(5)
with col1:
    st.metric(label=rt[0], value=int(dd[0]))
with col2:
    st.metric(label=rt[1], value=int(dd[1]))
with col3:
    st.metric(label=rt[2], value=int(dd[2]))
with col4:
    st.metric(label=rt[3], value=int(dd[3]))
with col5:
    st.metric(label=rt[4], value=int(dd[4]))
fig = px.pie(top5, values=dt, names='Rating',title="Top 5 Production of the day")
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig)



# -------------------------------------------------------
a,b=product_target_achieved()
st.write("")
st.write("")
st.write("")
st.header("Overall - Monthly Production Target Vs Production Achieved")
df1=pd.DataFrame()
df1['Target']=['Monthly Target','Cummalative']
df1['Production']=[df['Month target in nos'].sum(),df['Cummalative '].sum()]
fig=px.bar(data_frame=df1,x='Target', y='Production',color_discrete_map={'Monthly Target': '#FF870F','Cummalative': '#29BA8C'})
st.plotly_chart(fig)

col1,col2,col3=st.columns(3)
with col1:
    st.metric(label="Target", value=int(df['Month target in nos'].sum()))
with col2: 
    st.metric(label="Achieved", value=int(df['Cummalative '].sum()))
with col3:
    st.metric(label='Percentage %',value=round((int(df['Cummalative '].sum())/int(df['Month target in nos'].sum()))*100,2))




# --------------------------------------------------------------------
st.write("")
st.write("")
st.write("")
st.header("RatingWise - Monthly Production Target vs Production Achieved")
opt1=st.selectbox("Select Option",options=['Ratings where Monthly Target > Cummalative','Ratings where Monthly Target < Cummalative'])

if opt1=="Ratings where Monthly Target > Cummalative":
    st.subheader(f"Rating's whose Production Achieved is lagging behind than Monthly Production Target are - ")
    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc="sum", y=a['Month target in nos'], x=a['Rating'], name="Monthly Target"))
    fig.add_trace(go.Histogram(histfunc="sum",  y=a['Cummalative '], x=a['Rating'], name="Achieved"))
    st.plotly_chart(fig)
if opt1=="Ratings where Monthly Target < Cummalative":
    st.subheader(f"Rating's whose Production Achieved is ahead of Monthly Production Target are - ")
    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc="sum", y=b['Month target in nos'], x=b['Rating'], name="Monthly Target"))
    fig.add_trace(go.Histogram(histfunc="sum",  y=b['Cummalative '], x=b['Rating'], name="Achieved"))

    st.plotly_chart(fig)



