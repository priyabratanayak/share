import pandas as pd
import base64
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go

def app():
    # for wider screen
    background_color = '#F5F5F5'
    
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
    if add_selectbox == "Semantic Search":
    
        with st.form(key="Semantic_Similarity"):
            # create radio button
            col1, col2, col3, col4,col5 = st.columns([0.5,1, 1,1, 0.5])
            with col1:
                
                radiobutton_category = col1.radio(
                    " Category: ", ("Regular", "Cover","AMO"))
                
            with col2:            
                # create an input search bar
                qt = col2.text_input("Quantity")
                radiobutton_type = col2.radio(
                    " Type: ", ("Normal", "Intraday (MIS)"))
            with col3:            
                # create an input search bar
                price = col3.text_input("Price") 
                tr_price = col3.text_input("Trigger Price") 
            with col4:
                st.write("")
                st.write("")
                if st.checkbox("Stop Loss"): 
                    st.write("Checked")
                    pass
                st.write("")
                
                sl_price = col4.text_input("SL Price %") 
            with col5:
                st.write("")
                st.write("")
                # Create a search button
                searchbutton = st.form_submit_button(label="Buy")
                st.write("")
                
                st.write("")
                cancel = st.form_submit_button(label="Cancel")
            st.session_state.radio = radiobutton_type
            st.session_state.counter_two = pd.DataFrame()
            placeholder = st.empty()
    
            if st.session_state.radio == "Search in Master usecase table":
                if qt == '':
                    if searchbutton:
                        st.error("Please enter the query")
    
                elif (len(qt) > 0):
                    msg = placeholder.info('Fetching data. Kindly Wait...')
                    #st.subheader("Search Results")
                    master_usecase_output = None
                    if (master_usecase_output.shape[0] > 0):
                        left, right, right_most = st.columns([3.5, 2.5, 0.5])
                        msg.subheader('Search Results')
                        left.write(master_usecase_output)
                        df = pd.DataFrame(master_usecase_output)
                        csv = df.to_csv(index=False)
                        # some strings <-> bytes conversions necessary here
                        b64 = base64.b64encode(csv.encode()).decode()
                        href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (To download the file right-click and save as &lt;name&gt;.csv)'
                        left.markdown(href, unsafe_allow_html=True)
                        left.write(
                            "To view the Microbots associated with Deployment id's please enter the Deployment id below")
    
                    search_dpid = right.text_input(" Enter Deployement ID: ")
                    right_most.write("")
                    right_most.write("")
                    submitbutton = right_most.form_submit_button(label='Submit')
    
                    # Create a search button
                    if search_dpid == "":
                        if submitbutton:
                            right.error("Please enter the Deployment id")
    
                    elif (len(search_dpid) > 0):
                        bot_depid_output = None
                        if bot_depid_output.shape[0] == 0:
                            right.error(" Search returned zero records.")
                        else:
                            right.subheader("Search Results")
                            right.write(bot_depid_output)
    
            elif st.session_state.radio == "Search in Bot description table":
                if qt == '':
                    if searchbutton:
                        st.error("Please enter the query")
    
                elif (len(qt) > 0):
                    msg = placeholder.info('Fetching data. Kindly Wait...')
                    bot_descriptions_output =None
                   
                    if bot_descriptions_output.shape[0] > 0:
                        msg.subheader("Search Result")
                        st.write(bot_descriptions_output)
                        df1 = pd.DataFrame(bot_descriptions_output)
                        csv = df1.to_csv(index=False)
                        # some strings <-> bytes conversions necessary here
                        b64 = base64.b64encode(csv.encode()).decode()
                        href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as &lt;some_name&gt;.csv)'
                        st.markdown(href, unsafe_allow_html=True)
    
    if add_selectbox == "String Search":
        with st.form(key="String_Similarity"):
            # create radio button
            col_1, col_2, col_3, col_4 = st.columns([2, 3.5, 0.5, 1])
            radio_button = col_1.radio(
                " Select table: ", ("Search in Master usecase table", "Search in Bot description table"))
    
            # create an input search bar
            search_bar = col_2.text_input(" Enter search string: ")
    
            with col_4:
                st.write("")
                st.write("")
                # Create a search button
                search_button = st.form_submit_button(label="Search")
    
            st.session_state.radio = radio_button
            st.session_state.counter_two = pd.DataFrame()
            place_holder = st.empty()
    
            if st.session_state.radio == "Search in Master usecase table":
                if search_bar == '':
                    if search_button:
                        st.error("Please enter the query")
    
                elif (len(search_bar) > 0):
                    msg = place_holder.info('Fetching data. Kindly Wait...')
                    #st.subheader("Search Results")
                    master_string = ""
                    if (master_string.shape[0] > 0):
                        msg.subheader('Search Results')
                        st.write(master_string)
                        dfs = pd.DataFrame(master_string)
                        csv = dfs.to_csv(index=False)
                        # some strings <-> bytes conversions necessary here
                        b64 = base64.b64encode(csv.encode()).decode()
                        href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (To download the file right-click and save as &lt;name&gt;.csv)'
                        st.markdown(href, unsafe_allow_html=True)
                        st.write(
                            "To view the Microbots associated with Deployment id's please enter the Deployment id below")
    
                    search_dp_id = st.text_input(" Enter Deployement ID: ")
                    submit_button = st.form_submit_button(label='Submit')
    
                    # Create a search button
                    if search_dp_id == "":
                        if submit_button:
                            st.error("Please enter the Deployment id")
    
                    elif (len(search_dp_id) > 0):
                        bot_dep_id_output =None
                        if bot_dep_id_output.shape[0] == 0:
                            st.error(" Search returned zero records.")
                        else:
                            st.subheader("Search Results")
                            st.write(bot_dep_id_output)
    
            elif st.session_state.radio == "Search in Bot description table":
    
                if search_bar == '':
                    if search_button:
                        st.error("Please enter the query")
    
                elif (len(search_bar) > 0):
                    msg = place_holder.info('Fetching data. Kindly Wait...')
                    bot_str_desc_output =None
                    if bot_str_desc_output.shape[0] > 0:
                        msg.subheader("Search Result")
                        st.write(bot_str_desc_output)
                        dfs1 = pd.DataFrame(bot_str_desc_output)
                        csv = dfs1.to_csv(index=False)
                        # some strings <-> bytes conversions necessary here
                        b64 = base64.b64encode(csv.encode()).decode()
                        href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as &lt;some_name&gt;.csv)'
                        st.markdown(href, unsafe_allow_html=True)
