INSERT INTO {schema}.col_masccl (
    t_id,
    ccl_mas,
    ue_mas_gc_terreno,
    ue_mas_gc_unidadconstruccion
)
SELECT
    nextval('{schema}.t_ili2db_seq'::regclass),
    l.t_id,
    t.t_id,
    uc.t_id
FROM tmp_col_masccl tm
LEFT JOIN {schema}.gc_lindero l ON tm.ccl_mas::text = l.local_id
LEFT JOIN {schema}.gc_terreno t ON tm.ue_mas_gc_terreno::text = t.local_id
LEFT JOIN {schema}.gc_unidadconstruccion uc ON tm.ue_mas_gc_unidadconstruccion::text = uc.local_id;
