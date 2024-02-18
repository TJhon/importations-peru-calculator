
-- ALTER TABLE clientpi DROP COLUMN real BOOLEAN;
-- ALTER TABLE clientpi DROP COLUMN real;
-- SELECT * FROM clientpi;
DROP TABLE taxes_default;

CREATE TABLE taxes_default AS
SELECT 
    ad_valorem * 100 AS v_ad_valorem,
    excise_tax * 100 AS v_excise_tax,
    igv * 100 AS v_igv,
    ipm * 100 AS v_ipm,
    sp_tax * 100 AS v_sp,
    adp_tax * 100 AS v_antidupping,
    insurage * 100 AS v_insurage,
    surcharge_tax * 100 AS v_surcharge,
    penalty_charge * 100 AS v_penalty_charge,
    ley, hs_code
FROM taxes;

-- Si deseas eliminar la tabla original
