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
