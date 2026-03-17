get_movement_of_quality_targets_query = """
        SELECT entity_id, target_name, priority_level 
        FROM targets
        WHERE (priority_level = 1 OR priority_level = 2)
        AND movement_distance_km >= 5;
        """

get_count_signal_type_query = """
    SELECT signal_type, COUNT(signal_type) as signal_count
    FROM intel_signals
    GROUP BY signal_type
    ORDER BY  COUNT(signal_type) DESC;
    """

get_top_3_unknown_entities_query = """
    SELECT entity_id, COUNT(entity_id) as reports_amount
    FROM intel_signals
    WHERE priority_level = 99
    GROUP BY entity_id
    order by COUNT(entity_id) DESC
    LIMIT 3;
    """

get_targets_that_wakes_up_query = """
    WITH static_targets as (
        SELECT entity_id, distance_from_last
        FROM `intel_signals`
        WHERE time(timestamp) BETWEEN '08:00:00' AND '20:00:00'
        GROUP BY entity_id, date(timestamp), distance_from_last
        HAVING distance_from_last = 0
        ),
        moving_targets as (
        SELECT entity_id, distance_from_last
        FROM intel_signals
        WHERE time(timestamp) BETWEEN '20:00:00' AND '08:00:00'
        GROUP BY entity_id, date(timestamp), distance_from_last
        HAVING distance_from_last >= 10
        )
        select entity_id 
        FROM moving_targets
        WHERE entity_id IN (SELECT entity_id FROM static_targets);
    """
