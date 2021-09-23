# Jetbrains Plugin Mirror
This product is used to download wanted JetBrains plugins
to a local directory.

The downloaded plugins may be copied to a standalone host
or to offline networks or networks without access to
the JetBrains Markedplace.

Install the mirrored plugins manually in the desired JetBrains product.

## JetBrains Plugins Repository API
The API used to download plugin files and metadata are
documented here:<br>
https://plugins.jetbrains.com/docs/marketplace/api-reference.html

The API returns XML data for metadata about plugins, like
the name, pluginXmlId and versions.

This information + information about JetBrains product are
needed to download a plugin.

The JetBrains product list is here:<br>
https://plugins.jetbrains.com/docs/marketplace/product-codes.html

### Examples using the API
To list or download a plugin, you need the product code and the build version
number for the product you want to download for.

This information can easily be obtained by pressing Help->About for the relevant product.
For CLion 2021.2.2 this build info is printed:
```
Build #CL-212.5284.51, built on September 16, 2021
```

The product code is 'CL' and the build number is '212.5284.51'.

#### List all plugins compatible with product
Required info:
* ProductCode
* BuildNumber

https://plugins.jetbrains.com/plugins/list/?build=CL-212.5284.51

Returns:
* XML data containing information about plugin name, pluginXmlId, version, category and
description for each plugin.

#### Get information about one plugin
Required info:
* PluginID (number)
* PluginXmlId

When browsing the [markedplace](https://markedplace.jetbrains.com) and looking
on the details of a plugin, you see that the URL contains a number in addition to the
name of the plugin. Example URL for the Markdown plugin:<br>
https://plugins.jetbrains.com/plugin/7793-markdown/

Here the pluginID is '7793'. This cab be used to get XML dta about this plugin:<br>
https://plugins.jetbrains.com/plugins/list?pluginId=7793

But this tool downloa plugins from a list file, and it is easier for the user to have a
list of pluginXmlId instead of numeric values. The return XML for the link above contains this info:
``` XML
<name>Markdown</name>
<id>org.intellij.plugins.markdown</id>
```

This 'id' tag here is the pluginXmlId. The same plugin xml data can be downloaded using this 'id':<br>
https://plugins.jetbrains.com/plugins/list?pluginId=org.intellij.plugins.markdown

How can you obtain this pluginXmlID from the markedplace web page?<br>
Go to the plugin Version page in the markedplace. Click on the latest version and on the new
web-page the 'id' should be presented. Example for the Markdown plugin version 212.5080.22:<br>
https://plugins.jetbrains.com/plugin/7793-markdown/versions/stable/132494

Returns:
* XML metadata for this plugin. Containing among oth things: name, pluginXmlID, description, categories and all versions.

### Download latest plugin compatible with product and build number
This URL will download latest version of a plugin that is compatible with the product and build version:<br>
https://plugins.jetbrains.com/pluginManager?action=download&id=org.intellij.plugins.markdown&build=CL-212.5284.51

Can also download a given version of a plugin:
https://plugins.jetbrains.com/plugin/download?pluginId=org.intellij.plugins.markdown&version=212.5080.22

When downloading this URL from a web browser a download file dialogue pops up with a default name like
'<pluginName-Version.zip'. When downloading this with wget the file is downloaded with the directory part of
the URL as filename. Possible som scripting on the web-server to present as a file download for ordinary web-browsers.

Download with curl:
```
curl -vL "https://plugins.jetbrains.com/pluginManager?action=download&id=org.intellij.plugins.markdown&build=CL-212.5284.51"

< HTTP/2 301
< content-length: 0
< date: Thu, 23 Sep 2021 10:26:41 GMT
< set-cookie: AWSALB=eB4jowjeQfcy6XL1iOI/CnnD+MPlczmA8gKDbUFFsCRh3NPeESH+UyJEouo2tmyukxNld56lSNsEcRBgsZD6DXjOT2wiOCdTP8H4p/7KYXwFdJEA37GqbRMiRGDO; Expires=Thu, 30 Sep 2021 10:26:41 GMT; Path=/
< set-cookie: AWSALBCORS=eB4jowjeQfcy6XL1iOI/CnnD+MPlczmA8gKDbUFFsCRh3NPeESH+UyJEouo2tmyukxNld56lSNsEcRBgsZD6DXjOT2wiOCdTP8H4p/7KYXwFdJEA37GqbRMiRGDO; Expires=Thu, 30 Sep 2021 10:26:41 GMT; Path=/; SameSite=None; Secure
< location: /files/7793/132494/markdown-212.5080.22.zip?updateId=132494&pluginId=7793&family=INTELLIJ&code=CL&build=212.5284.51
< x-content-type-options: nosniff
< x-xss-protection: 1; mode=block
< cache-control: no-cache, no-store, max-age=0, must-revalidate
< pragma: no-cache
< expires: 0
< strict-transport-security: max-age=31536000 ; includeSubDomains
< x-frame-options: SAMEORIGIN
< content-security-policy: connect-src 'self' localhost:* http://localhost:* *.jetbrains.com www.google-analytics.com *.hotjar.com wss://*.hotjar.com app-lon02.marketo.com bam.nr-data.net bam-cell.nr-data.net hub.jetbrains.com youtrack.jetbrains.com; default-src 'self'; script-src 'self' 'unsafe-eval' 'unsafe-inline' tagmanager.google.com www.googletagmanager.com www.google-analytics.com static.hotjar.com script.hotjar.com js-agent.newrelic.com bam.nr-data.net bam-cell.nr-data.net resources.jetbrains.com www.youtube.com; font-src data: 'self' *.jetbrains.com themes.googleusercontent.com fonts.gstatic.com static.hotjar.com; img-src 'unsafe-inline' data: *; style-src 'unsafe-inline' 'self' *.jetbrains.com cloud.typography.com tagmanager.google.com fonts.googleapis.com; frame-src 'self' www.googletagmanager.com vars.hotjar.com www.youtube.com hub.jetbrains.com youtrack.jetbrains.com;
< content-language: en
< x-edge-origin-shield-skipped: 0
< x-cache: Miss from cloudfront
< via: 1.1 f66e3db0f0449307dba3fbf72bbf3bac.cloudfront.net (CloudFront)
< x-amz-cf-pop: OSL50-C1
< x-amz-cf-id: fwIOGDLhR5hFjDKHynBrifNoZRqgB0JdhY2kTz55Q5or3ZqyNNa0bQ==
<
* Connection #0 to host plugins.jetbrains.com left intact
* Issue another request to this URL: 'https://plugins.jetbrains.com/files/7793/132494/markdown-212.5080.22.zip?updateId=132494&pluginId=7793&family=INTELLIJ&code=CL&build=212.5284.51'
* Found bundle for host plugins.jetbrains.com: 0x55a444de8c30 [can multiplex]
* Re-using existing connection! (#0) with host plugins.jetbrains.com
* Connected to plugins.jetbrains.com (143.204.54.37) port 443 (#0)
* Using Stream ID: 3 (easy handle 0x55a444df0b60)
> GET /files/7793/132494/markdown-212.5080.22.zip?updateId=132494&pluginId=7793&family=INTELLIJ&code=CL&build=212.5284.51 HTTP/2
> Host: plugins.jetbrains.com
> user-agent: curl/7.76.1
> accept: */*
>
< HTTP/2 200
< content-type: application/zip
< content-length: 1323839
< x-amz-replication-status: COMPLETED
< last-modified: Fri, 13 Aug 2021 08:54:24 GMT
< content-disposition: attachment; filename="markdown-212.5080.22.zip"
< x-amz-version-id: DHVQZU5e3Zl.TwrNSIkd7st_umjCaCfm
< accept-ranges: bytes
< server: AmazonS3
< x-edge-origin-shield-skipped: 0
< date: Thu, 23 Sep 2021 07:39:53 GMT
< etag: "3717a45fbd9f780bd5d10704138abadd"
< x-cache: Hit from cloudfront
< via: 1.1 f66e3db0f0449307dba3fbf72bbf3bac.cloudfront.net (CloudFront)
< x-amz-cf-pop: OSL50-C1
< x-amz-cf-id: ITRdjUCz55Oq7TH-N7dMpD7Ticcooc37YUGEDsOLHcba8WqaZkYaiA==
< age: 10009
```

The HTTP 3 code means that the resource has moved permanently and the response contains the filename, length of file
and content-type with the new url to download the file from.

The 'location:' tag gives the new URL that the resource has been moved to.
```
< location: /files/7793/132494/markdown-212.5080.22.zip?updateId=132494&pluginId=7793&family=INTELLIJ&code=CL&build=212.5284.51
```

Filename in clear text:
```
< content-disposition: attachment; filename="markdown-212.5080.22.zip"
```

File type and size:
```
< content-type: application/zip
< content-length: 1323839
```

```
URL="https://plugins.jetbrains.com/pluginManager?action=download&id=org.intellij.plugins.markdown&build=CL-212.5284.51"
LOC=$(wget --no-verbose --method=HEAD --output-file - $URL)
echo $LOC
2021-09-23 12:39:03 URL: https://plugins.jetbrains.com/files/7793/132494/markdown-212.5080.22.zip?updateId=132494&pluginId=7793&family=INTELLIJ&code=CL&build=212.5284.51 200 OK

```


# Implementation
The mirroring is implemented in python using 'request' to download
metadata information and 'lxml' to parse the xml.