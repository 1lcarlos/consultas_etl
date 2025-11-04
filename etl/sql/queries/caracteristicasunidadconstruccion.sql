SELECT DISTINCT
identificador, 
gu.text_code as tipo_unidad_construccion,
total_plantas,
uu.text_code as uso,
anio_construccion,
area as area_construida,
observacion,
total_habitaciones, 
total_banios, 
total_locales 
FROM {schema}.gc_caracteristicasunidadconstruccion gc
LEFT JOIN {schema}.gc_unidadconstrucciontipo gu ON gu.id = gc.tipo_unidad_construccion
LEFT JOIN {schema}.gc_usouconstipo uu ON uu.id = gc.uso;


