from requests import get, Response
from config import url, filename
from json import dump


def main():
    cmsURL = url
    categoriesCMS = []
    while True:
        response: Response = get(cmsURL)
        categoriesCMS = [*categoriesCMS, *response.json().get("data", [])]
        cmsURL = (
            response.json()
            .get("links", {"next": None})
            .get("next", {"href": None})
            .get("href", None)
        )
        if not cmsURL:
            break

    categories = list(
        map(
            lambda x: {
                "id": x.get("id"),
                "type": x.get("type"),
                "drupal_internal__tid": x.get("attributes").get("drupal_internal__tid"),
                "name": x.get("attributes").get("name"),
            },
            categoriesCMS,
        )
    )

    categories.sort(key=lambda x: x.get("name"))
    # Group categories by 'drupal_internal__tid' and find the maximum 'id' in each group
    filteredCategories = []
    for index, item in enumerate(categories):
        checkCategory = list(filter(lambda x: x.get("name") == item.get("name"), filteredCategories))
        if not len(checkCategory):
            filteredCategories.append(item)
        else:
            for check in checkCategory:
                if item.get("drupal_internal__tid") >= check.get("drupal_internal__tid"):
                    filteredCategories.remove(check)
                    filteredCategories.append(item)
    
    try:
        with open("output/" + filename, "w") as file:
            dump(filteredCategories, file)
    except BaseException as error:
        print(error)


if __name__ == "__main__":
    try:
        main()
    except BaseException as error:
        print(error)
