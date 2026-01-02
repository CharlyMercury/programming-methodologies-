

def say_hello(name):
    """
    Function to greet a person with their name.
    
    Parameters:
    name (str): The name of the person to greet.
    
    Returns:
    str: A greeting message.
    """
    return f"Hello, {name}!"


response_1 = say_hello("Alice")
response_2 = say_hello("Bob")
print(type(response_1))  # Output: Hello, Alice!
print(type(response_2))  # Output: Hello, Bob!


### Positional Parameters ###
def add_numbers(number_a, number_b=0):
    """
    Function to add two numbers.
        
        Parameters:
            a (int): The first number.
            b (int): The second number.
        
        Returns:
            int: The sum of the two numbers.
    """
    return number_a+ number_b

# Positional arguments
print(add_numbers(5, 10)) # Output: 15
print(add_numbers(3, 7))  # Output: 10
# Keyword arguments
print(add_numbers(number_a=5, number_b=10)) # Output: 15
print(add_numbers(number_b=5, number_a=10)) # Output: 15
# Optional argument
print(add_numbers(number_a=5))
print(add_numbers(5)) # Output: 5
# Args and Kwargs