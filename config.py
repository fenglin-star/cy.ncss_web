import pymongo

client = pymongo.MongoClient('localhost',27017)
mogondb_project = client['大学生创新创业项目']
project = mogondb_project['全国高校_创新创业项目']


end = 17113