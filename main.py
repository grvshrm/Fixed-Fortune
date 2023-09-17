import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
from db_utils import MongoDBClient

st.set_page_config(
    page_title="Fixed Fortune",
    page_icon="🏛",
    # layout="wide",
)

st.markdown("""
<style>
.css-cio0dv          
{
            visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

selected = option_menu(
    menu_title = "Fixed Fortune",
    options = ["Reports", "Results", "Analytics"],
    icons = ["clipboard-data-fill", "database", "graph-up"],
    menu_icon = "cast",
    default_index = 1,
    orientation = "horizontal",
    styles = {
        "menu-title" : {'text-align': 'center;'},
    }
)

if selected == "Reports":
    st.header("Report Data")
    risk_data = pd.read_csv("risk_data.csv", index_col = False)
    st.dataframe(data = risk_data, width = 1000, height = 250)
    
if selected == "Results":
    # st.markdown("---")
    st.header("Bond Calculator")
    bond_file = st.file_uploader("Please Upload Bond Pricing Data:", type=["xlsx", "csv"])
    if bond_file:
        if '.csv' in bond_file.name:
            bond_data = pd.read_csv(bond_file.name, index_col = False)
            st.dataframe(data = bond_data, width = 1000, height = 250)
            if "risk_btn_clicked" not in st.session_state:
                st.session_state.risk_btn_clicked = False
            # def risk_click():
            #     st.session_state.risk_btn_clicked = True
            # btn_state = st.button("Calculate Risk", on_click = risk_click)
            btn_state = st.button("Calculate Risk")
            if btn_state or st.session_state.risk_btn_clicked:
                st.session_state.risk_btn_clicked = True
                from quant_lib import RiskCalculator
                rc = RiskCalculator(bond_data)
                risk_data = rc.calculate_risk()
                st.dataframe(data = risk_data, width = 1000, height = 250)
                save_btn = st.button("Save Results")
                if save_btn:
                    risk_data.to_csv("risk_data.csv", index = False)
                    mdb = MongoDBClient()
                    mdb.saveRiskData(risk_data)
                    st.success("Data Saved Successfully!")

        elif '.xlsx' in bond_file.name:
            print("xlsx file")

if selected == "Analytics":    
    st.header("Bond Data")
    if "details_btn_clicked" not in st.session_state:
        st.session_state.details_btn_clicked = False
    # def details_click():
    #     st.session_state.details_btn_clicked = True
    bond_name = st.text_input("Enter Bond Name")
    # details_btn = st.button("Get Details", on_click = details_click)
    details_btn = st.button("Get Details")
    if details_btn or st.session_state.details_btn_clicked:
        st.session_state.details_btn_clicked = True

        if bond_name:
            # with st.form("Bond Details Form"):
            mdb = MongoDBClient()
            bond_risk_data = mdb.get_risk_data(bond_name)
            if not bond_risk_data:
                st.warning("No data Found!")
            else:
                col1, col2 = st.columns(2)
                asset_id = col1.text_input(label = "Asset ID", value = bond_risk_data['asset_id'], disabled = True)
                bond_price = col2.text_input(label = "Bond Price", value = bond_risk_data['bond_price'], disabled = True)
                cpn_rate = col1.text_input(label = "Coupon Rate", value = bond_risk_data['coupon_rate'], disabled = True)
                face_val = col2.text_input(label = "Face Value", value = bond_risk_data['face_value'], disabled = True )
                time_period = col1.text_input(label = "Time Period", value = bond_risk_data['time_period'], disabled = True)
                ytm = col2.text_input("Yield To Maturity", value = bond_risk_data['ytm'], disabled = True)
                mdur = col1.text_input("Modified Duration", value = bond_risk_data['mdur'], disabled = True)
                conv = col2.text_input("Convexity", value = bond_risk_data['conv'], disabled = True)