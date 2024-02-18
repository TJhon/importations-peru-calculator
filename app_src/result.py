from pydantic import BaseModel


class Result(BaseModel):
    # client
    client_name: str = None
    hs_code: str = None
    # user input
    ammount: float = None
    price_unit: float = None
    cbm: float = None
    total_kg: float = None
    # taxes values
    v_ad_valorem: float
    v_igv: float
    v_ipm: float
    v_antidupping: float
    v_perception: float
    v_insurage: float
    first_import: bool
    # environment values
    price_cbm: float
    # capital/port
    desconsolidation_ton: float
    transport_local_ton: float
    # province
    province: bool
    transport_local_province: float

    # TC

    tc: float = None
    real: bool = False

    fob: float = None
    cif: float = None
    freight: float = None
    freigth_taxes: float = None
    insurage: float = None
    total_taxes: float = None

    ad_valorem: float = None
    igv: float = None
    ipm: float = None
    perception: float = None
    antidupping: float = None

    # ad_valorem_p: float = None
    # igv_p: float = None
    # ipm_p: float = None
    # antidupping_p: float = None
    # perception_p: float = None

    desconsolidation: float = None
    transport_local: float = None
    province_transport: float = None
    total_logistic: float = None

    def run_all(self):

        self.calculate_fob()
        self.calculate_cif()
        self.calculate_taxes()
        self.logistic_cost()
        return self

    def calculate_fob(self):
        # print(self.real)
        # self.user_input
        fob = self.price_unit * self.ammount
        self.fob = fob

    def calculate_cif(self):
        insurage = self.v_insurage / 100 * self.fob
        freight = self.price_cbm * self.cbm
        cif = insurage + freight + self.fob
        self.insurage = insurage
        self.freight = freight
        self.freigth_taxes = insurage + freight
        self.cif = cif

    def calculate_taxes(self):
        cif = self.cif
        # self.ad_valorem_p = self.v_ad_valorem
        # self.igv_p = self.v_igv
        # self.ipm_p = self.v_ipm
        # self.antidupping_p = self.v_antidupping

        ad_valorem = cif * self.v_ad_valorem / 100
        igv = cif * self.v_igv / 100
        ipm = cif * self.v_ipm / 100
        antidupping = cif * self.v_antidupping / 100

        CIF = cif + ad_valorem + igv + ipm + antidupping

        if not self.first_import:
            self.v_perception = 3.5
        # self.perception_p = self.perception

        perception = CIF * self.v_perception / 100

        total_taxes = CIF + perception - cif

        self.ad_valorem = ad_valorem
        self.igv = igv
        self.ipm = ipm
        self.antidupping = antidupping
        self.perception = perception

        self.total_taxes = total_taxes

    def logistic_cost(self):
        total_kg = self.total_kg

        if total_kg is None:
            total_kg = self.ammount
        ton = total_kg / 1000

        desconsolidation = ton * self.desconsolidation_ton
        transport_local = ton * self.transport_local_ton * (1.18)

        province_transport = 0

        if self.province:
            dolar_ton_province = self.transport_local_province / self.tc
            province_transport = ton * dolar_ton_province

        total_transport_local = (
            province_transport
            + desconsolidation
            + transport_local
            + self.freight
            # + self.insurage
        )

        self.desconsolidation = desconsolidation
        self.transport_local = transport_local
        self.province_transport = province_transport
        self.total_logistic = total_transport_local


# a = Result_ins.model_validate({"tc": 12, "real": False})
# print(a)


# class User(BaseModel):
#     id: int
#     name: str = "John Doe"
#     # signup_ts: Optional[datetime] = None


# m = User.model_validate({"id": 123, "name": "James"})
# print(m)

# from pydantic import BaseModel


# class MyClass(BaseModel):
#     algo: int = None

#     def method(self):
#         self.algo = 12


# # Uso del método
# obj = MyClass()
# print(obj.algo)  # Output: None
# obj.method()
# print(obj.algo)  # Output: 12
