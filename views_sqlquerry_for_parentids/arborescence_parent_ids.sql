CREATE OR REPLACE VIEW arborescence_parent_ids AS
WITH RECURSIVE parent_tree AS (
    -- Base row
    SELECT
        a.id,
        a.id_parent,
        CAST(NULL AS CHAR(255)) AS parent_path,
        0 AS depth
    FROM arborescence a

    UNION ALL

    -- Walk up the tree
    SELECT
        pt.id,
        p.id_parent,
        CASE
            WHEN pt.parent_path IS NULL THEN CAST(p.id AS CHAR(255))
            ELSE CONCAT(p.id, ',', pt.parent_path)
        END AS parent_path,
        pt.depth + 1
    FROM parent_tree pt
    JOIN arborescence p
        ON pt.id_parent = p.id
)

SELECT
    id,
    COALESCE(
        JSON_ARRAYAGG(CAST(parent_id AS UNSIGNED)),
        JSON_ARRAY()
    ) AS parent_ids
FROM (
    SELECT
        id,
        depth,
        SUBSTRING_INDEX(
            SUBSTRING_INDEX(parent_path, ',', n.n),
            ',', -1
        ) AS parent_id
    FROM parent_tree
    JOIN (
        SELECT 1 n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL
        SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL
        SELECT 9 UNION ALL SELECT 10
    ) n
        ON parent_path IS NOT NULL
       AND n.n <= 1 + LENGTH(parent_path) - LENGTH(REPLACE(parent_path, ',', ''))
    ORDER BY id, depth DESC
) ordered_parents
GROUP BY id;
