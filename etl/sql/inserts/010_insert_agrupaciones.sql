INSERT INTO {schema}.gc_agrupacioninteresados
( t_id
, t_ili_tid
, tipo
, nombre
, tipo_interesado
, tipo_documento
, numero_documento
, comienzo_vida_util_version
, espacio_de_nombres
, local_id)
SELECT 
id_agrupacion
,uuid_generate_v4()
,it.t_id as tipo_agrupacion
,nombre
,it.t_id as interesadotipo
,dt.t_id as tipo_documento
,numero_documento
,comienzo_vida_util_version::timestamp
,espacio_de_nombres
,id_agrupacion
FROM tmp_agrupacion_interesados ai
left join {schema}.col_grupointeresadotipo git on ai.tipo_agrupacion ILIKE '%' || git.ilicode || '%'  
left join {schema}.col_interesadotipo it  on ai.interesadotipo ILIKE '%' || it.ilicode || '%' 
left join {schema}.col_documentotipo dt on ai.tipo_documento ILIKE '%' || dt.ilicode || '%' 
WHERE git.baseclass is not null;   

