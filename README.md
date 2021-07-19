Canny Edge Detector Prototype
===

This is a microservice prototype, which runs the [Canny Edge Detection](https://en.wikipedia.org/wiki/Canny_edge_detector) algorithm on images uploaded to an REST endpoint. This was written in three hours as part of an interview assignment so expect bugs and errors.

## Run

To run this microservice in debug mode, execute `docker-compose up` (or `docker-compose up -d` to run in the background). The default port is `80` and can be adjusted in the `docker-compose.override.yml`.

Use the service with any web request tool like Postman or cUrl.

## Further Improvements

- Setup CI lint
- Use external uWSGI and Nginx
- Provide Helm chart
- Use numpy on the whole arrays instead of just the single values inside for-loops
- Perform the calculations in another thread (using OpenCV would also increase preformance significantly)
- Rearchitect the application
  - Put the image into a queue and return transaction ID instead of the image
  - Provide a different endpoint, which, given the transaction ID, returns the processed image (or an error if its not yet finished)
  - Or build it cloud-native with AWS/Azure Queues and Lamdbas/Cloud Functions

## Examples

### Query (cURL)

```bash
curl --location --request POST 'localhost/detect' \
--form 'file=@"./input.png"' \
--output "output.png"
```

### Result

![results images](.github/images/results.jpg)
