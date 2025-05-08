import asyncio
from aiohttp import web
import os
from pathlib import Path

#Set up paths for all required files 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
DB_FILE = os.path.join(BASE_DIR, 'db.txt')

async def serve_html(filename, status=200):
    #serve HTML files from templates folder
    filepath = os.path.join(TEMPLATES_DIR, filename)
    if not os.path.exists(filepath):
        return web.Response(status=404, text="404: File Not Found")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return web.Response(text=content, content_type='text/html', status=status)

async def handle_registration(request):
    
    data = await request.post()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()

    if not username or not email:
        return web.Response(
            text="Error: Both username and email are required", status=400)

    # Ensure directory exists
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    
    # Write to database file
    try:
        with open(DB_FILE, 'a', encoding='utf-8') as db:
            db.write(f"{username}  {email}\n")
        
        # Return success response
        return web.Response(text="Registration successful!", content_type='text/html' '<a href="/">Return Home</a>')
        
    except IOError as e:
        return web.Response(
            text=f"Error saving data: {str(e)}",
            status=500
        )

async def handle_request(request):
    #Main request handler
    if request.method == 'GET':
        if request.path == '/':
            return await serve_html('index.html')
        elif request.path == '/index.html':
            return await serve_html('index.html')
        elif request.path == '/register.html':
            return await serve_html('register.html')
        else:
            return web.Response(status=404, text="404: Not Found")
    
    elif request.method == 'POST' and (request.path == '/register.html' or request.path == '/submit.html'):
        return await handle_registration(request)
    
    else:
        return web.Response(status=405, text="405: Method Not Allowed")

async def init_app():
    # Ensure templates directory exists
    os.makedirs(TEMPLATES_DIR, exist_ok=True)

    #Initializing the application
    app = web.Application()
    app.router.add_get('/', handle_request)
    app.router.add_get('/index.html', handle_request)
    app.router.add_get('/register.html', handle_request)
    #app.router.add_post('/register', handle_request)
    app.router.add_post('/submit.html', handle_request)
    return app

def main():
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        app = loop.run_until_complete(init_app())

        print("------ Server is up and Running -------") 
        web.run_app(app, host='localhost', port=8085)
    except KeyboardInterrupt:
        print("\nServer stopped gracefully")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        loop.close()

if __name__ == '__main__':
    main()