from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb+srv://kesu123:KK%40123@cluster0.qaannsv.mongodb.net/",tlsAllowInvalidCertificates=True)


db=client["ytmanager"]
video_collection=db["videos"]

# print(video_collection)

def add_videos(name,time):
  video_collection.insert_one({"name":name,"time":time})

def list_videos():
  # enumerative hai to loop laga do 
  for video in video_collection.find():
    print(f"ID:{video['_id']},Name:{video['name']}and Time:{video['time']}")

def update_videos(video_id,new_name,new_time):
  video_collection.update_one(
    {'_id':ObjectId(video_id)},
    {"$set":{"name":new_name,"time":new_time}}
  )
def delete_video(video_id):
  video_collection.delete_one({"_id": ObjectId(video_id)})



def main():
  while True:
    print("\n Youtube Manager | choose and option")
    print("1. List all youtube vidoes")
    print("2. Add a youtube vidoes")
    print("3. update a  youtube vidoes details ")
    print("4. Delete a  youtube vidoes")
    print("5. Exit the app ")
    choice= input("enter your choice: ")
 
    if choice =='1':
      list_videos()
    elif choice =='2':
      name=input("Enter the video name:")
      time=input("Enter the video time:")
      add_videos(name,time)

    elif choice =='3':
      video_id=input("Enter the video ID to update:")
      name=input("Enter the video name:")
      time=input("Enter the video time:")
      update_videos(video_id,name,time)
    elif choice=='4':
      video_id=input("Enter the video ID to delete:")
      delete_videos(video_id)

    elif choice =='5':
      break
    else:
      print("Invalid choice ")


if __name__ == "__main__":
   main()


