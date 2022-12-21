from elasticsearch import Elasticsearch


raw_index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "content": {
                    "type": "text"
                },
                "doc_id": {
                    "type": "text"
                },
                "doc_url": {
                    "type": "text"
                }
            }
        }
    }

stemmed_index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "analysis": {
                "filter": {
                    "russian_stop": {
                        "type": "stop",
                        "stopwords": "_russian_"
                    },
                    "russian_stemmer": {
                        "type": "stemmer",
                        "language": "russian"
                    }
                },
                "analyzer": {
                    "rebuilt_russian": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "russian_stop",
                            "russian_stemmer"
                        ]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "content": {
                    "type": "text",
                    "analyzer": "rebuilt_russian"
                },
                "doc_id": {
                    "type": "text"
                },
                "doc_url": {
                    "type": "text"
                }
            }
        }
    }

stemmed_pagerank_index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "analysis": {
                "filter": {
                    "russian_stop": {
                        "type": "stop",
                        "stopwords": "_russian_"
                    },
                    "russian_stemmer": {
                        "type": "stemmer",
                        "language": "russian"
                    }
                },
                "analyzer": {
                    "rebuilt_russian": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "russian_stop",
                            "russian_stemmer"
                        ]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "content": {
                    "type": "text",
                    "analyzer": "rebuilt_russian"
                },
                "doc_id": {
                    "type": "text"
                },
                "doc_url": {
                    "type": "text"
                },
                "pagerank": {
                    "type": "rank_feature"
                }
            }
        }
    }


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch(
        [{'host': '127.0.0.1', 'port': 9200, 'scheme': 'https'}],
        basic_auth=('elastic', '+*FA2JP_tXfvaBr-e6PQ'),
        verify_certs=False
    )
    if _es.ping():
        print('Elastic search подключен!')
    else:
        print('Подключиться к Elastic search не получилось(')
    return _es


# es index with raw documents (no lemmatization and stop words removal)
def create_raw_documents_index(es_obj):
    index_name = 'raw'
    try:
        if not es_obj.indices.exists(index=index_name):
            es_obj.indices.create(index=index_name, body=raw_index_settings)
            print('Индекс для необработанных текстов создан')
        else:
            print('Индекс для необработанных текстов уже существует')
    except Exception as ex:
        print(str(ex))


# es index with stemmed documents with stop words removal
def create_stemmed_documents_index(es_obj):
    index_name = 'stemmed'
    try:
        if not es_obj.indices.exists(index=index_name):
            es_obj.indices.create(index=index_name, body=stemmed_index_settings)
            print('Индекс для обработанных текстов создан')
        else:
            print('Индекс для обработанных текстов уже существует')
    except Exception as ex:
        print(str(ex))


# es index with stemmed documents with stop words removal + pagerank counted
def create_stemmed_documents_with_pagerank_index(es_obj):
    index_name = 'stemmed_pagerank'
    try:
        if not es_obj.indices.exists(index=index_name):
            es_obj.indices.create(index=index_name, body=stemmed_pagerank_index_settings)
            print('Индекс для обработанных документов с pagerankом создан')
        else:
            print('Индекс для обработанных документов с pagerankом уже существует')
    except Exception as ex:
        print(str(ex))


def create_indexes_if_missing(es_obj):
    create_raw_documents_index(es_obj)
    create_stemmed_documents_index(es_obj)
    create_stemmed_documents_with_pagerank_index(es_obj)


def import_record_to_elastic(es_obj, json_record, index_name):
    try:
        outcome = es_obj.index(index=index_name, body=json_record)
    except Exception as ex:
        print('Ошибка в индексации данных')
        print(str(ex))
