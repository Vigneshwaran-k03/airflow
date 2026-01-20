CREATE VIEW catman_parent_ids AS
WITH RECURSIVE parent_tree AS (
    SELECT
        c.id AS child_id,
        p.id AS parent_id,
        p.id_parent,
        1 AS depth
    FROM catman_swap c
    JOIN catman_swap p ON p.id = c.id_parent

    UNION ALL

    SELECT
        pt.child_id,
        p.id,
        p.id_parent,
        pt.depth + 1
    FROM parent_tree pt
    JOIN catman_swap p ON p.id = pt.id_parent
),
ordered_tree AS (
    SELECT
        child_id,
        parent_id,
        depth
    FROM parent_tree
    ORDER BY child_id, depth DESC
)
SELECT
    child_id,
    CONCAT(
        '[',   -- comma added here
        GROUP_CONCAT(parent_id ORDER BY depth DESC SEPARATOR ','),
        ']'
    ) AS parent_ids
FROM ordered_tree
GROUP BY child_id;
