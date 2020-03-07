import httpx

STATS_URL_TEMPLATE = "https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/1/query?f=json&where=1=1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&cacheHint=true&outStatistics={out_statistics}"
STATS_PER_COUNTRY_URL = "https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/2/query?f=json&where=Confirmed > 0&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Confirmed desc&resultOffset=0&cacheHint=true"


def parse_summary_data():
    stats = {}
    for stat in ["confirmed", "deaths", "recovered"]:
        out_statistics = (
            '[{"statisticType":"sum","onStatisticField":"%s","outStatisticFieldName":"value"}]'
            % stat
        )
        url = STATS_URL_TEMPLATE.format(out_statistics=out_statistics)
        response = httpx.post(url)
        response.raise_for_status()
        raw_data = response.json()
        value = raw_data["features"][0]["attributes"]["value"]
        stats[stat] = value
    return stats


def parse_per_country_data():
    response = httpx.post(STATS_PER_COUNTRY_URL)
    response.raise_for_status()
    raw_data = response.json()
    countries_raw_data = raw_data["features"]
    return countries_raw_data
