import csv
import scrapy
from scrapy.crawler import CrawlerProcess
import os
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

URL = "https://ทองคําราคา.com/"


class MySpider(scrapy.Spider):
    name = "gold_price_spider"
    start_urls = [URL,]

    def parse(self, response):
        header = response.css("#divDaily h3::text").get().strip()
        print(header)

        table = response.css("#divDaily .pdtable")
        # print(table)

        rows = table.css("tr")
        # rows = table.xpath("//tr")
        # print(rows)

        li = []
        
        for row in rows:
            # print(row.css("td::text").extract())
            # print(row.xpath("td//text()").extract())
            data_row = row.css("td::text").extract()
            li.append(data_row)

        # Write to CSV
        # YOUR CODE HERE
        # print(li)
        
        # li[] setup 1st column -> li[0]
        # then use li[1:-1] mean
        # start from row1 (normally row0)
        df = pd.DataFrame(li[1:-1], columns=li[0])
        
        df.info()
        df.to_csv('gold_price_spider.csv', index=None)
        
        # Upload to GCS 
        # YOUR CODE HERE
        
        
        # GCS to Bigquery
        # YOUR CODE HERE
        # def load_data_from_gcs_to_bigquery(gsutil_uri, source_format):
        #     keyfile = os.environ.get("KEYFILE_PATH")
        #     bq_client = bigquery.Client(
        #         credentials=service_account.Credentials.from_service_account_file(
        #             keyfile
        #         ),
        #     )

        #     # table_id  = project_id + dataset_id + table_name
        #     table_id = "cultivated-list-383715.greenery.events"
        #     bq_table = bq_client.get_table(table_id)

        #     job_config = bigquery.LoadJobConfig(
        #         schema=bq_table.schema,
        #         source_format=source_format,
        #         write_disposition="WRITE_TRUNCATE",
        #     )
        #     if ".csv" in gsutil_uri:
        #         job_config.skip_leading_rows = 1

        #     start = time.time()
        #     load_job = bq_client.load_table_from_uri(
        #         gsutil_uri, table_id, job_config=job_config
        #     )
        #     load_job.result()
        #     end = time.time()

        #     destination_table = bq_client.get_table(table_id)
        #     print("Loaded {} rows.".format(destination_table.num_rows))
        #     print("Loaded data in {}".format(end - start))


        # if __name__ == "__main__":
        #     print("CSV format")
        #     load_data_from_gcs_to_bigquery("gs://example-78147/events.csv", bigquery.SourceFormat.CSV)
        #     print("\n")

        #     print("PARQUET format")
        #     load_data_from_gcs_to_bigquery("gs://example-78147/events.parquet", bigquery.SourceFormat.PARQUET)
        #     print("\n")

        #     print("AVRO format")
        #     load_data_from_gcs_to_bigquery("gs://example-78147/events.avro", bigquery.SourceFormat.AVRO)


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(MySpider)
    process.start()
