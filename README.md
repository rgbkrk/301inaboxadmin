301 in a box admin
==================

Admin/API for 301inabox

## Quickstart

From your trusty shell:
```bash
# Set up an admin node for 301inabox
docker run -d --name admin -p 8081:8080 rgbkrk/301inaboxadmin
# Run 301inabox, linking it to the admin node
docker run --link admin:admin -p 80:8080 rgbkrk/301inabox
```

Make sure to add some records to the admin node:
```
curl -X POST localhost:8081/api/records \
     -d '{"record":{"hostname":"hackathon.301inabox.tk","url":"http://www.example.org"}}' \
     -H "Content-Type:application/json"
```
