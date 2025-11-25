INSERT INTO {schema}.gc_agrupacioninteresados
( t_id
, t_ili_tid
, tipo
, nombre
--, tipo_interesado
--, tipo_documento
--, numero_documento
, comienzo_vida_util_version
, espacio_de_nombres
, local_id)
SELECT 
 nextval('{schema}.t_ili2db_seq'::regclass)
,uuid_generate_v4()
,git.t_id as tipo_agrupacion
,nombre
--,it.t_id as interesadotipo
--,dt.t_id as tipo_documento
--,numero_documento
,comienzo_vida_util_version::timestamp
,espacio_de_nombres
,id_agrupacion
FROM tmp_agrupacion_interesados ai
LEFT JOIN (
    SELECT DISTINCT ON (SPLIT_PART(ilicode, '_', 2)) 
        t_id, 
        ilicode
    FROM {schema}.col_grupointeresadotipo
    ORDER BY SPLIT_PART(ilicode, '_', 2), t_id
) git ON SPLIT_PART(ai.tipo_agrupacion, '_', 2) = SPLIT_PART(git.ilicode, '_', 2)
--left join {schema}.col_interesadotipo it  on ai.interesadotipo ILIKE '%' || it.ilicode || '%' 
--left join {schema}.col_documentotipo dt on ai.tipo_documento ILIKE '%' || dt.ilicode || '%' 
--WHERE dt.baseclass is not null; 


--Se comentan las lineas anterios porque al insertar los datos se generan nuevos registros en la tabla agrupacion interesados que no siguen las reglas de normalizacion de datos, la clase col_miembros es la que me permite relacionar la agrupacion con el interesado, no la misma tabla agrupacion interesados.  

