# =========================================================
# CECS218 RETAIL MANAGEMENT SYSTEM
# REEM SARHAN AND MALAK YAMANI
# =========================================================
from datetime import datetime

# =========================================================
# CUSTOM EXCEPTIONS
# =========================================================
class InvalidProductError(Exception):
    pass

class InvalidQuantityError(Exception):
    pass

class InvalidMembershipError(Exception):
    pass

class InvalidMemberTypeError(Exception):
    pass

class InvalidRateError(Exception):
    pass

class InvalidFileFormatError(Exception):
    pass

class InvalidNameError(Exception):
    pass

# =========================================================
# CUSTOMER CLASS
# =========================================================
class Customer:

    def __init__(self, customer_id, name, value=0):
        
        self.id = customer_id
        self.name = name
        self.value = float(value)
    
    # No discount for normal customer
    def get_discount(self, price):

        return 0, price

    def display_info(self):

        print(f"ID: {self.id}")
        print(f"Name: {self.name}")
        print(f"Value: {self.value}")
        print("Type: Customer")
        print("---------------------------")
    
    # Getters
    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

# =========================================================
# MEMBER CLASS
# =========================================================
class Member(Customer):

    discount_rate = 0.05

    def __init__(self, customer_id, name, value=0):

        super().__init__(customer_id, name, value)

    def get_discount(self, price):
        
        final_price = price - (price * Member.discount_rate)

        return Member.discount_rate, final_price
    
    # Update discount rate for all members
    @classmethod
    def set_rate(cls, rate):

        cls.discount_rate = rate

    def display_info(self):

        print(f"ID: {self.id}")
        print(f"Name: {self.name}")
        print("Type: Member")
        print(f"Discount Rate: {Member.discount_rate * 100}%")
        print(f"Value: {self.value}")
        print("---------------------------")

# =========================================================
# VIP MEMBER CLASS
# =========================================================
class VIPMember(Customer):

    threshold = 1000

    def __init__(self, customer_id, name, value=0, rate1=0.10):

        super().__init__(customer_id, name, value)

        self.rate1 = rate1
        self.rate2 = rate1 + 0.05

    def get_discount(self, price):

        if price <= VIPMember.threshold:

            rate = self.rate1

        else:

            rate = self.rate2

        final_price = price - (price * rate)

        return rate, final_price

    def set_rate(self, new_rate):

        self.rate1 = new_rate
        self.rate2 = new_rate + 0.05
    
    # Update threshold value for all VIP members
    @classmethod
    def set_threshold(cls, threshold):

        cls.threshold = threshold

    def display_info(self):

        print(f"ID: {self.id}")
        print(f"Name: {self.name}")
        print("Type: VIP Member")
        print(f"Rate1: {self.rate1 * 100}%")
        print(f"Rate2: {self.rate2 * 100}%")
        print(f"Threshold: {VIPMember.threshold}")
        print(f"Value: {self.value}")
        print("---------------------------")

# =========================================================
# PRODUCT CLASS
# =========================================================
class Product:

    def __init__(self, product_id, name, price, stock):

        self.id = product_id
        self.name = name
        self.price = float(price)
        self.stock = int(stock)

    def display_info(self):

        print(f"ID: {self.id}")
        print(f"Name: {self.name}")
        print(f"Price: {self.price}")
        print(f"Stock: {self.stock}")
        print("---------------------------")

# =========================================================
# BUNDLE CLASS
# =========================================================
class Bundle(Product):

    def __init__(self, bundle_id, name, components, stock):

        self.components = components

        total_price = 0

        for product in components:

            total_price += product.price
        
        # Bundles are sold at 80% of the total
        # price of all component products
        bundle_price = total_price * 0.8

        super().__init__(bundle_id, name, bundle_price,stock)

    def display_info(self):

        component_ids = []

        for product in self.components:

            component_ids.append(product.id)

        print(f"ID: {self.id}")
        print(f"Name: {self.name}")
        print(f"Components: {component_ids}")
        print(f"Bundle Price: {self.price}")
        print(f"Stock: {self.stock}")
        print("---------------------------")

# =========================================================
# ORDER CLASS
# =========================================================
class Order:

    def __init__(self, customer, product, quantity, vip_fee=0):

        self.customer = customer
        self.product = product
        self.quantity = quantity
        self.vip_fee = vip_fee
        self.date = datetime.now()

    # Process order by applying discount,
    # updating stock, and customer spending
    def process_order(self):

        total_price = self.product.price * self.quantity

        discount_rate, final_price = self.customer.get_discount(total_price)

        final_price = final_price + self.vip_fee

        # Reduce stock after successful purchace
        self.product.stock -= self.quantity

        self.customer.value += final_price

        return discount_rate, final_price
    
    # DISPLAY RECEIPT
    def display_receipt(self):

        discount_rate, final_price = self.process_order()

        print("------------------------------------------")

        print(f"{self.customer.name} purchases {self.quantity} x {self.product.name}.")

        print(f"Unit price: {self.product.price} (SAR)")

        # VIP membership price
        if self.vip_fee > 0:

            print(f"Membership price: {self.vip_fee} (SAR)")

        print(f"{self.customer.name} gets a discount of {discount_rate * 100} %.")

        print(f"Total price: {final_price} (SAR)")

        print("------------------------------------------")

# =========================================================
# RECORDS CLASS
# =========================================================
class Records:

    def __init__(self):

        self.customers = []
        self.products = []
        self.orders = []

    # Generate unique customer number
    # for new customers
    def generate_customer_number(self):

        used_numbers = []

        for customer in self.customers:

            # Remove first letter
            number = int(customer.id[1:])

            used_numbers.append(number)

        # Start searching from 1
        new_number = 1

        while new_number in used_numbers:

            new_number += 1

        return new_number

    # Read customers from customers.txt
    # and validate IDs, names, and values
    def read_customers(self):

        try:

            file = open("customers.txt", "r")

        except FileNotFoundError:

            raise FileNotFoundError("customers.txt file is missing!")

        used_ids = []
        used_names = []

        for line in file:

            try:

                line = line.strip()

                if line == "":
                    continue

                data = line.split(",")

                if len(data) != 4:

                    raise InvalidFileFormatError("Customer line must contain 4 values")

                customer_id = data[0].strip()
                name = data[1].strip()

                rate = float(data[2])
                value = float(data[3])

                # =========================================
                # VALIDATE NAME
                # =========================================
                if any(char.isdigit() for char in name):

                    raise InvalidNameError("Customer name cannot contain digits")

                if name.lower() in used_names:

                    raise InvalidNameError(f"Duplicate customer name: {name}")

                used_names.append(name.lower())

                # =========================================
                # VALIDATE IDS
                # =========================================
                if customer_id in used_ids:

                    raise InvalidFileFormatError(f"Duplicate customer ID: {customer_id}")

                used_ids.append(customer_id)

                # =========================================
                # VALIDATE VALUES
                # =========================================
                if rate < 0:

                    raise InvalidRateError("Rate cannot be negative")

                if rate > 1:

                    raise InvalidRateError("Rate cannot exceed 1")

                if value < 0:

                    raise InvalidFileFormatError("Customer value cannot be negative")

                # Create customer
                if customer_id.startswith("C"):

                    customer = Customer(
                        customer_id,
                        name,
                        value
                    )

                elif customer_id.startswith("M"):

                    Member.discount_rate = rate

                    customer = Member(
                        customer_id,
                        name,
                        value
                    )

                elif customer_id.startswith("V"):

                    customer = VIPMember(
                        customer_id,
                        name,
                        value,
                        rate
                    )

                else:

                    raise InvalidFileFormatError(f"Invalid customer ID: {customer_id}")

                self.customers.append(customer)

            except ValueError:

                print("Invalid numeric value in customer line:")
                print(line)

            except Exception as e:

                print("Error in customer line:")
                print(line)

                raise

        file.close()

    # Read products and bundles from products.txt
    # and validate prices, stock, and IDs
    def read_products(self):

        try:

            file = open("products.txt", "r")

        except FileNotFoundError:

            raise FileNotFoundError("products.txt file is missing!")

        used_ids = []
        used_names = []

        for line in file:

            try:

                line = line.strip()

                if line == "":
                    continue

                data = line.split(",")

                product_id = data[0].strip()
                name = data[1].strip()

                # =========================================
                # VALIDATE NAME
                # =========================================
                if any(char.isdigit() for char in name):

                    raise InvalidNameError("Product name cannot contain digits")

                if name.lower() in used_names:

                    raise InvalidNameError(f"Duplicate product name: {name}")

                used_names.append(name.lower())

                # =========================================
                # VALIDATE IDS
                # =========================================
                if product_id in used_ids:

                    raise InvalidFileFormatError(f"Duplicate product ID: {product_id}")

                used_ids.append(product_id)

                # Normal product
                if product_id.startswith("P"):

                    if len(data) != 4:
                        
                        raise InvalidFileFormatError("Product line must contain 4 values")

                    price = float(data[2])
                    stock = int(data[3])

                    if price < 0:

                        raise InvalidProductError("Price cannot be negative")

                    if stock < 0:

                        raise InvalidQuantityError("Stock cannot be negative")

                    product = Product(
                        product_id,
                        name,
                        price,
                        stock
                    )

                    self.products.append(product)

                # BUNDLE
                elif product_id.startswith("B"):

                    if len(data) < 5:

                        raise InvalidFileFormatError("Invalid bundle format")

                    stock = int(data[-1])

                    if stock < 0:

                        raise InvalidQuantityError("Stock cannot be negative")

                    component_ids = data[2:-1]

                    components = []

                    for component_id in component_ids:
                        
                        component_id = component_id.strip()

                        product = self.find_product(component_id)

                        if product is None:

                            raise InvalidProductError(f"Bundle product {component_id} not found")

                        components.append(product)

                    bundle = Bundle(
                        product_id,
                        name,
                        components,
                        stock
                    )

                    self.products.append(bundle)

                else:

                    raise InvalidFileFormatError(f"Invalid product ID: {product_id}")

            except ValueError:

                print("Invalid numeric value in product line:")

                print(line)

            except Exception as e:

                print("Error in product line:")
                print(line)

                raise

        file.close()

    # load previous orders from orders.txt
    def read_orders(self):
            
            try:
                
                file = open("orders.txt", "r")
            
            except Exception:
                print("Cannot load the order file. Run as if there is no order previously.")
                return

            try:
                
                for line in file:

                    try:
                        
                        line = line.strip()
                    
                        if line == "":
                            continue
                    
                        data = [item.strip() for item in line.split(",")]

                        if len(data) != 4:
                        
                            raise InvalidFileFormatError("Order line must contain 4 values")

                        customer_search = data[0]
                        product_search = data[1]
                        quantity = int(data[2])

                        date = datetime.strptime(
                            data[3],
                            "%d/%m/%Y %H:%M:%S"
                        )

                        # Find customer
                        customer = self.find_customer(customer_search)

                        if customer is None:
                            raise InvalidProductError(f"Customer not found: {customer_search}")

                        # FIND PRODUCT
                        product = self.find_product(product_search)

                        if product is None:
                        
                            raise InvalidProductError(f"Product not found: {product_search}")

                        # =========================================
                        # VALIDATE QUANTITY
                        # =========================================
                        if quantity <= 0:
                        
                            raise InvalidQuantityError("Quantity must be positive")
                    
                        # Create order
                        order = Order(
                            customer,
                            product,
                            quantity
                        )

                        order.date = date

                        self.orders.append(order)

                    except ValueError:
                    
                        print("Invalid numeric/date value in order line:")
                        print(line)

                    except Exception as e:

                        print("Error in order line:")
                        print(line)
                        print(e)

            except Exception:

                print("Cannot load the order file. Run as if there is no order previously.")

                self.orders = []

            finally:

                file.close()

    # Search customer by ID or name
    def find_customer(self, search):

        for customer in self.customers:

            if customer.id.lower() == search.lower() or customer.name.lower() == search.lower():

                return customer

        return None

    # Search product or bundle by ID or name
    def find_product(self, search):

        for product in self.products:

            if product.id.lower() == search.lower() or product.name.lower() == search.lower():

                return product

        return None

    # DISPLAY CUSTOMERS
    def list_customers(self):

        print("\n========== CUSTOMERS ==========")

        for customer in self.customers:

            customer.display_info()

    # DISPLAY PRODUCTS
    def list_products(self):

        print("\n========== PRODUCTS ==========")

        for product in self.products:

            product.display_info()

    # DISPLAY ALL ORDERS
    def list_orders(self):

        print("\n========== ORDERS ==========")

        for order in self.orders:

            print(
                f"{order.customer.name}, "
                f"{order.product.name}, "
                f"{order.quantity}, "
                f"{order.date}"
            )

    # DISPLAY CUSTOMER ORDERS
    def list_customer_orders(self, search):

        found = False

        for order in self.orders:

            if order.customer.id == search or order.customer.name == search:

                print(
                    f"{order.customer.name}, "
                    f"{order.product.name}, "
                    f"{order.quantity}, "
                    f"{order.date}"
                )

                found = True

        if not found:

            print("Invalid customer!")

# =========================================================
# OPERATIONS CLASS
# =========================================================
class Operations:

    def __init__(self):

        self.records = Records()

    def start(self):

        try:

            self.records.read_customers()
            self.records.read_products()
            self.records.read_orders()

        
        except Exception as e:

            print(e)
            print("Program cannot continue!")

            return

        print("\nWelcome to the RMIT retail management system!")

        # =====================================================
        # MAIN MENU LOOP
        # ===================================================== 
        while True:

            print("\n========== MENU ==========")

            print("1. Place an Order")

            print("2. Display Customers")

            print("3. Display Products")

            print("4. Display Orders")

            print("5. Adjust VIP Rates")

            print("6. Adjust VIP Threshold")

            print("7. Adjust Product Price")

            print("8. Display Customer Orders")

            print("9. Exit")

            print("==========================")

            choice = input("Choose option: ")

            if choice == "1":

                try:

                    self.place_order()

                except Exception as e:

                    print("Order Error:")
                    print(e)

            elif choice == "2":

                self.records.list_customers()

            elif choice == "3":

                self.records.list_products()

            elif choice == "4":

                self.records.list_orders()

            elif choice == "5":

                self.adjust_vip_rate()

            elif choice == "6":

                self.adjust_threshold()

            elif choice == "7":

                self.adjust_product_price()

            elif choice == "8":

                search = input("Enter customer name or ID: ")

                self.records.list_customer_orders(search)

            elif choice == "9":

                print("Program Ended.")
                break

            else:

                print("Invalid option!")

    # =====================================================
    # PLACE ORDER
    # =====================================================
    def place_order(self):

        vip_fee = 0

        # CUSTOMER
        customer_name = input("Enter customer name or ID: ").strip()

        if customer_name.upper().startswith(("C", "M", "V")):

            customer = self.records.find_customer(customer_name)

            if customer is None:

                print("Customer ID does not exist!")
                return

        else:

            if any(char.isdigit() for char in customer_name):

                print("Invalid name! Name cannot contain digits.")
                return

            customer = self.records.find_customer(customer_name)

        # NEW CUSTOMER
        if customer is None:

            answer = input("Become a member? (y/n): ").lower()

            if answer not in ["y", "n"]:

                print("Answer must be y or n")
                return

            if answer == "y":

                member_type = input("Enter membership type (M/V): ").upper()

                if member_type not in ["M", "V"]:

                    print("Must enter M or V")
                    return

                number = self.records.generate_customer_number()

                if member_type == "M":

                    new_id = f"M{number}"

                    customer = Member(
                        new_id,
                        customer_name
                    )

                else:

                    new_id = f"V{number}"

                    customer = VIPMember(
                        new_id,
                        customer_name
                    )

                    vip_fee = 200

                    print("VIP Membership Fee: 200 SAR")

                    customer.value += 200

            else:

                number = self.records.generate_customer_number()

                new_id = f"C{number}"

                customer = Customer(
                    new_id,
                    customer_name
                )

            self.records.customers.append(customer)

        # PRODUCT
        product_name = input("Enter product name or ID: ").strip()

        product = self.records.find_product(product_name)

        if product is None:

            print("Product does not exist!")
            return

        # QUANTITY
        try:

            quantity = int(input("Enter quantity: "))

        except ValueError:

            print("Quantity must be integer")
            return

        if quantity <= 0:

            print("Quantity must be positive")
            return

        if quantity > product.stock:

            print("Not enough stock")
            return

        # Create order object after validating
        # customer, product, and quantity
        order = Order(
            customer,
            product,
            quantity,
            vip_fee
        )

        self.records.orders.append(order)

        order.display_receipt()
    
    # =====================================================
    # ADJUST VIP RATE
    # =====================================================
    def adjust_vip_rate(self):

        search = input("Enter VIP member name or ID: ")

        customer = self.records.find_customer(search)

        if customer is None or not isinstance(customer, VIPMember):

            print("Invalid VIP customer!")
            return

        while True:

            try:

                new_rate = float(input("Enter new first rate: "))

                if new_rate < 0:

                    raise InvalidRateError("Rate cannot be negative")

                if new_rate > 1:

                    raise InvalidRateError("Rate cannot exceed 1")

                customer.set_rate(new_rate)

                print("VIP rates updated!")

                break

            except Exception as e:

                print(e)

    # =====================================================
    # ADJUST THRESHOLD
    # =====================================================
    def adjust_threshold(self):

        while True:

            try:

                threshold = float(input("Enter new threshold: "))

                if threshold <= 0:

                    raise InvalidRateError("Threshold must be positive")

                VIPMember.set_threshold(threshold)

                print("Threshold updated!")

                break

            except Exception as e:

                print(e)

    # =====================================================
    # ADJUST PRODUCT PRICE
    # =====================================================
    def adjust_product_price(self):

        search = input("Enter product name or ID: ").strip()

        product = self.records.find_product(search)
        
        # PRODUCT NOT FOUND
        if product is None:

            print("Product not found!")
            return
        
        # ENTER NEW PRICE
        while True:

            try:

                new_price = float(input("Enter new product price: "))

                if new_price <= 0:

                    raise InvalidProductError("Price must be positive")

                product.price = new_price

                print("Product price updated!")

                break

            except Exception as e:
                print(e)

# =========================================================
# MAIN PROGRAM
# =========================================================
program = Operations()

program.start()