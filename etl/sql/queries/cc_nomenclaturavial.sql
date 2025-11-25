-- Consulta para extraer datos de la tabla cc_nomenclaturavial

SELECT
    id,
    geometria,
    numero_via,
    cl.text_code as tipo_via
FROM {schema}.cc_nomenclaturavial cl
JOIN {schema}.cc_nomenclaturavial_tipo_via cn ON cn.id = cl.tipo_via;
