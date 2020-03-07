import httpx

STATS_URL_TEMPLATE = "https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/1/query?f=json&where=1=1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&cacheHint=true&outStatistics={out_statistics}"


def parse_data():
    stats = {}
    for stat in ["confirmed", "deaths", "recovered"]:
        out_statistics = (
            '[{"statisticType":"sum","onStatisticField":"%s","outStatisticFieldName":"value"}]'
            % stat
        )
        url = STATS_URL_TEMPLATE.format(out_statistics=out_statistics)
        response = httpx.post(url)
        response.raise_for_status()
        data = response.json()
        value = data["features"][0]["attributes"]["value"]
        stats[stat] = value
    return stats
