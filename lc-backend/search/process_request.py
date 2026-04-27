import django
from django.http import JsonResponse
import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from django.conf import settings
from datetime import datetime

import json
# import psycopg2


url: str = settings.SUPABASE_URL
key: str = settings.SUPABASE_KEY
supabase: Client = create_client(
    url,
    key,
    options=ClientOptions(
        postgrest_client_timeout=10,
        storage_client_timeout=10,
        schema="public",
    )
)



class process_request:
    def get(request, query, stringified_search_parameters):
        # this search engine requires the person im triyng to reach to use the same wording as me, which could create a barier to finding them
        search_parameters = json.loads(stringified_search_parameters)
        
        print(f"Received search request with query: {query} and parameters: {search_parameters}")
        if(query == "undefined"):
            print("no query, just filters")
            loads = int(search_parameters['loads'])
            addrate = int(search_parameters['addRate'])
            if search_parameters.get("searchType") == "Recent":
                supabase_response = supabase.rpc("search_all_no_query_results_recent", {"p_filters": search_parameters, "p_loads": loads, "p_addrate": addrate}).execute()
                length = supabase.rpc("search_all_no_query_results_total", {"p_filters": search_parameters}).execute().data
                fixed_json = supabase_response.data
            else:
                supabase_response = supabase.rpc("search_all_no_query_results_popular", {"p_filters": search_parameters, "p_loads": loads, "p_addrate": addrate}).execute()
                length = supabase.rpc("search_all_no_query_results_total", {"p_filters": search_parameters}).execute().data
                fixed_json = supabase_response.data
        else:
            loads = int(search_parameters['loads'])
            addrate = int(search_parameters['addRate'])
            if search_parameters.get("searchType") == "Recent":
                supabase_response = supabase.rpc("search_all_query_results_recent", {"p_query": query, "p_filters": search_parameters, "p_loads": loads, "p_addrate": addrate}).execute()
                length = supabase.rpc("search_all_query_results_length", {"p_query": query, "p_filters": search_parameters}).execute().data
                fixed_json = supabase_response.data
            else:
                supabase_response = supabase.rpc("search_all_query_results_popular", {"p_query": query, "p_filters": search_parameters, "p_loads": loads, "p_addrate": addrate}).execute()
                length = supabase.rpc("search_all_query_results_length", {"p_query": query, "p_filters": search_parameters}).execute().data
                fixed_json = supabase_response.data
         
        return JsonResponse({"message": "Search results retrieved successfully!", "data": fixed_json, "total_results": length}, status=200)