from typing import List


def displayElectoralDistrict(electoralDistrict: str) -> None:
    grouped = electoralDistrict.groupby("Province").size().reset_index(name="Count")
    grouped = grouped.sort_values(by="Count", ascending=False)

    plt.figure(figsize=(10, 6))
    plt.bar(grouped["Province"], grouped["Count"])
    plt.xlabel("Province")
    plt.ylabel("Count")
    plt.title("Count of Electoral Districts by Province")
    plt.xticks(rotation=45)
    plt.tight_layout()
    # Show the plot
    plt.show()


def getProvince(electoralDistrict: str) -> str:
    electoralDistrictDictionary = {
        10: "Newfoundland and Labrador",
        11: "Prince Edward Island",
        12: "Nova Scotia",
        13: "New Brunswick",
        24: "Quebec",
        35: "Ontario",
        46: "Manitoba",
        47: "Saskatchewan",
        48: "Alberta",
        59: "British Columbia",
        60: "Yukon",
        61: "Northwest Territories",
        62: "Nunavut",
    }
    province = "n.a."
    electoralDistrictCode = int(electoralDistrict[0:2])

    if electoralDistrictCode in electoralDistrictDictionary:
        province = electoralDistrictDictionary[electoralDistrictCode]

    return province
