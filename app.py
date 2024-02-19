import streamlit as st


from app_src.taxes_values import default_taxes
from components.sidebar import taxes, cost_volumen, other_parameters
from components.input_form import user_input
from components.summary import summary_imports

# Insert Data
st.title("Calculador de importaciones")

register_tab, summary_tab = st.tabs(["Registro", "Resumen"])


with register_tab:
    user_values, taxes_values = user_input()

    with st.sidebar:
        st.title("Parametros")
        if taxes_values is not None:
            tax = taxes(**taxes_values)
        else:
            tax = taxes(**default_taxes)
        volumen = cost_volumen()
        other = other_parameters()

    from data_client.client import (
        ClientPI,
        add_row,
        ClientPITaxes,
        TaxesValues,
        LogisticCost,
    )

    def add_data(user, table):
        client_input = table(**user)
        response = add_row(client_input)
        return response

    def valid_number(obj, name="Registro"):
        if obj is None:
            st.warning(f"Debe registrar correctamente el elment: {name}")
            st.stop()

    from app_src.result import Result

    if st.button("Registrar", use_container_width=True, type="primary"):

        for user in user_values:
            valid_number(user.get("price_unit"), "`Precio unitario`")
            valid_number(user.get("cbm"), "`Volumen del producto (CBM)`")
            valid_number(user.get("ammount"), "`Cantidad del producto`")

        results = [
            Result(**user, **tax, **volumen, **other).run_all() for user in user_values
        ]
        st.write(results)
        user = [add_data(result.model_dump(), ClientPI) for result in results]
        taxes_result = [
            add_data(result.model_dump(), ClientPITaxes) for result in results
        ]
        taxes_result = [
            add_data(result.model_dump(), TaxesValues) for result in results
        ]
        result = results[0]
        logistic = add_data(result.model_dump(), LogisticCost)

        st.success("Registro Completo")


with summary_tab:
    summary_imports(other)
