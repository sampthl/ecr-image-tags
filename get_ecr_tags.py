import boto3
import re

def get_all_image_tags(client, repository_name):
    images = []
    print(f"Looking for images in {repository_name} ... ")
    response = client.describe_images(
        repositoryName = repository_name,
        filter = {
            'tagStatus': 'TAGGED'
        }
    )
    images += response.get('imageDetails')
    next_token = response.get('nextToken')
    while next_token:
        print(f"Found another page, getting more images for {repository_name} ...")
        response = client.describe_images(
            repositoryName = repository_name,
            nextToken = next_token,
            filter = {
                'tagStatus': 'TAGGED'
            }
        )
        images += response.get('imageDetails')
        next_token = response.get('nextToken')

    return [image.get('imageTags')[0] for image in images]

client = boto3.client('ecr')

tags = get_all_image_tags(client, 'reservations-svc')

newer_tags = list(filter(lambda x: re.search(r"^30", x), tags))

print(newer_tags)
