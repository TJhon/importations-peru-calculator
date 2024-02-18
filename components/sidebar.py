import streamlit as st

# from


def taxes(v_ad_valorem, v_igv, v_ipm, v_antidupping, v_insurage, **kwargs):
    with st.expander("Calculo de Impuestos: (%)"):
        # st.title("Impuestos")
        seguro = st.number_input("Porcentaje del seguro (Sunat)", 0.0, value=v_insurage)
        ad_valorem = st.number_input("Ad Valorem", 0.0, value=v_ad_valorem)
        igv_percent = st.number_input("Impuesto General a las Ventas", 0.0, value=v_igv)
        ipm_percent = st.number_input("IPM", 0.0, value=v_ipm)
        antidupping_percent = st.number_input("Antidupping", 0.0, value=v_antidupping)
        first_import = st.checkbox("Primera importacion?")
    perception_percent = 10
    if not first_import:
        perception_percent = 3.5
    return {
        "v_perception": perception_percent,
        "v_insurage": seguro,
        "v_ad_valorem": ad_valorem,
        "v_igv": igv_percent,
        "v_ipm": ipm_percent,
        "v_antidupping": antidupping_percent,
        "first_import": first_import,
    }


def cost_volumen():
    with st.expander("Costos Respecto al volumen ($)"):
        price_cbm = st.number_input("Precio por CBM", value=35)
        desconsolidation_ton = st.number_input(
            "Desconsolidacion Por Tonelada", value=47.2
        )
        transporte_local = st.number_input("Transporte por Tonelada", value=65)
        province = st.checkbox("Es de provincia?")
        transporte_provincial = 450
        if province:
            transporte_provincial = st.number_input(
                "Transporte por Tonelada a Provincias (PEN)", value=450
            )
    return {
        "price_cbm": price_cbm,
        "province": province,
        "desconsolidation_ton": desconsolidation_ton,
        "transport_local_province": transporte_provincial,
        "transport_local_ton": transporte_local,
    }


def other_parameters():
    with st.expander("Otros Parametros"):
        st.subheader("Sunat - Peru")
        tc = st.number_input("Tipo de Cambio", value=3.81)
        st.subheader("Costos Por toda la importacion")
        trans_fee = st.number_input("Transmission Fee", value=51)
        handling = st.number_input("Handling", value=0)
        good_check = st.number_input("Visto Bueno", value=141)
        storage = st.number_input("Almacen", value=200)
        supervition = st.number_input("Supervicion de Embarque", value=100)
        custom_agent = st.number_input("Agente de aduandas", value=140)
        operating_cost = st.number_input("Costos Operativos", value=42)
    return {
        "trans_fee": trans_fee,
        "handling": handling,
        "good_check": good_check,
        "storage": storage,
        "shipmet_supervision": supervition,
        "custom_agent": custom_agent,
        "operating_cost": operating_cost,
        "tc": tc,
    }
