from ids_dashboard import create_app

app = create_app()

if __name__ == "__main__":
    # Local-only by default. Do not expose this development server to the public internet.
    app.run(host="127.0.0.1", port=5000, debug=False)
