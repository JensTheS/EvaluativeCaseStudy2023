import requests
import time


def format_response(response):
    """
    Formats a given response into a more readable format.

    Args:
        response (Any): The response to be formatted.

    Returns:
        str: The formatted response.
    """
    if isinstance(response, str):
        return response
    elif isinstance(response, (list, tuple)):
        formatted_items = [format_response(item) for item in response]
        return "[\n  {}\n]".format(",\n  ".join(formatted_items))
    elif isinstance(response, dict):
        formatted_items = []
        for key, value in response.items():
            if isinstance(value, dict):
                formatted_items.append("{}: {}".format(key, format_response(value)))
            else:
                formatted_items.append("{}: {}".format(key, value))
        return "{\n  {}\n}".format(",\n  ".join(formatted_items))
    else:
        return str(response)


def send_request(prompt, comment, max_tokens, num_return_sequences=10):
    start_time = time.time()

    url = "http://localhost:8000"  # replace with the URL of your server

    data = {
        "prompt": prompt,
        "comment": comment,
        "max_tokens": max_tokens,
        "num_return_sequences": num_return_sequences,
    }
    response = requests.post(url, json=data)
    total_time = time.time() - start_time
    output_dict = {}

    for i in range(num_return_sequences):
        key = str(i + 1)
        output_dict[key] = format_response(response.json()["output"][i])

    return {
        "time": total_time,
        "num_tokens": response.json()["num_tokens"],
        "output": output_dict,
    }


code_challenges = [
    {
        "prompt": "def divide(a, b):",
        "comment": "",
        "max_tokens": 50,
    },
    {"prompt": "def multiply(a, b):", "comment": "", "max_tokens": 50},
    {"prompt": "def subtract(a, b):", "comment": "", "max_tokens": 50},
    {"prompt": "def is_prime(num):", "comment": "", "max_tokens": 100},
    {
        "prompt": "def fibonacci(n):",
        "comment": "# Calculate the nth Fibonacci number.",
        "max_tokens": 100,
    },
    {
        "prompt": "def factorial(n):",
        "comment": "# Calculate the factorial of n.",
        "max_tokens": 100,
    },
    {
        "prompt": "def sum_of_digits(n):",
        "comment": "# Calculate the sum of the digits of n.",
        "max_tokens": 500,
    },
    {
        "prompt": "def merge_sort(lst):",
        "comment": "# Sort the list using the merge sort algorithm.",
        "max_tokens": 500,
    },
    {
        "prompt": "def binary_search(lst, target):",
        "comment": "# Search for the target in the sorted list using binary search.",
        "max_tokens": 500,
    },
    {
        "prompt": "def quicksort(lst):",
        "comment": "# Sort the list using the quicksort algorithm.",
        "max_tokens": 500,
    },
    {
        "prompt": "def bubble_sort(lst):",
        "comment": "# Sort the list using the bubble sort algorithm.",
        "max_tokens": 500,
    },
    {
        "prompt": "def insertion_sort(lst):",
        "comment": "# Sort the list using the insertion sort algorithm.",
        "max_tokens": 500,
    },
]

result_list = []

for challenge in code_challenges:
    prompt = challenge["prompt"]
    comment = challenge["comment"]
    max_tokens = challenge["max_tokens"]

    result_list.append(send_request(prompt, comment, max_tokens, 1))

for result in result_list:
    print(result["time"], result["num_tokens"])

for result in result_list:
    for key, output in result["output"].items():
        print("Sequence {}: {}".format(key, format_response(output)))
