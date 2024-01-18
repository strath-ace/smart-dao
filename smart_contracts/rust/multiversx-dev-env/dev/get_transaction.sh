curl --request GET \
  --url http://localhost:9200/transactions/_search \
  --header 'Content-Type: application/json' \
  --data '{
    "size" : 100,
    "query": {
        "bool": {
            "should": [
                {
                    "match": {
                        "sender": "erd1k2s324ww2g0yj38qn2ch2jwctdy8mnfxep94q9arncc6xecg3xaq6mjse8"
                    }
                },
                {
                    "match": {
                        "receiver": "erd1k2s324ww2g0yj38qn2ch2jwctdy8mnfxep94q9arncc6xecg3xaq6mjse8"
                    }
                },
                {
                    "match": {
                        "receivers": "erd1k2s324ww2g0yj38qn2ch2jwctdy8mnfxep94q9arncc6xecg3xaq6mjse8"
                    }
                }
            ]
        }
    },
     "sort": [
        {
            "timestamp": {
                "order": "desc"
            }
        }
    ]
}' \
  -o output_transaction.json 

