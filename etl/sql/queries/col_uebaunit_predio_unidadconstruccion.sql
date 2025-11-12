SELECT  
gu.id as ue_gc_unidadconstruccion,
unidad

FROM {schema}.col_uebaunit cu
JOIN {schema}.gc_unidadconstruccion gu ON cu.ue_gc_unidadconstruccion = gu.id;