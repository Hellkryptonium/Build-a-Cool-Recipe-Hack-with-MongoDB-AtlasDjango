try:
    import django
    print(f"Django is installed, version: {django.__version__}")
except ImportError:
    print("Django is not installed")

try:
    import voyageai
    print(f"VoyageAI is installed")
    print("Available attributes:", [attr for attr in dir(voyageai) if not attr.startswith('__')])
except ImportError:
    print("VoyageAI is not installed")

try:
    import google.generativeai
    print(f"Google Generative AI is installed")
except ImportError:
    print("Google Generative AI is not installed")

try:
    import pymongo
    print(f"PyMongo is installed")
except ImportError:
    print("PyMongo is not installed")

try:
    import djongo
    print(f"Djongo is installed")
except ImportError:
    print("Djongo is not installed")
