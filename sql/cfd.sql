WITH initial_complete AS (
  SELECT 
    kanban_day.count AS complete_at_point_zero,
    kanban_column.order AS last_column
  FROM
    kanban_day
    JOIN kanban_column
        ON kanban_day.column_id = kanban_column.id
  [[ WHERE  {{ date }} ]]
  ORDER BY kanban_column.order DESC, kanban_day.date
  LIMIT 1
)

SELECT 
    kanban_day.date,
    kanban_column.name,
    kanban_column.order,
    CASE WHEN (kanban_column.order = last_column) THEN MAX(kanban_day.count) - MAX(complete_at_point_zero)
         ELSE MAX(kanban_day.count) END
         AS count
FROM 
    kanban_day
    JOIN kanban_column
        ON kanban_day.column_id = kanban_column.id
    CROSS JOIN initial_complete
WHERE
    extract(dow from kanban_day.date) = 0
    [[ AND {{ date }} ]]
GROUP BY 1, 2, 3, last_column
ORDER BY 3 DESC; 
