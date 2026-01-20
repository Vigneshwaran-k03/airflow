CREATE VIEW tech_parent_ids AS
WITH RECURSIVE tech_tree AS (

    /* Root nodes */
    SELECT
        t.id,
        t.id_parent,
        JSON_ARRAY() AS parent_ids
    FROM arbre_kit_technique t
    WHERE t.id_parent = 0

    UNION ALL

    /* Child nodes */
    SELECT
        c.id,
        c.id_parent,
        JSON_ARRAY_APPEND(p.parent_ids, '$', p.id) AS parent_ids
    FROM arbre_kit_technique c
    JOIN tech_tree p ON c.id_parent = p.id
)

SELECT * FROM tech_tree;
