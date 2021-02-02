# Web-Crawler

This project is for ripping sites, it downloads all html/css/js/imgs and makes zip archive.  

## Getting started

 To run project:
 
```
docker-compose up -d
```
 To run project:
 
```
docker exec -it crawler flask db upgrade
```

### Project URLs
* Add site and create task for downloading site, /api/v1/site:

    * POST http://localhost/api/v1/site
    
        ```
        {
          "url": "https://example.com/"
        }
        ```
    * Response containing site_id by which possible to get status of the downloading site and download zip archive with this site. 
        ```
        {
          "site_id": 1
        }
        ```
* Get status of the downloading site and link for downloading zip archive:
    * GET http://localhost/api/v1/site/<int:site_id>
    * Response:
         ```
        {
            "status": "done",
            "zip_url": "http://localhost/api/v1/site/5/zip"
        }
        ```
* Get zip archive:
    * GET http://localhost/api/v1/site/<int:site_id>/zip
