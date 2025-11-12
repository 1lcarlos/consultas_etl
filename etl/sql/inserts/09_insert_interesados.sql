INSERT INTO {schema}.gc_interesado
(t_id, t_ili_tid, tipo_documento, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, sexo, autoreconocimientoetnico, autoreconocimientocampesino, razon_social, nombre, tipo_interesado, numero_documento, comienzo_vida_util_version, espacio_de_nombres, local_id)
SELECT 
  --nextval('{schema}.t_ili2db_seq'::regclass)
  id_interesado
, uuid_generate_v4()
, dt.t_id as tipo_documento
, primer_nombre
, segundo_nombre
, primer_apellido
, segundo_apellido
, sti.t_id as sexo
, autrec.t_id as autoreconocimientoetnico
, false as autoreconocimientocampesino
, razon_social
, nombre
, it.t_id as tipointeresado
, documento_identidad as numero_documento
, comienzo_vida_util_version::timestamp
, espacio_de_nombres
--, estado_civil
--, tipo_verificado
, local_id
FROM tmp_interesado i
left join {schema}.gc_sexotipo sti on i.sexo ILIKE '%' || sti.ilicode || '%'  
left join {schema}.col_interesadotipo it on i.interesadotipo ILIKE '%' || it.ilicode || '%'  
left join {schema}.col_documentotipo dt on i.tipo_documento ILIKE '%' || dt.ilicode || '%'  
left join {schema}.gc_autoreconocimientoetnicotipo autrec on i.grupo_etnico ILIKE '%' || autrec.ilicode || '%' 
WHERE dt.baseclass is not null
