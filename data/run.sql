
-- ALTER TABLE clientpi DROP COLUMN real BOOLEAN;
-- ALTER TABLE clientpi DROP COLUMN real;
-- SELECT * FROM clientpi;
-- DROP TABLE taxes_default;

-- CREATE TABLE taxes_default AS
-- SELECT 
--     ad_valorem * 100 AS v_ad_valorem,
--     excise_tax * 100 AS v_excise_tax,
--     igv * 100 AS v_igv,
--     ipm * 100 AS v_ipm,
--     sp_tax * 100 AS v_sp,
--     adp_tax * 100 AS v_antidupping,
--     insurage * 100 AS v_insurage,
--     surcharge_tax * 100 AS v_surcharge,
--     penalty_charge * 100 AS v_penalty_charge,
--     ley, hs_code
-- FROM taxes;


SELECT 
    cp.hs_code,
    cp.real,
    cp.client_name,
    cp.ammount,
    cp.price_unit,
    cp.total_kg,
    cp.fob,
    SUM(ct.total_taxes + ct.insurage) AS total,
    lc.total_logistic
FROM 
    clientpi AS cp
JOIN 
    clientpitaxes AS ct ON cp.hs_code = ct.hs_code
JOIN 
    logisticcost AS lc ON cp.hs_code = lc.hs_code
GROUP BY 
    cp.id;

