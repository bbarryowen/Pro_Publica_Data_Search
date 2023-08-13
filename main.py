from google_sheets import insertNames


def main():
    insertNames(
        "https://projects.propublica.org/nonprofits/organizations/912198760")
    insertNames(
        "https://projects.propublica.org/nonprofits/organizations/371341741")
    insertNames(
        "https://projects.propublica.org/nonprofits/organizations/271744129")


if __name__ == "__main__":
    main()
