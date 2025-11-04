INSERT INTO {schema}.gc_caracteristicasunidadconstruccion
(t_id, 
t_ili_tid, 
identificador, 
tipo_unidad_construccion, 
total_plantas, 
uso, 
anio_construccion, 
area_construida, 
estado_conservacion, 
observaciones, 
total_habitaciones, 
total_banios, 
total_locales)
SELECT
nextval('{schema}.t_ili2db_seq'::regclass),  
    uuid_generate_v4(),
    cu.identificador,
    cu.tipo_unidad_construccion,
    cu.total_plantas,
    uu.t_id as uso,
    anio_construccion,
    area_construida,
    CASE 
        WHEN cc.total_calificacion BETWEEN 0 AND 25 THEN 'Malo'
        WHEN cc.total_calificacion BETWEEN 26 AND 50 THEN 'Regular'
        WHEN cc.total_calificacion BETWEEN 51 AND 75 THEN 'Bueno'
        WHEN cc.total_calificacion BETWEEN 76 AND 100 THEN 'Excelente'
        ELSE 'Sin información'
    END AS estado_conservacion,
    cu.observaciones,
    cu.total_habitaciones,
    cu.total_banios,
    cu.total_locales

    FROM tmp_caracteristicasunidadconstruccion cu
    LEFT JOIN {schema}.gc_usouconstipo uu ON uu.ilicode ILIKE '%' || cu.uso || '%'
    LEFT JOIN {schema}.cuc_calificacionconvencional cc ON cc.gc_caracteristicasunidadconstruccion = cu.id