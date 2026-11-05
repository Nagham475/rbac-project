
class RBAC:
    def __init__(self):
        self.role_permissions = {}   # role -> set of permissions
        self.user_roles = {}         # user -> role

    def add_role(self, role):
        self.role_permissions.setdefault(role, set())

    def assign_permission(self, role, permission):
        """Assign a permission (access right) to a role."""
        self.add_role(role)
        self.role_permissions[role].add(permission)

    def assign_role(self, user, role):
        """Assign a user to a role."""
        if role not in self.role_permissions:
            print(f"Error: role '{role}' does not exist.")
            return False
        self.user_roles[user] = role
        return True

    def check_access(self, user, permission):
        """Return True if the user's role has the requested permission."""
        role = self.user_roles.get(user)
        if role is None:
            return False
        return permission in self.role_permissions[role]


def setup():
    rbac = RBAC()
    rbac.assign_permission("Admin", "create")
    rbac.assign_permission("Admin", "view")
    rbac.assign_permission("Admin", "update")
    rbac.assign_permission("Admin", "delete")
    rbac.assign_permission("Manager", "view")
    rbac.assign_permission("Manager", "update")
    rbac.assign_permission("Customer", "view")
    return rbac


def show_roles(rbac):
    print("\n--- Roles and Permissions ---")
    for role, perms in rbac.role_permissions.items():
        print(f"{role}: {', '.join(sorted(perms))}")


def show_users(rbac):
    print("\n--- Users and Roles ---")
    if not rbac.user_roles:
        print("No users assigned yet.")
    for user, role in rbac.user_roles.items():
        print(f"{user} -> {role}")


def main():
    rbac = setup()
    while True:
        print("\n===== RBAC System (Account object) =====")
        print("1. Assign user to role")
        print("2. Show roles and permissions")
        print("3. Show users and roles")
        print("4. Test access (user, action)")
        print("5. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            user = input("User name: ").strip()
            role = input("Role (Admin/Manager/Customer): ").strip().capitalize()
            if rbac.assign_role(user, role):
                print(f"{user} was assigned to role {role}.")
        elif choice == "2":
            show_roles(rbac)
        elif choice == "3":
            show_users(rbac)
        elif choice == "4":
            user = input("User name: ").strip()
            action = input("Action (create/view/update/delete): ").strip().lower()
            if user not in rbac.user_roles:
                print(f"User '{user}' has no role. Access DENIED.")
            elif rbac.check_access(user, action):
                print(f"Access GRANTED: {user} ({rbac.user_roles[user]}) can {action} accounts.")
            else:
                print(f"Access DENIED: {user} ({rbac.user_roles[user]}) cannot {action} accounts.")
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()