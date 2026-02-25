import json
import rsa
import os


if os.path.isfile("contactos.json"):
    with open("contactos.json", "r", encoding="utf-8") as f:
        f.seek(0)
        contactos = json.load(f)
else:
    contactos = {'p':0, '0': 'Anonimo', 'n0': 0, 'e0': 0, 'd0': 0}        


def generate_and_register_keys():
    print("######## Generate keys ########")
    lower = int(input("Lower bound: "))
    upper = int(input("Upper bound: "))
    n, e, d = rsa.generate_keys(lower, upper)
    contactos['n0'] = n
    contactos['e0'] = e
    contactos['d0'] = d
    return "Keys generated and saved"

    
def register_user():
    print("######## Register user ########")
    contactos['0'] = input("Name: ")
    contactos['n0'] = int(input("     n: "))
    contactos['e0'] = int(input("     e: "))
    contactos['d0'] = int(input("     d: "))
    return "Keys saved"

    
def register_contact():
    print("######## New contact ########")
    name = input("Name: ")
    n = int(input("     n: "))
    e = int(input("     e: "))
    
    i = (len(contactos)-2)//3
    contactos[str(i)] = name
    contactos['n'+str(i)] = n
    contactos['e'+str(i)] = e
    return "Contact saved"

    
def encrypt_message():
    print("######## Message ########")
    print("Contacts")
    if len(contactos) <= 5:
        return "No contacts"
    for i in range(1,(len(contactos)-2)//3):

        print("{}. {}".format(i,contactos[str(i)]))
    try:
        recipient = input("To: ")
        n = contactos['n' + str(recipient)]
        e = contactos['e' + str(recipient)]
        p = contactos['p']
    except Exception:
        return "Contact not found"
    main()
    print("######## Message ########")
    print("To", contactos[recipient])
    message = input("> ")
    encrypted = rsa.encrypt_string(message, n, e, p)
    serialized = "".join(str(value) + " " for value in encrypted)[:-1]
        
    with open(contactos[recipient] + ".txt", "w", encoding="utf-8") as f:
        f.write(("From {} (n = {}, e = {})".format(contactos['0'], contactos['n0'], contactos['e0'])) + "\n")
        f.write(("To {} (n = {}, e = {}, p = {})".format(contactos[recipient], n, e, p)) + "\n")
        f.write(serialized)

    return "Encrypted message saved to {}.txt".format(contactos[recipient])


def decrypt_message():
    print("######## Message ########")
    if os.path.isfile(contactos['0']+".txt"):
        with open(contactos['0'] + ".txt", "r", encoding="utf-8") as f:
            sender = f.readline()
            receiver = f.readline()
            message = f.readline()
    else:
        return "No messages"
    parts = message.split(" ")
    p = int(receiver.split(" ")[-1].split(")")[0])
    cipher = list(map(int, parts))
    decrypted = rsa.decrypt_string(cipher, contactos['n0'], contactos['d0'], p)
    print(sender, decrypted)
    print()
    input("\033[3mPress Enter to continue\033[0m")
    return " "

    
def change_padding():
    print("######## Change padding ########")
    contactos['p'] = int(input("New padding: "))
    return "Padding updated"


def exit_program():
    with open("contactos.json", "w", encoding="utf-8") as f:
        json.dump(contactos, f)
    return ""

    
def main():
    os.system("cls")
    print("########", contactos['0'], "########")
    print("n =", contactos['n0'])
    print("e =", contactos['e0'])
    print("p =", contactos['p'])
    print()

if __name__ == "__main__":
    a = " "
    while a:
        main()
        print("######## Menu ########")
        print("1. Register user")
        print("2. Generate keys")
        print("3. New contact")
        print("4. Encrypt message")
        print("5. Decrypt message")
        print("6. Change padding")
        print("7. Exit")
        print()
        print("\033[3m" + a + "\033[0m")
        option = input("> ")
        main()
        try:
            if option == '1':
                a = register_user()
            elif option == '2':
                a = generate_and_register_keys()
            elif option == '3':
                a = register_contact()
            elif option == '4':
                a = encrypt_message()
            elif option == '5':
                a = decrypt_message()
            elif option == '6':
                a = change_padding()
            elif option == '7':
                a = exit_program()
            else:
                a = "Invalid option"
        except Exception as e:
            a = str(e)