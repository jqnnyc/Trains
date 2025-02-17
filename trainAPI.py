import requests
import xml.etree.ElementTree as ET
import pandas as pd
import re
import xml.dom.minidom
from lxml import etree

def returnTrains (loc):

    loc = "FLE"

    # Define the headers for the HTTP request
    headers = {
        'Accept': 'text/xml',
        'Content-Type': 'text/xml; charset=utf-8',
        'SOAPAction': 'http://thalesgroup.com/RTTI/2015-05-14/ldb/GetDepBoardWithDetails'
    }

    # Define the body of the SOAP request
    body = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:typ="http://thalesgroup.com/RTTI/2013-11-28/Token/types" xmlns:ldb="http://thalesgroup.com/RTTI/2021-11-01/ldb/">
    <soapenv:Header>
        <typ:AccessToken>
            <typ:TokenValue>d3242ece-d3c8-49dc-9389-d433aed7bf3c</typ:TokenValue>
        </typ:AccessToken>
    </soapenv:Header>
    <soapenv:Body>
        <ldb:GetDepBoardWithDetailsRequest>
            <ldb:numRows>10</ldb:numRows>
            <ldb:crs>{loc}</ldb:crs>
            <ldb:timeOffset>0</ldb:timeOffset>
            <ldb:timeWindow>240</ldb:timeWindow>
        </ldb:GetDepBoardWithDetailsRequest>
    </soapenv:Body>
    </soapenv:Envelope>"""

    # Perform the HTTP request
    response = requests.post(
        url="https://lite.realtime.nationalrail.co.uk/OpenLDBWS/ldb12.asmx",
        headers=headers,
        data=body,
        verify=False #probs shouldn't do this...
    )

    # Check if the request was successful
    if response.status_code == 200:
        # Convert XML response to string
        xml_string = response.text
        
        # Parse XML
        root = etree.fromstring(xml_string.encode("utf-8"))

        # Rename all tags without namespaces
        for elem in root.iter():
            elem.tag = re.sub(r"{.*}", "", elem.tag)

        # Find all <service> elements directly
        services = root.xpath("//trainServices/service")

        # Extract std and etd values
        data = [
            {
                "std": service.xpath("std/text()")[0] if service.xpath("std") else "N/A"
                ,"etd": service.xpath("etd/text()")[0] if service.xpath("etd") else "N/A"
                ,"operator": service.xpath("operator/text()")[0] if service.xpath("operator") else "N/A"
                ,"origin": service.xpath(".//origin/location/locationName/text()")[0] if service.xpath(".//origin/location/locationName") else "N/A"
                ,"destination": service.xpath(".//destination/location/locationName/text()")[0] if service.xpath(".//destination/location/locationName") else "N/A"
                ,"platform": service.xpath("platform/text()")[0] if service.xpath("platform") else "N/A"
                ,"crs": service.xpath("./../../crs/text()")[0] if service.xpath("./../../crs") else "N/A"
            }
            for service in services
        ]

        df = pd.DataFrame(data)
        #print(df)
        return df

    else:
        print(f"Request failed with status code {response.status_code}")



