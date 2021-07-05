import scrapy
from ..items import OpenprojectsItem

class OpenForge(scrapy.Spider):

    name = "openforge"
    start_urls = [
        "https://openforge.gov.in/softwaremap/trove_list.php?offset=0&form_cat=106&special_cat=none"
    ]

    def parse(self, response):
        items = OpenprojectsItem()
        software_section = response.css("section#softwaremap-list-results")
        rows = software_section.css("tbody tr")
        separator = "$"
        for row in rows:
            columns = row.css("td")
            project_name = columns[0].css("a::text").extract()
            description =columns[1].css("::text").extract()
            categories = columns[2].css("div.softwaremap-list-results-trovecat a::text").extract()
            creation_date = columns[3].css("::text").extract()
            items["project"] = separator.join(project_name)
            items["description"] = separator.join(description)
            items["categories"] = separator.join(categories)
            items["creation_date"] = separator.join(creation_date)
            yield items

        next_page = response.css("div.tlp-pagination a")[2].css("::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

