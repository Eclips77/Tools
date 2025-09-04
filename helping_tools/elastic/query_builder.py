"""
Elasticsearch Query Builder Module

This module provides a flexible query builder for Elasticsearch that allows
for creating complex queries using a fluent interface with method chaining.
"""

from typing import Dict, List, Optional, Any, Union, TypeVar, cast, Mapping


# Type definitions for method chaining
T = TypeVar('T', bound='ElasticQueryBuilder')
B = TypeVar('B', bound='BoolQueryBuilder')

class ElasticQueryBuilder:
    """
    A builder class for constructing Elasticsearch queries with a fluent interface.
    
    This class provides methods to create various types of Elasticsearch queries
    including search queries, aggregations, filters, and update/delete operations.
    It uses method chaining to allow for expressive and readable query construction.
    
    Attributes:
        query (Dict[str, Any]): The constructed query.
        _aggs (Dict[str, Any]): Aggregations for the query.
        _source (Union[bool, List[str]]): Source filtering settings.
        _size (Optional[int]): Result size limit.
        _from (Optional[int]): Result offset for pagination.
        _sort (List[Dict[str, Dict[str, str]]]): Sort criteria.
    """
    
    def __init__(self) -> None:
        """Initialize a new query builder with empty query structure."""
        self.query: Dict[str, Any] = {}
        self._aggs: Dict[str, Dict[str, Any]] = {}
        self._source: Union[bool, List[str]] = True
        self._size: Optional[int] = None
        self._from: Optional[int] = None
        self._sort: List[Dict[str, Dict[str, str]]] = []
        self._script: Optional[Dict[str, Any]] = None
        
    # ---- Basic Query Types ----
    
    def match(self: T, field: str, value: Any, operator: str = 'or', fuzziness: Optional[str] = None) -> T:
        """
        Add a match query clause.
        
        Args:
            field (str): The field to match against.
            value (Any): The value to match.
            operator (str, optional): The boolean operator to use. Defaults to 'or'.
            fuzziness (str, optional): Fuzziness parameter, e.g., 'AUTO'. Defaults to None.
            
        Returns:
            ElasticQueryBuilder: Self reference for method chaining.
        """
        match_params: Dict[str, Any] = {"query": value, "operator": operator}
        if fuzziness:
            match_params["fuzziness"] = fuzziness
            
        self.query = {"match": {field: match_params}}
        return self
        
    def term(self, field: str, value: Any) -> 'ElasticQueryBuilder':
        """
        Add a term query clause for exact matching.
        
        Args:
            field (str): The field to match against.
            value (Any): The exact value to match.
            
        Returns:
            ElasticQueryBuilder: Self reference for method chaining.
        """
        self.query = {"term": {field: {"value": value}}}
        return self
        
    def terms(self, field: str, values: List[Any]) -> 'ElasticQueryBuilder':
        """
        Add a terms query clause for matching multiple values.
        
        Args:
            field (str): The field to match against.
            values (List[Any]): List of values to match.
            
        Returns:
            ElasticQueryBuilder: Self reference for method chaining.
        """
        self.query = {"terms": {field: values}}
        return self
        
    def range(self, field: str, **kwargs) -> 'ElasticQueryBuilder':
        """
        Add a range query clause.
        
        Args:
            field (str): The field to apply the range to.
            **kwargs: Range parameters, e.g., gt, gte, lt, lte.
            
        Returns:
            ElasticQueryBuilder: Self reference for method chaining.
        """
        self.query = {"range": {field: kwargs}}
        return self
        
    def exists(self, field: str) -> 'ElasticQueryBuilder':
        """
        Add an exists query to check if a field exists.
        
        Args:
            field (str): The field to check for existence.
            
        Returns:
            ElasticQueryBuilder: Self reference for method chaining.
        """
        self.query = {"exists": {"field": field}}
        return self
        
    def wildcard(self, field: str, value: str) -> 'ElasticQueryBuilder':
        """
        Add a wildcard query for pattern matching.
        
        Args:
            field (str): The field to match against.
            value (str): The pattern to match (can contain * and ? wildcards).
            
        Returns:
            ElasticQueryBuilder: Self reference for method chaining.
        """
        self.query = {"wildcard": {field: {"value": value}}}
        return self
        
    def prefix(self, field: str, value: str) -> 'ElasticQueryBuilder':
        """
        Add a prefix query to match documents with fields starting with a prefix.
        
        Args:
            field (str): The field to match against.
            value (str): The prefix value.
            
        Returns:
            ElasticQueryBuilder: Self reference for method chaining.
        """
        self.query = {"prefix": {field: {"value": value}}}
        return self
        
    def regexp(self, field: str, value: str) -> 'ElasticQueryBuilder':
        """
        Add a regexp query for regular expression matching.
        
        Args:
            field (str): The field to match against.
            value (str): The regular expression pattern.
            
        Returns:
            ElasticQueryBuilder: Self reference for method chaining.
        """
        self.query = {"regexp": {field: {"value": value}}}
        return self
    
    # ---- Compound Queries ----
    
    def bool(self) -> 'BoolQueryBuilder':
        """
        Start building a bool query.
        
        Returns:
            BoolQueryBuilder: A boolean query builder for more complex queries.
        """
        return BoolQueryBuilder(self)
    
    def query_string(self: T, query_string: str, fields: Optional[List[str]] = None) -> T:
        """
        Add a query string query for advanced text search.
        
        Args:
            query_string (str): The query string text.
            fields (List[str], optional): Fields to search in. Defaults to None.
            
        Returns:
            ElasticQueryBuilder: Self reference for method chaining.
        """
        query_dict: Dict[str, Any] = {"query": query_string}
        if fields:
            query_dict["fields"] = fields
        
        self.query = {"query_string": query_dict}
        return self
    
    # ---- Aggregations ----
    
    def aggregation(self, name: str, agg_type: str, field: Optional[str] = None, **kwargs) -> 'ElasticQueryBuilder':
        """
        Add an aggregation to the query.
        
        Args:
            name (str): Name of the aggregation.
            agg_type (str): Type of aggregation (e.g., terms, avg, sum).
            field (str, optional): Field to aggregate on. Defaults to None.
            **kwargs: Additional aggregation parameters.
            
        Returns:
            ElasticQueryBuilder: Self reference for method chaining.
        """
        agg = {agg_type: {}}
        
        if field:
            agg[agg_type]["field"] = field
        
        agg[agg_type].update(kwargs)
        self._aggs[name] = agg
        
        return self
    
    # ---- Result Controls ----
    
    def source(self: T, fields: Union[bool, List[str]]) -> T:
        """
        Control which source fields to include in the response.
        
        Args:
            fields (Union[bool, List[str]]): True for all fields, False for no fields,
                                            or a list of fields to include.
            
        Returns:
            ElasticQueryBuilder: Self reference for method chaining.
        """
        self._source = fields
        return self
    
    def size(self, size: int) -> 'ElasticQueryBuilder':
        """
        Set the maximum number of results to return.
        
        Args:
            size (int): Maximum number of results.
            
        Returns:
            ElasticQueryBuilder: Self reference for method chaining.
        """
        self._size = size
        return self
    
    def from_offset(self, from_offset: int) -> 'ElasticQueryBuilder':
        """
        Set the offset for pagination.
        
        Args:
            from_offset (int): Offset value (number of results to skip).
            
        Returns:
            ElasticQueryBuilder: Self reference for method chaining.
        """
        self._from = from_offset
        return self
    
    def sort(self, field: str, order: str = "asc") -> 'ElasticQueryBuilder':
        """
        Add a sort criterion to the query.
        
        Args:
            field (str): Field to sort by.
            order (str, optional): Sort order ('asc' or 'desc'). Defaults to "asc".
            
        Returns:
            ElasticQueryBuilder: Self reference for method chaining.
        """
        self._sort.append({field: {"order": order}})
        return self
    
    # ---- Update Operations ----
    
    def script_update(self: T, script_source: str, script_params: Optional[Dict[str, Any]] = None) -> T:
        """
        Create a script update operation.
        
        Args:
            script_source (str): The script source code.
            script_params (Dict[str, Any], optional): Script parameters. Defaults to None.
            
        Returns:
            ElasticQueryBuilder: Self reference for method chaining.
        """
        script_dict: Dict[str, Any] = {
            "source": script_source,
            "lang": "painless"
        }
        
        if script_params:
            script_dict["params"] = script_params
            
        self._script = script_dict
        return self
    
    def update_by_query(self) -> Dict[str, Any]:
        """
        Create an update-by-query operation using the current query.
        
        Returns:
            Dict[str, Any]: The update-by-query body.
            
        Raises:
            ValueError: If no script is defined.
        """
        if not self._script:
            raise ValueError("Script must be defined for update_by_query")
            
        body = {"script": self._script}
        
        if self.query:
            body["query"] = self.query
            
        return body
    
    # ---- Delete Operations ----
    
    def delete_by_query(self) -> Dict[str, Any]:
        """
        Create a delete-by-query operation using the current query.
        
        Returns:
            Dict[str, Any]: The delete-by-query body.
            
        Raises:
            ValueError: If query is empty.
        """
        if not self.query:
            raise ValueError("Query must be defined for delete_by_query")
            
        return {"query": self.query}
    
    # ---- Build Methods ----
    
    def build(self) -> Dict[str, Any]:
        """
        Build the final search query object.
        
        Returns:
            Dict[str, Any]: The complete search query.
        """
        body: Dict[str, Any] = {}
        
        # Add query if defined
        if self.query:
            body["query"] = self.query
            
        # Add aggregations if defined
        if self._aggs:
            body["aggs"] = self._aggs
            
        # Add source filtering
        body["_source"] = self._source
        
        # Add size if defined
        if self._size is not None:
            body["size"] = self._size
            
        # Add from if defined
        if self._from is not None:
            body["from"] = self._from
            
        # Add sort if defined
        if self._sort:
            body["sort"] = self._sort
            
        return body


class BoolQueryBuilder:
    """
    A builder for constructing Elasticsearch bool queries.
    
    This class helps build bool queries with must, must_not, should, and filter clauses.
    It's designed to be used in conjunction with ElasticQueryBuilder.
    
    Attributes:
        parent (ElasticQueryBuilder): The parent query builder.
        must_clauses (List[Dict[str, Any]]): Must clauses.
        must_not_clauses (List[Dict[str, Any]]): Must not clauses.
        should_clauses (List[Dict[str, Any]]): Should clauses.
        filter_clauses (List[Dict[str, Any]]): Filter clauses.
        _minimum_should_match (Optional[int]): Minimum should match parameter.
    """
    
    def __init__(self, parent: ElasticQueryBuilder):
        """
        Initialize a bool query builder.
        
        Args:
            parent (ElasticQueryBuilder): The parent query builder.
        """
        self.parent = parent
        self.must_clauses: List[Dict[str, Any]] = []
        self.must_not_clauses: List[Dict[str, Any]] = []
        self.should_clauses: List[Dict[str, Any]] = []
        self.filter_clauses: List[Dict[str, Any]] = []
        self._minimum_should_match: Optional[int] = None
    
    def must(self: B, query_dict: Dict[str, Any]) -> B:
        """
        Add a must clause to the bool query.
        
        Args:
            query_dict (Dict[str, Any]): The query dict to add.
            
        Returns:
            BoolQueryBuilder: Self reference for method chaining.
        """
        self.must_clauses.append(query_dict)
        return self
    
    def must_not(self, query_dict: Dict[str, Any]) -> 'BoolQueryBuilder':
        """
        Add a must_not clause to the bool query.
        
        Args:
            query_dict (Dict[str, Any]): The query dict to add.
            
        Returns:
            BoolQueryBuilder: Self reference for method chaining.
        """
        self.must_not_clauses.append(query_dict)
        return self
    
    def should(self, query_dict: Dict[str, Any]) -> 'BoolQueryBuilder':
        """
        Add a should clause to the bool query.
        
        Args:
            query_dict (Dict[str, Any]): The query dict to add.
            
        Returns:
            BoolQueryBuilder: Self reference for method chaining.
        """
        self.should_clauses.append(query_dict)
        return self
    
    def filter(self, query_dict: Dict[str, Any]) -> 'BoolQueryBuilder':
        """
        Add a filter clause to the bool query.
        
        Args:
            query_dict (Dict[str, Any]): The query dict to add.
            
        Returns:
            BoolQueryBuilder: Self reference for method chaining.
        """
        self.filter_clauses.append(query_dict)
        return self
    
    def minimum_should_match(self: B, value: int) -> B:
        """
        Set the minimum_should_match parameter.
        
        Args:
            value (int): Minimum number of should clauses that must match.
            
        Returns:
            BoolQueryBuilder: Self reference for method chaining.
        """
        self._minimum_should_match = value
        return self
    
    def end(self) -> ElasticQueryBuilder:
        """
        End the bool query builder and return to the parent query builder.
        
        Returns:
            ElasticQueryBuilder: The parent query builder.
        """
        bool_query: Dict[str, Any] = {}
        
        if self.must_clauses:
            bool_query["must"] = self.must_clauses
            
        if self.must_not_clauses:
            bool_query["must_not"] = self.must_not_clauses
            
        if self.should_clauses:
            bool_query["should"] = self.should_clauses
            
        if self.filter_clauses:
            bool_query["filter"] = self.filter_clauses
            
        if self._minimum_should_match is not None:
            bool_query["minimum_should_match"] = self._minimum_should_match
            
        self.parent.query = {"bool": bool_query}
        return self.parent




# Example usage:if __name__ == "__main__":
    # Build a complex query
    builder = ElasticQueryBuilder()
    query = (builder
             .bool()
                 .must({"match": {"title": {"query": "Elasticsearch", "operator": "and"}}})
                 .filter({"term": {"status": "published"}})
                 .should({"range": {"publish_date": {"gte": "2023-01-01"}}})
                 .minimum_should_match(1)
                 .end()
             .aggregation("top_authors", "terms", field="author.keyword", size=5)
             .source(["title", "author", "publish_date"])
             .size(10)
             .from_offset(0)
             .sort("publish_date", "desc")
             .build())