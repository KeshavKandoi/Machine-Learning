import requests

def fetch_random_user_freeapi():
    url = "https://api.freeapi.app/api/v1/public/randomusers/user/random"
    
    response = requests.get(url)
    data = response.json()

    if data["success"] and "data" in data:
        user = data["data"]

        # Extract values
        gender = user["gender"]
        latitude = user["location"]["coordinates"]["latitude"]
        longitude = user["location"]["coordinates"]["longitude"]
        md5 = user["login"]["md5"]
        sha1 = user["login"]["sha1"]
        sha256 = user["login"]["sha256"]

        return gender, latitude, longitude, md5, sha1, sha256

    else:
        raise Exception("Failed to fetch user data")

def main():
    try:
        gender, lat, lon, md5, sha1, sha256 = fetch_random_user_freeapi()
        
        print(f"Gender: {gender}")
        print(f"Latitude: {lat}")
        print(f"Longitude: {lon}")
        print(f"MD5: {md5}")
        print(f"SHA1: {sha1}")
        print(f"SHA256: {sha256}")

    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    main()
