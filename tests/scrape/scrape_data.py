from pathlib import Path

# static sample of html text used for testing, scraped from
# https://comptroller.baltimorecity.gov/boe/meetings/minutes
html_path = Path.cwd() / "tests" / "scrape" / "sample_boe_page.html"
with open(html_path, "r") as file:
    HTML_TEXT = file.read()

# Example set of expected year links pulled from HTML_TEXT
YEAR_LINKS = {
    "2020": "https://comptroller.baltimorecity.gov/minutes-2020",
    "2019": "https://comptroller.baltimorecity.gov/2019",
    "2018": "https://comptroller.baltimorecity.gov/minutes-2018",
    "2017": "https://comptroller.baltimorecity.gov/boe/meetings/minutes",
    "2016": "https://comptroller.baltimorecity.gov/minutes-2016-0",
    "2015": "https://comptroller.baltimorecity.gov/minutes-2015",
    "2014": "https://comptroller.baltimorecity.gov/minutes-2014",
    "2013": "https://comptroller.baltimorecity.gov/minutes-2013",
    "2012": "https://comptroller.baltimorecity.gov/minutes-2012",
    "2011": "https://comptroller.baltimorecity.gov/minutes-2011",
    "2010": "https://comptroller.baltimorecity.gov/minutes-2010",
    "2009": "https://comptroller.baltimorecity.gov/minutes-2009",
}

# input to check_missing_pdfs()
MEETING_LINKS = {
    "2020": {
        "2020-01-15": "https://www.fake-path.com/2020-01-15",
        "2020-01-22": "https://www.fake-path.com/2020-01-22",
    },
    "2019": {
        "2019-01-09": "https://www.fake-path.com/2019-01-15",
        "2019-01-16": "https://www.fake-path.com/2019-01-08",
    },
}

LINKS_2017 = {
    "2017_01_11": "https://comptroller.baltimorecity.gov/files/0001-00792017-01-11pdf",
    "2017_01_12": "https://comptroller.baltimorecity.gov/files/0080-00982017-01-12pdf",
    "2017_01_18": "https://comptroller.baltimorecity.gov/files/0099-01832017-01-18pdf",
    "2017_01_25": "https://comptroller.baltimorecity.gov/files/0184-03092017-01-25pdf",
    "2017_04_05": "https://comptroller.baltimorecity.gov/files/1131-12162017-04-05pdf",
    "2017_04_12": "https://comptroller.baltimorecity.gov/files/1217-13402017-04-12pdf",
    "2017_04_26": "https://comptroller.baltimorecity.gov/files/1341-14962017-04-26pdf",
    "2017_08_09": "https://comptroller.baltimorecity.gov/files/3104-32622017-08-09pdf",
    "2017_08_16": "https://comptroller.baltimorecity.gov/files/3263-34112017-08-16pdf",
    "2017_08_23": "https://comptroller.baltimorecity.gov/files/3412-35702017-08-23pdf",
    "2017_08_30": "https://comptroller.baltimorecity.gov/files/3571-36892017-08-30pdf",
    "2017_12_06": "https://comptroller.baltimorecity.gov/files/5085-52472017-12-06pdf",
    "2017_12_13": "https://comptroller.baltimorecity.gov/files/5248-54812017-12-13pdf",
    "2017_12_20": "https://comptroller.baltimorecity.gov/files/5482-55802017-12-20pdf",
    "2017_02_01": "https://comptroller.baltimorecity.gov/files/0310-03822017-02-01pdf",
    "2017_02_08": "https://comptroller.baltimorecity.gov/files/0383-04642017-02-08pdf",
    "2017_02_15": "https://comptroller.baltimorecity.gov/files/0465-05812017-02-15pdf",
    "2017_07_12": "https://comptroller.baltimorecity.gov/files/2636-27832017-07-12pdf",
    "2017_07_19": "https://comptroller.baltimorecity.gov/files/2784-29372017-07-19pdf",
    "2017_07_26": "https://comptroller.baltimorecity.gov/files/2938-31032017-07-26pdf",
    "2017_06_07": "https://comptroller.baltimorecity.gov/files/2079-21802017-06-07pdf",
    "2017_06_12": "https://comptroller.baltimorecity.gov/files/2181-21852017-06-12pdf",
    "2017_06_12_meeting2": "https://comptroller.baltimorecity.gov/files/2186-22002017-06-12pdf",
    "2017_06_12_meeting3": "https://comptroller.baltimorecity.gov/sites/default/files/06-12-2017%20SPECIALMEETING.pdf",
    "2017_06_14": "https://comptroller.baltimorecity.gov/files/2201-23312017-06-14pdf",
    "2017_06_21": "https://comptroller.baltimorecity.gov/files/2332-24512017-06-21pdf",
    "2017_06_28": "https://comptroller.baltimorecity.gov/files/2452-26352017-06-28pdf",
    "2017_03_01": "https://comptroller.baltimorecity.gov/files/0582-07292017-03-01pdf",
    "2017_03_08": "https://comptroller.baltimorecity.gov/files/0730-08482017-03-08pdf",
    "2017_03_15": "https://comptroller.baltimorecity.gov/files/0849-09332017-03-15pdf",
    "2017_03_22": "https://comptroller.baltimorecity.gov/files/0934-10072017-03-22pdf",
    "2017_03_29": "https://comptroller.baltimorecity.gov/files/1008-11302017-03-29pdf",
    "2017_05_03": "https://comptroller.baltimorecity.gov/files/1497-16332017-05-03pdf",
    "2017_05_10": "https://comptroller.baltimorecity.gov/files/1634-17162017-05-10pdf",
    "2017_05_17": "https://comptroller.baltimorecity.gov/files/1717-18782917-05-17pdf",
    "2017_05_31": "https://comptroller.baltimorecity.gov/files/1879-20782017-05-31pdf",
    "2017_11_01": "https://comptroller.baltimorecity.gov/files/4591-46832017-11-01pdf",
    "2017_11_08": "https://comptroller.baltimorecity.gov/files/4684-48032017-11-08pdf",
    "2017_11_15": "https://comptroller.baltimorecity.gov/files/4804-49082017-11-15pdf",
    "2017_11_22": "https://comptroller.baltimorecity.gov/files/4909-50842017-11-22pdf",
    "2017_10_04": "https://comptroller.baltimorecity.gov/files/4100-42232017-10-04pdf",
    "2017_10_11": "https://comptroller.baltimorecity.gov/files/4224-43362017-10-11pdf",
    "2017_10_18": "https://comptroller.baltimorecity.gov/files/4337-44312017-10-18pdf",
    "2017_10_25": "https://comptroller.baltimorecity.gov/files/4432-45902017-10-25pdf",
    "2017_09_13": "https://comptroller.baltimorecity.gov/files/3690-38152017-09-13pdf",
    "2017_09_20": "https://comptroller.baltimorecity.gov/files/3816-39312917-09-20pdf",
    "2017_09_27": "https://comptroller.baltimorecity.gov/files/3932-40992017-09-27pdf",
}
