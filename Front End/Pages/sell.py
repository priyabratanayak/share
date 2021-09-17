import pandas as pd
import base64
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
from kiteconnect import KiteConnect
import numpy as np
def app():
    
    
    if 'category' not in st.session_state:
            st.session_state['category']=None
    if 'qt' not in st.session_state:
            st.session_state['qt']=None
    if 'type' not in st.session_state:
            st.session_state['type']=None
    if 'price' not in st.session_state:
            st.session_state['price']=None
    if 'tprice' not in st.session_state:
            st.session_state['tprice']=None
    if 'ordertype' not in st.session_state:
            st.session_state['ordertype']="Market"
    if 'sl_percent' not in st.session_state:
            st.session_state['sl_percent']=None
    if 'msg' not in st.session_state:
            st.session_state['msg']=None
    if 'placeholder_msg' not in st.session_state:
            st.session_state['placeholder_msg']=None
    if 'instrument' not in st.session_state:
            st.session_state['instrument']=None        
    if 'exchange' not in st.session_state:
            st.session_state['exchange']=None 
    kite = KiteConnect(api_key=st.session_state.key_secret[0])
    kite.set_access_token(st.session_state.access_token[1].strip())           
    # for wider screen
    background_color = '#F5F5F5'
    placeholder=None
    # print title
    st.title("Buy")
    components.html(
        """<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """)
    master_usecase_output = pd.DataFrame()
    placeholder = None
    add_selectbox = st.sidebar.selectbox(
        'Search Options',
        ('Semantic Search', 'String Search')
    )
    
    with st.form(key="sell"):
            
            # create radio button
            col1, col2, col3, col4,col5 = st.columns([0.5,1, 1,1, 0.5])
            with col1:
                st.session_state.exchange = col1.radio(
                    " Exchange: ", ("NSE","BSE"))
                st.session_state.category = col1.radio(
                    " Category: ", ("Regular", "Cover","AMO"))
                
            with col2:
                st.session_state.instrument = col2.text_input("Instrument / Order ID")
                st.session_state.qt = col2.text_input("Quantity")
                st.session_state.type = col2.radio(
                    " Type: ", ("Longterm CNC", "Intraday (MIS)"))
                st.session_state.placeholder_msg = st.empty()
                
            with col3:            
                # create an input search bar
                st.session_state.price = col3.text_input("Price") 
                st.session_state.tprice = col3.text_input("Trigger Price") 
                
            with col4:
                st.write("")
                st.write("")
                st.session_state.ordertype = col4.radio(
                    " Order Type: ", ("Market", "Limit","SL","SL-M"))
                
                st.write("")
                
                st.session_state.sl_percent = col4.text_input("SL Price %") 
            with col5:
                st.write("")
                st.write("")
                # Create a search button
                buybtn = st.form_submit_button(label="Sell")
                if buybtn:
                    
                    
                    
                    
                    if st.session_state.exchange=='NSE':                    
                        buy_exchange=kite.EXCHANGE_NSE
                    elif st.session_state.exchange=='BSE':                    
                        buy_exchange=kite.EXCHANGE_BSE
                        
                    
                    if st.session_state.category=='Regular':
                        buy_variety=kite.VARIETY_REGULAR
                    elif st.session_state.category=='Cover':
                        buy_variety=kite.VARIETY_CO
                    elif st.session_state.category=='AMO':
                        buy_variety=kite.VARIETY_AMO
                        
                        
                    if len(st.session_state.instrument)>0:
                        symbol=st.session_state.instrument
                        
                    if len(st.session_state.qt)>0:
                        buy_quantity=st.session_state.qt
                    
                    if st.session_state.type=='Longterm CNC':
                        buy_product=kite.PRODUCT_CNC
                    elif st.session_state.type=='Intraday (MIS)':
                        buy_product=kite.PRODUCT_MIS
                        
                        
                    if st.session_state.ordertype=='Market':
                        buy_ORDER_TYPE=kite.ORDER_TYPE_MARKET
                    elif st.session_state.ordertype=='Limit':
                        buy_ORDER_TYPE=kite.ORDER_TYPE_LIMIT
                    elif st.session_state.ordertype=='SL':
                        buy_ORDER_TYPE=kite.ORDER_TYPE_SL
                    elif st.session_state.ordertype=='SL-M':
                        buy_ORDER_TYPE=kite.ORDER_TYPE_SLM
                        
                        
                    
                    sl_price=st.session_state.sl_percent
                    
                    if st.session_state.category=='Regular':
                        if st.session_state.ordertype=='Market':
                            st.write(symbol)
                            st.write(buy_exchange)
                            st.write(kite.TRANSACTION_TYPE_BUY)
                            st.write(buy_quantity)
                            st.write(buy_ORDER_TYPE)
                            st.write(buy_product)
                            st.write(buy_variety)
                            sts=kite.place_order(tradingsymbol=symbol,
                                        exchange=buy_exchange,
                                        transaction_type=kite.TRANSACTION_TYPE_BUY,
                                        quantity=buy_quantity,
                                        order_type=buy_ORDER_TYPE,
                                        product=buy_product,
                                        variety=buy_variety)
                            st.write(sts)
                    
                    
                        
                    
                st.write("")
                st.write("")  
                cancel = st.form_submit_button(label="Cancel")
                if cancel:
                    if len(st.session_state.instrument)>0:
                        symbol=st.session_state.instrument
                        try:
                            msg=kite.cancel_order(order_id=symbol,variety=kite.VARIETY_REGULAR)
                            st.session_state.placeholder_msg.success(msg)
                        except:
                            st.session_state.placeholder_msg.error("Order cannot be cancelled as it is being processed")
                             
            
            orders = kite.orders()
            net_df=pd.DataFrame(orders) 
            if net_df.shape[0]>0:
                
                net_df=net_df[['order_id','transaction_type','tradingsymbol','product','quantity','average_price','status']]
                net_df=net_df[net_df['transaction_type']=='SELL']
                net_df = net_df.rename({'order_id':'Order ID','transaction_type':'Type','tradingsymbol':'Instrument','product':'Product',"quantity":'Qty.','average_price':'Avg.','status':'Status'}, axis='columns')
                
                net_df.index = np.arange(1, len(net_df) + 1)
                st.subheader("Use the Order ID to Cancel an InProcess or Open Order")
                st.table(net_df)
                
                fig=go.Figure(data=go.Table(
                    columnwidth=[0.1,0.1,0.2,0.1,0.1,0.1,0.1],
                    header=dict(values=list(["Row No.",'Order ID',"Type","Instrument",'Product',"Qty.","Avg.",'Status']),
                    fill_color='#FD8E72',align='center'),cells=dict(values=([net_df.index[:],net_df["Order ID"][0:].tolist(),net_df["Type"][0:].tolist(),net_df["Instrument"][0:].tolist(),net_df["Product"][0:].tolist(),net_df["Qty."][0:].tolist(),net_df["Avg."][0:].tolist(),net_df["Status"][0:].tolist()]))))    
                fig.update_layout(width=1000,height=300,margin=dict(l=1,r=1,b=15,t=15),
                                        paper_bgcolor = background_color
                                        
                                        )
                