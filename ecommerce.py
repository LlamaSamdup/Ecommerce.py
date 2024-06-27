import json

# Asking user to login or register
user_input = input("Do you want to login or register? ").lower()

# login function
def login():
    user_name = input("Enter your username: ")
    user_password = input("Enter your password: ")
    print()

    try:
        with open("users.txt", "r") as file1:
            user_data = file1.read()
    except FileNotFoundError:
        print("No users found. Please register first.")
        return

    # converting userdata to list so a for loop can iterate for the list of items
    list_user_data = user_data.split("\n")
    user_found = False

    for i in list_user_data: 
        if i.strip():  # Ensure we process only non-empty lines
            dict_data = json.loads(i) # Convert json string to dictionary using loads method
            if 'username' in dict_data and 'password' in dict_data:
                if user_name == dict_data['username'] and user_password == dict_data['password']:
                    if dict_data.get('usertype', '') == 'seller': # empty quotation marks is used as default value incase the key usertype is not present in dict_data dictionary
                        user_found = True
                    
                        while True:
                            print('*************************************')
                            print('*****       Login Successful    *****')
                            print('*****        Welcome Seller     *****')
                            print('*************************************')
                            print()
                            print('1. Add Product    2. View Product    3. Logout')
                            print()
                            user_choice = input('Enter your choice: ')
                            if user_choice == '1' and dict_data.get('usertype', '') == 'seller':
                                add_product()
                            elif user_choice == '2':
                                view_product()
                            elif user_choice == '3':
                                print('You have been logged out.')
                                return
                            else:
                                print('Invalid Choice')
                            break # Exit the loop if login is successful
                    
                    elif dict_data.get('usertype', '') == 'buyer':
                            print('*************************************')
                            print('*****       Login Successful    *****')
                            print('*****        Welcome Buyer      *****')
                            print('*************************************')
                            print()
                            print('1. View Product    2. View Bills    3. Logout')
                            print()
                            user_choice = input('Enter your choice: ')
                            if user_choice == '1':
                                buy_product(user_name)
                            elif user_choice == '2':
                                view_bills(user_name)
                            elif user_choice == '3':
                                print('You have been logged out.')
                            else:
                                print('Invalid Choice')
                            return

    if not user_found:
        print("Invalid username or password. Please try again.")

# register function        
def register():
    user_name = input('Enter your username: ')
    user_password = input('Enter your password: ')
    user_type = input("Enter user type (buyer/seller): ").lower() # lower() returns the lowercased strings from the given string by converting each uppercase character to lowercase.

    try:
        with open("users.txt", "r") as file:
            existing_users = file.readlines()
    except FileNotFoundError:
        existing_users = []  # Create an empty list if the file doesn't exist, so that the code can still execute the loop and process the list of exisiting users, even if the file does not exist

    # check if the username with same name already exists in our file users.txt
    for user in existing_users:
        if user.strip():  # Ensure we process only non-empty lines
            dict_data = json.loads(user)
            if 'username' in dict_data:
                if user_name == dict_data['username']:
                    print("Username already exists. Please choose a different username.")
                    return
                
    # creating a dictionary for userdata
    user_data = {
        'username': user_name,
        'password': user_password,
        'usertype': user_type
    }

    json_data = json.dumps(user_data)

    with open('users.txt', 'a') as file:
        file.write(json_data + '\n')

    print('Registration Successful...')

# add product function
def add_product():
    product_name = input('Enter product name: ')
    product_description = input('Enter product description: ')
    product_price = int(input('Enter product price: '))

    # creating a dictionary for productdata
    product_data = {
        'name': product_name,
        'description': product_description,
        'price': product_price
    }

    # converting dictionary to json string
    json_data = json.dumps(product_data)

    with open('products.txt', 'a') as file:
        file.write(json_data + '\n')

    print('Product Added Successfully...')

# view product function
def view_product():
    try:
        with open('products.txt', 'r') as file1:
            products = file1.readlines()
    except FileNotFoundError:
        print("No products found.")
        return

    for product in products:
        if product.strip():  # Ensure we process only non-empty lines
            product_data = json.loads(product)
            print(product_data)

# buy product function
def buy_product(buyer_name):
    try:
        with open('products.txt', 'r') as file:
            products = file.readlines()
    except FileNotFoundError:
        print('No products found.')
        return

    # product_list = [] is created to store all the products read from the products.txt file. 
    # This list allows the program to display the products to the user, let them select a product by its index, 
    # and then access the details of the selected product later in the code.
    product_list = []

    # This loop reads each product, converts it from a JSON string to a dictionary, and appends it to product_list
    for product in products:
        if product.strip():
            product_data = json.loads(product)
            product_list.append(product_data)
            print(f'{len(product_list)}. {product_data}')
    
    product_choice = int(input('Enter the product number you want to purchase: '))
    if 1 <= product_choice <= len(product_list):
        selected_product = product_list[product_choice - 1]
        quanity = int(input('Enter the quantity: '))
        total_price = int(selected_product['price']) * quanity

        # creating a dictionary for billdata
        bill_data = {
            'buyer': buyer_name,
            'product': selected_product['name'],
            'quantity': quanity,
            'total': total_price
        }

        # converting dictionary to json string and writing to file
        json_data = json.dumps(bill_data)
        with open('bills.txt', 'a') as file1:
            file1.write(json_data + '\n')

        print('Product Purchased Successfully...')
        print(f'Bill: {bill_data}')    

    else:
        print ('Invalid product choice.')

# view bills function
def view_bills(buyer_name):
    try:
        with open('bills.txt', 'r') as file:
            bills = file.readlines()

    except FileNotFoundError:
        print('No bills found.')
        return

    # filter bills based on buyer name
    for bill in bills:
        if bill.strip():
            bill_data = json.loads(bill)
            if bill_data['buyer'] == buyer_name:
                print(bill_data)    

if user_input == 'login':
    login()
elif user_input == 'register':
    register()
else:
    print("Invalid input. Please enter 'login' or 'register'.")
