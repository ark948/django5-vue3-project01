def user_is_employee(user):
    if user.groups.filter(name='Employees').exists():
        print("\nACCESS GRANTED\n")
        return True
    print("\nBLOCKED\n")