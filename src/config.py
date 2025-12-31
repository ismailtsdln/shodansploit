import os

class Config:
    @staticmethod
    def get_api_key():
        """
        Retrieves the Shodan API key.
        Checks environment variable SHODAN_API_KEY first, then api.txt file.
        Returns None if not found.
        """
        # Check environment variable
        api_key = os.environ.get("SHODAN_API_KEY")
        if api_key:
            return api_key.strip()
            
        # Check api.txt file
        api_file_path = "api.txt"
        if os.path.exists(api_file_path) and os.path.getsize(api_file_path) > 0:
            try:
                with open(api_file_path, 'r') as file:
                    content = file.readline()
                    if content:
                        return content.strip()
            except IOError:
                pass
                
        return None

    @staticmethod
    def save_api_key(api_key):
        """
        Saves the API key to api.txt.
        """
        try:
            with open('api.txt', 'w') as file:
                file.write(api_key)
            return True
        except IOError:
            return False
