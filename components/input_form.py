import streamlit as st
from app_src.taxes_values import hs_taxes


def number_input(name, placeholder="123.23", value=None, min=0.0, default=st):
    return default.number_input(name, min, value=value, placeholder=placeholder)


def user_input():
    client = st.text_input("Nombre del Cliente", placeholder="AnyOne")
    hs_code = st.text_input("Ingrese el hsCode ", placeholder="2933.11.10.100")

    values = None
    if hs_code != "":
        values = hs_taxes(hs_code)

    col1, col2 = st.columns(2)

    with col1:
        ammount = number_input("Ingrese la cantidad en unidades del producto:")
        cbm = number_input("Cual es la dimension del producto (CBM):")
        price_unit_fake = number_input(
            "Ingresar un precio unitario diferente al `Real`?", value=None
        )

    with col2:
        price_unit = number_input("Cual es el precio unitario del producto: ")
        total_kg = number_input("Cual es el total de Kilogramos:", value=ammount)

    col_m1, col_m2 = st.columns(2)
    # with col_m2:

    if ammount and price_unit:
        total_fob = ammount * price_unit
        col_m1.metric("Real FOB", total_fob)

    if ammount and price_unit_fake:
        total_fob_f = ammount * price_unit_fake
        col_m2.metric("Fake FOB", total_fob_f)

    real = True
    if price_unit_fake and (price_unit_fake != price_unit):
        real = False

    insert_db = {
        "client_name": client,
        "hs_code": hs_code,
        "ammount": ammount,
        "price_unit": price_unit,
        "cbm": cbm,
        "total_kg": total_kg,
        "real": True,
    }
    insert_db_fake = insert_db.copy()
    insert_db_fake["price_unit"] = price_unit_fake
    insert_db_fake["real"] = real

    if real:
        return [insert_db], values
    else:
        return [insert_db, insert_db_fake], values
