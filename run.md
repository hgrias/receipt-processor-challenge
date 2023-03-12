# Steps to Run

## Requirements
- Docker
- Clone repo on local:
  
        git clone https://github.com/hgrias/receipt-processor-challenge.git


## Steps

1. CD into the repo directory
2. Build the image 
   
        docker build -t receipt-api .
   
3. Run the API server

        docker run -p 5000:5000 receipt-api
   
4. Send requests to `http://127.0.0.1:5000`

---

## Examples

1. Using cURL
   1. Process a receipt

            curl --header "Content-Type: application/json" \
            --request POST \
            --data '{"retailer": "Target", "purchaseDate": "2022-01-02", "purchaseTime": "13:13", "total": "1.25", "items": [{ "shortDescription": "Pepsi - 12-oz", "price": "1.25" }]}' \
            http://localhost:5000/receipts/process

        Example response:

            {"id":"a588a1c0-987b-473c-8687-784b3fc4362d"}

    2. Get receipt points using response from process endpoint

            curl --request GET http://localhost:5000/receipts/a588a1c0-987b-473c-8687-784b3fc4362d/points

        Example response:

            {"points":31}