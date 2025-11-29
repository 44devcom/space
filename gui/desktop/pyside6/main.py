import sys
from PySide6.QtWidgets import QApplication
from wizard import Wizard


def main():
    app = QApplication(sys.argv)
    
    wizard = Wizard()
    wizard.show()
    
    result_code = wizard.exec()
    
    if result_code == Wizard.DialogCode.Accepted:
        results = wizard.getResults()
        print("Wizard completed with results:")
        print(f"Console: {results['console']}")
        print(f"Domain: {results['domain']}")
        print(f"Token: {'*' * len(results['token']) if results['token'] else '(empty)'}")
        print(f"IPv4: {results['ipv4']}")
        print(f"NS1: {results['ns1']}")
        print(f"NS2: {results['ns2']}")
        print(f"DNS: {results['dns']}")
        print(f"Email: {results['email']}")
        print(f"User: {results['user']}")
        print(f"Password: {'*' * len(results['password']) if results['password'] else '(empty)'}")
        print(f"Rule: {results['rule']}")
        print(f"Role: {results['role']}")
        print(f"Data: {results['data']}")
    else:
        print("Wizard cancelled or closed")
    
    sys.exit(0)


if __name__ == "__main__":
    main()

