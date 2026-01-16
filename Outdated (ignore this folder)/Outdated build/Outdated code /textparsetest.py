# import textwrap
# import os

# def parse_to_screen(text):
#     try:
#         # Get the number of columns in the current terminal window
#         columns = os.get_terminal_size().columns
#     except OSError:
#         # Fallback to a standard width (e.g., 80) if not running in a terminal
#         columns = 80

#     # wrap() returns a list of lines, fill() returns a single string with \n
#     formatted_text = textwrap.fill(text, width=columns)
    
#     print(formatted_text)

# # Example usage:
long_text = "This is a very long string that might normally get cut off by the edge of your screen if you don't wrap it properly. By using the textwrap module, we ensure that the logic respects word boundaries."
# parse_to_screen(long_text)
