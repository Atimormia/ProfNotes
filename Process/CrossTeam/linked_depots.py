import sys
import subprocess

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_dependencies():
    try:
        import P4
    except ImportError:
        return False
    return True

def main():
    if not check_dependencies():
        print("Some dependencies are missing. Installing...")
        try:
            install("P4")
            print("Dependencies installed successfully.")
        except Exception as e:
            print(f"Failed to install dependencies: {e}")
            sys.exit(1)

    from P4 import P4, P4Exception

    if len(sys.argv) < 2:
        print("Usage: python linked_depots.py <searching_depot>")
        sys.exit(1)
    
    searching_depot = sys.argv[1]
    p4 = P4()
    
    try:
        p4.connect()
        print("Connected to Perforce server")

        streams = p4.run('streams')
        linked_depots = []

        for stream in streams:
            stream_name = stream['Stream']
            stream_data = p4.run('stream', '-o', stream_name)
            paths = stream_data[0].get('Paths', [])
            for path in paths:
                if searching_depot in path:
                    clean_path = path.split('##')[0].strip()
                    parts = clean_path.split('//')
                    if len(parts) > 1:
                        linking_way = parts[0].strip().split()[0]
                        linked_depot = '//' + parts[1].strip()
                        linked_depots.append((stream_name, linked_depot, linking_way))
                    break

        if linked_depots:
            print("Depots linked to the current depot:")
            print("{:<60} {:<60} {}".format("Stream", "Linked Depot", "Linking Way"))
            for stream, linked_depot, linking_way in linked_depots:
                print("{:<60} {:<60} {}".format(stream, linked_depot, linking_way))
        else:
            print("No depots linked to the current depot.")

    except P4Exception as e:
        for error in e.errors:
            print(error)
    finally:
        p4.disconnect()
        print("Disconnected from Perforce server")

if __name__ == "__main__":
    main()
