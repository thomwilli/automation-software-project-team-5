from rqi_generator import generate_rqi_csv

def main():

    students = [
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@email.com",
            "course": "BLS",
            "location": "Sacramento",
            "payment_status": "Paid",
            "date_registered": "2026-02-15"
        }
    ]

    generate_rqi_csv(students)

if __name__ == "__main__":
    main()
