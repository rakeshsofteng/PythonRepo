# Program to print multiplication tables for entered numbers

def print_table(number, upto=10):
    print("*" * 20)
    print(f"Table for {number}")
    print("*" * 20)
    for i in range(1, upto + 1):
        print(f"{number} x {i} = {number * i}")

def main():
    nums = input("Enter numbers separated by spaces: ")
    numbers = [int(n) for n in nums.split()]
    for num in numbers:
        print(f"\nMultiplication Table for {num}:")
        print_table(num)

if __name__ == "__main__":
    main()