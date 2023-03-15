import uuid


async def upload(bucket, file):
    key = bucket + "/" + str(uuid.uuid4()) + "-" + file.filename
    return key


async def download(bucket, filename):
    return filename
