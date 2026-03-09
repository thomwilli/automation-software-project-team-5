from sheets_manager import update_both_sheets

test_student = {
    "email": "teststudent123@email.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "5551234567",
    "course": "BLS",
    "date": "03/04/2026",
    "location": "TN Memphis",
    "group": "HeartCode BLS Complete - 2026"
}

update_both_sheets(test_student)