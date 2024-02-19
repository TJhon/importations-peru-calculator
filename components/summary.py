import pandas as pd, sqlite3, streamlit as st


def query_df(
    query="Select * from clientpi",
    data_name: str = "./data/clients.sqlite",
    client=None,
) -> pd.DataFrame:

    conn = sqlite3.connect(data_name)

    if client is not None:
        query += "where client_name = {client}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def summary_imports(other):

    st.header("Summary / Resumen")

    clients = query_df("Select distinct client_name from clientpi")[
        "client_name"
    ].values

    # clients = query_df("clientpi", "distinct client_name")["client_name"].values

    client_select = st.selectbox("Selecciona al Cliente", clients)

    fob_df = query_df(
        f"""
        select * from clientpi 
        where client_name = '{client_select}'
        """
    )

    taxes_df = query_df(
        f"""
        select * from clientpitaxes
        where client_name = '{client_select}'
        """
    )
    taxes_values_df = query_df(
        f"""
        select distinct * from taxesvalues
        where client_name = '{client_select}'
        """
    )
    logistic_df = query_df(
        f"""
        select distinct * from logisticcost 
        where client_name = '{client_select}'
        """
    )

    # st.write('<hr style="border: 1px solid;">', unsafe_allow_html=True)

    real_fob = fob_df.query("real == 1")
    fake_fob = fob_df.query("real == 0")
    real_taxes = taxes_df.query("real == 1")
    fake_taxes = taxes_df.query("real == 0")

    real_total_cif = real_fob["cif"].sum()
    real_total_fob = real_fob["fob"].sum()

    logistic_relation = logistic_df[["freight", "total_logistic"]].sum().round(2)

    col_taxes = [
        "ad_valorem",
        "igv",
        "ipm",
        "insurage",
        "perception",
        "antidupping",
        "total_taxes",
    ]

    tax_real = real_taxes[col_taxes].sum().round(2)
    tax_fake = fake_taxes[col_taxes].sum().round(2)

    def cal_logistic_no_relation(values: dict):
        elements = list(values.keys())
        total = 0
        for element in elements:
            if element != "tc":
                total += values[element]
        return total

    logistic_no_relation = cal_logistic_no_relation(other)

    total_logistic = logistic_relation["total_logistic"] + logistic_no_relation
    total_real_taxes = tax_real["total_taxes"]
    total_real_insurage = tax_real["insurage"]
    total_fake_taxes = tax_fake["total_taxes"]
    total_fake_insurage = tax_fake["insurage"]
    total_cost_importation = total_logistic + real_total_fob + total_real_taxes

    diff_taxes = total_real_taxes - total_fake_taxes
    diff_taxes = round(diff_taxes, 2)

    diff_insurage = total_real_insurage - total_fake_insurage
    diff_insurage = round(diff_insurage, 2)

    total_diff = diff_taxes + diff_insurage

    fake = True
    if len(fake_taxes) < 1:
        fake = False
        diff_taxes = None
        diff_insurage = None
        total_diff = None

    st.metric("Costos de importacion Total", total_cost_importation, total_diff)
    st.divider()

    cm1, cm2, cm3 = st.columns(3)
    cm11, cm22, cm33 = st.columns(3)

    cm1.subheader("Valor")
    cm1.metric("Total FOB", real_total_fob)
    cm1.metric("Total CIF", real_total_cif)

    cm2.subheader("Taxes")
    cm2.metric("Total Taxes / Impuestos Totales", total_real_taxes, diff_taxes)

    cm3.subheader("Logistic")
    cm3.metric("Total Logistic Costs", total_logistic)
    cm3.metric(
        "Logistica Relacionada a la Carga",
        logistic_relation["total_logistic"],
        diff_insurage,
    )
    cm3.metric("Logistica No Relacionada", logistic_no_relation)

    st.subheader("Details / Detalles")

    with st.expander("FOB"):
        st.subheader("`Real values / Valores Reales`")
        st.dataframe(real_fob)
        if len(fake_fob) > 0:
            st.subheader("`Fake values / Valores Simulados`")
            st.dataframe(fake_fob)
    with st.expander("Impuestos / Taxes"):
        st.subheader("`Real values / Valores Reales`")
        st.dataframe(real_taxes)
        if len(fake_taxes) > 0:
            st.subheader("`Fake values / Valores Simulados`")
            st.dataframe(fake_taxes)
    with st.expander("Valores de Impuestos"):
        st.subheader("`Impuestos en base al HSCODE`")
        st.dataframe(taxes_values_df)

    with st.expander("Logistic Costs / Costos logisticos"):
        st.subheader("`Costos Relacionados`")
        st.dataframe(logistic_df)

    # real_taxes_v = taxes_values_df.
