import httpx

ARCGIS_BASE_URL = "https://services1.arcgis.com/0MSEUqKaxRlEPj5g/ArcGIS/rest/services/ncov_cases/FeatureServer"

ARCGIS_API_URL = f"{ARCGIS_BASE_URL}/1/query"
ARCGIS_REGION_API_URL = f"{ARCGIS_BASE_URL}/2/query"


def parse_summary_data():
    stats = {}
    for stat in ["confirmed", "deaths", "recovered"]:
        response = httpx.post(
            ARCGIS_API_URL,
            data={
                "where": "1=1",
                "outFields": "*",
                "cacheHint": "true",
                "outStatistics": '[{"statisticType":"sum","onStatisticField":"%s","outStatisticFieldName":"value"}]'
                % stat,
                "f": "pjson",
            },
            timeout=25.0,
        )
        response.raise_for_status()
        raw_data = response.json()
        value = raw_data["features"][0]["attributes"]["value"]
        stats[stat] = value
    return stats


def parse_per_region_data():
    response = httpx.post(
        ARCGIS_REGION_API_URL,
        data={
            "where": "Confirmed>0",
            "orderByFields": "Confirmed desc",
            "outFields": "*",
            "cacheHint": "true",
            "f": "pjson",
        },
        timeout=25.0,
    )
    response.raise_for_status()
    raw_data = response.json()
    regions_raw_data = raw_data["features"]
    return regions_raw_data
