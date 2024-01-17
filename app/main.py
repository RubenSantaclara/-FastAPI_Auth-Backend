import uvicorn


if __name__ == '__main__':

    # Start server
    uvicorn.run(
        app     = 'server.app:app', 
        host    = '127.0.0.1', 
        port    = 8080, 
        reload  = True
    )