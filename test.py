from characterai import pyCAI
import concurrent.futures
token = '3bacec01844a43fd5e72089cfa8ea2cedb38335b'
character = 'WsqG34NBsbCr3hxN7gJA_y5khYtVQzTD71IqdtfO57Y'




client = pyCAI(token, headless=False)
# Create a thread pool executor
executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
sending = "Hello"
# Submit the function to the executor to be executed in a separate thread
future = executor.submit(client.chat.send_message,character,sending)

while True:
    if future.done():
    	result = future.result()
    	print(result)