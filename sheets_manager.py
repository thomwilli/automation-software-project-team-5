import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

AHA_SHEET_ID = "1sG511m7sT2J_GXxuNuGUxcPJGbAU_fG1EmugEtCkdsg"
RQI_SHEET_ID = "1siiszreyU8T7ZiOmI08sasBrBB8R1lATPDqxgMY2SEs"


def connect_to_sheets():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", SCOPE
    )
    client = gspread.authorize(credentials)
    return client


# -------- AHA -------- #

def build_aha_row(student):
    return [
        student.get("email", ""),
        student.get("first_name", ""),
        "",
        student.get("last_name", ""),
        student.get("phone", ""),
        student.get("course", ""),
        student.get("date", ""),
        "YES",
        "",
        ""
    ]


def add_student_to_aha(student):
    client = connect_to_sheets()
    sheet = client.open_by_key(AHA_SHEET_ID).sheet1

    existing_emails = sheet.col_values(1)

    if student["email"] in existing_emails:
        print("Duplicate in AHA sheet.")
        return False

    sheet.append_row(build_aha_row(student))
    print("Added to AHA sheet.")
    return True


# -------- RQI -------- #

def build_rqi_row(student):
    return [
        "",
        student.get("location", ""),
        student.get("email", ""),
        student.get("first_name", ""),
        "",
        student.get("last_name", ""),
        student.get("email", ""),
        "",
        "",
        "",
        "Active",
        "",
        "",
        "",
        "",
        "",
        student.get("group", "")
    ]


def add_student_to_rqi(student):
    client = connect_to_sheets()
    sheet = client.open_by_key(RQI_SHEET_ID).sheet1

    existing_emails = sheet.col_values(7)

    if student["email"] in existing_emails:
        print("Duplicate in RQI sheet.")
        return False

    sheet.append_row(build_rqi_row(student))
    print("Added to RQI sheet.")
    return True


def update_both_sheets(student):
    add_student_to_aha(student)
    add_student_to_rqi(student)
