
def user_in_group(user, group_name):
    return user.is_authenticated and user.groups.filter(name=group_name).exists()


def is_admin(user):
    return bool(
        user
        and user.is_authenticated
        and (user.is_superuser or user.is_staff or user_in_group(user, "admin"))
    )


def is_reviewer(user):
    return is_admin(user) or user_in_group(user, "reviewer")


def is_employee(user):
    return is_admin(user) or is_reviewer(user) or user_in_group(user, "employee")


def get_user_role(user):
    if is_admin(user):
        return "admin"
    if is_reviewer(user):
        return "reviewer"
    return "employee"