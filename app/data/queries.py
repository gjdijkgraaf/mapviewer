class PostgreSQLQueries(object):
    # query with help from https://gis.stackexchange.com/questions/112057/
    # sql-query-to-have-a-complete-geojson-feature-from-postgis/191446#191446
    postgresql_fetch_bbox = """
SELECT jsonb_build_object(
    'type',         'FeatureCollection',
    'features',     jsonb_agg(features)
)
FROM (
    SELECT jsonb_build_object(
        'type',         'Feature',
        'id',           {0},
        'geometry',     ST_AsGeoJSON({1})::jsonb,
        'properties',   to_jsonb(inputs) - '{0}' - '{1}'
    ) AS feature
    FROM (
        SELECT *
        FROM {2}
        WHERE {2}.{1} && ST_MakeEnvelope({3}, {4}, {5}, {6}, {7})
        ) inputs) features;"""
