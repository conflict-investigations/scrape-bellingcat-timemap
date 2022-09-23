### Scraping Bellingcat's timemap instance

Scrape [ukraine.bellingcat.com](https://ukraine.bellingcat.com/) JSON endpoints
and pull them together into a single coherent export file.

The [timemap](https://github.com/bellingcat/ukraine-timemap/) instance of
Bellingcat provides an "Export to JSON" button, but that is implemented on the
client side, scraping three separate endpoints and generating a file on-the-fly.

- https://ukraine.bellingcat.com/ukraine-server/api/ukraine/export_events/deeprows
- https://ukraine.bellingcat.com/ukraine-server/api/ukraine/export_sources/deepids
- https://ukraine.bellingcat.com/ukraine-server/api/ukraine/export_associations/deeprows

We can, however, reverse-engineer the generation of the JSON file:
[DownloadButton.js](https://github.com/bellingcat/ukraine-timemap/blob/590cb66a2b069fc3041662404bb0e34c896501a7/src/components/controls/DownloadButton.js#L37-L63),

This little script creates the same output as clicking on the "Export to JSON"
button would do.

### Usage

Run `python scrape.py > ukr-civharm-2022-XX-XX.json`.
