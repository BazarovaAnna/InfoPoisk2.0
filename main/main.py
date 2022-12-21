import warnings
from document_processing import process_doc_collection
from elastic_search import connect_elasticsearch, create_indexes_if_missing
from search_evaluator import evaluate_search
from page_rank import create_documents_graph, count_pagerank, import_pagerank_to_elastic_search


DOCUMENTS_COLLECTION_PATH = "../resources/byweb_for_course"
SEARCH_EVALUATION_RESULTS_PATH = "../resources/evaluation_metrics.txt"

if __name__ == "__main__":
    warnings.filterwarnings('ignore', message="Unverified HTTPS request is being made to host*")
    elastic = connect_elasticsearch()
    create_indexes_if_missing(elastic)
    documents_graph, document_by_page_url = create_documents_graph(elastic)
    pagerank_counted = count_pagerank(documents_graph)
    import_pagerank_to_elastic_search(elastic, document_by_page_url, pagerank_counted)
    process_doc_collection(DOCUMENTS_COLLECTION_PATH, elastic, need_raw=True, need_stemmed=True)
    evaluate_search(elastic, SEARCH_EVALUATION_RESULTS_PATH)
