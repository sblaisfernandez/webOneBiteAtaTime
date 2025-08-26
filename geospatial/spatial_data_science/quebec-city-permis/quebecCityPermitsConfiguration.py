quebecCityPermitsColumns = {
    "NUMERO_PERMIS": "permit_number",
    "DATE_DELIVRANCE": "issue_date",
    "ADRESSE_TRAVAUX": "work_address",
    "DOMAINE": "domain",
    "LOTS_IMPACTES": "affected_lots",
    "TYPE_PERMIS": "permit_type",
    "RAISON": "reason",
    "ARRONDISSEMENT": "borough",
    "GEOMETRY": "geometry",
}


mySupabase = {
    "databaseName": "real-estate",
    "table": {
        "quebec_city_permits": {
            "name": "quebec_city_permits",
            "columns": quebecCityPermitsColumns,
            "geometry_type": "POINT",
            "primary_key": "id",
        }
    },
}
