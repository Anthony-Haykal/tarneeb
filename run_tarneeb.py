
import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), 'tarneeb'))

try:
  
    from tarneeb.main import main
    main()
except ImportError as e:
    print(f"Error importing game modules: {e}")
    print("Make sure you have installed the required packages:")
    print("pip install -r tarneeb/requirements.txt")
except Exception as e:
    print(f"Error running the game: {e}")
    import traceback
    traceback.print_exc()
    
    print("\nPress Enter to exit...")
    input() 