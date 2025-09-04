"""
MongoDB Query Builder Module

This module provides a simple query builder for MongoDB that allows
for creating queries with a fluent interface.
"""

from typing import Dict, List, Optional, Any, Union, TypeVar, Set


T = TypeVar('T', bound='MongoQueryBuilder')


class MongoQueryBuilder:
    """
    A simple builder class for constructing MongoDB queries with a fluent interface.
    
    This class provides methods to create various types of MongoDB queries
    and filters with clear, chainable methods.
    
    Attributes:
        query (Dict[str, Any]): The constructed query filter.
        projection (Dict[str, Any]): Fields to include/exclude in results.
        sort_criteria (Dict[str, int]): Sort criteria for results.
    """
    
    def __init__(self) -> None:
        """Initialize an empty query builder."""
        self.query: Dict[str, Any] = {}
        self.projection: Dict[str, Any] = {}
        self.sort_criteria: Dict[str, int] = {}
        self.skip_value: Optional[int] = None
        self.limit_value: Optional[int] = None
    
    # ---- Basic Query Methods ----
    
    def eq(self: T, field: str, value: Any) -> T:
        """
        Add equality filter (field equals value).
        
        Args:
            field: Field name to filter on.
            value: Value to match.
            
        Returns:
            MongoQueryBuilder: Self reference for method chaining.
        """
        self.query[field] = value
        return self
    
    def ne(self: T, field: str, value: Any) -> T:
        """
        Add not-equals filter (field not equal to value).
        
        Args:
            field: Field name to filter on.
            value: Value to exclude.
            
        Returns:
            MongoQueryBuilder: Self reference for method chaining.
        """
        self.query[field] = {'$ne': value}
        return self
    
    def gt(self: T, field: str, value: Any) -> T:
        """
        Add greater-than filter.
        
        Args:
            field: Field name to filter on.
            value: Value to compare against.
            
        Returns:
            MongoQueryBuilder: Self reference for method chaining.
        """
        self.query[field] = {'$gt': value}
        return self
    
    def gte(self: T, field: str, value: Any) -> T:
        """
        Add greater-than-or-equal filter.
        
        Args:
            field: Field name to filter on.
            value: Value to compare against.
            
        Returns:
            MongoQueryBuilder: Self reference for method chaining.
        """
        self.query[field] = {'$gte': value}
        return self
    
    def lt(self: T, field: str, value: Any) -> T:
        """
        Add less-than filter.
        
        Args:
            field: Field name to filter on.
            value: Value to compare against.
            
        Returns:
            MongoQueryBuilder: Self reference for method chaining.
        """
        self.query[field] = {'$lt': value}
        return self
    
    def lte(self: T, field: str, value: Any) -> T:
        """
        Add less-than-or-equal filter.
        
        Args:
            field: Field name to filter on.
            value: Value to compare against.
            
        Returns:
            MongoQueryBuilder: Self reference for method chaining.
        """
        self.query[field] = {'$lte': value}
        return self
    
    def between(self: T, field: str, min_value: Any, max_value: Any) -> T:
        """
        Add range filter (field between min and max values).
        
        Args:
            field: Field name to filter on.
            min_value: Minimum value (inclusive).
            max_value: Maximum value (inclusive).
            
        Returns:
            MongoQueryBuilder: Self reference for method chaining.
        """
        self.query[field] = {'$gte': min_value, '$lte': max_value}
        return self
    
    def in_list(self: T, field: str, values: List[Any]) -> T:
        """
        Add in-list filter (field value is in the provided list).
        
        Args:
            field: Field name to filter on.
            values: List of values to match against.
            
        Returns:
            MongoQueryBuilder: Self reference for method chaining.
        """
        self.query[field] = {'$in': values}
        return self
    
    def nin_list(self: T, field: str, values: List[Any]) -> T:
        """
        Add not-in-list filter (field value is not in the provided list).
        
        Args:
            field: Field name to filter on.
            values: List of values to exclude.
            
        Returns:
            MongoQueryBuilder: Self reference for method chaining.
        """
        self.query[field] = {'$nin': values}
        return self
    
    def exists(self: T, field: str, exists: bool = True) -> T:
        """
        Add exists filter (field exists or not).
        
        Args:
            field: Field name to check existence of.
            exists: Whether field should exist. Defaults to True.
            
        Returns:
            MongoQueryBuilder: Self reference for method chaining.
        """
        self.query[field] = {'$exists': exists}
        return self
    
    def type_filter(self: T, field: str, bson_type: Union[int, str]) -> T:
        """
        Add type filter (field is of specific BSON type).
        
        Args:
            field: Field name to check type of.
            bson_type: BSON type code or name.
            
        Returns:
            MongoQueryBuilder: Self reference for method chaining.
        """
        self.query[field] = {'$type': bson_type}
        return self
    
    def regex(self: T, field: str, pattern: str, options: Optional[str] = None) -> T:
        """
        Add regex filter (field matches regular expression).
        
        Args:
            field: Field name to match against.
            pattern: Regular expression pattern.
            options: Regex options (e.g. 'i' for case-insensitive). Defaults to None.
            
        Returns:
            MongoQueryBuilder: Self reference for method chaining.
        """
        if options:
            self.query[field] = {'$regex': pattern, '$options': options}
        else:
            self.query[field] = {'$regex': pattern}
        return self
    
    # ---- Logical Operators ----
    
    def and_filter(self: T, *filters: Dict[str, Any]) -> T:
        """
        Add AND logical filter.
        
        Args:
            *filters: One or more query filters to AND together.
            
        Returns:
            MongoQueryBuilder: Self reference for method chaining.
        """
        if '$and' not in self.query:
            self.query['$and'] = []
            
        self.query['$and'].extend(filters)
        return self
    
    def or_filter(self: T, *filters: Dict[str, Any]) -> T:
        """
        Add OR logical filter.
        
        Args:
            *filters: One or more query filters to OR together.
            
        Returns:
            MongoQueryBuilder: Self reference for method chaining.
        """
        if '$or' not in self.query:
            self.query['$or'] = []
            
        self.query['$or'].extend(filters)
        return self
    
    def nor_filter(self: T, *filters: Dict[str, Any]) -> T:
        """
        Add NOR logical filter.
        
        Args:
            *filters: One or more query filters to NOR together.
            
        Returns:
            MongoQueryBuilder: Self reference for method chaining.
        """
        if '$nor' not in self.query:
            self.query['$nor'] = []
            
        self.query['$nor'].extend(filters)
        return self
    
    def not_filter(self: T, field: str, filter_expr: Dict[str, Any]) -> T:
        """
        Add NOT logical filter.
        
        Args:
            field: Field name to apply NOT filter to.
            filter_expr: Filter expression to negate.
            
        Returns:
            MongoQueryBuilder: Self reference for method chaining.
        """
        self.query[field] = {'$not': filter_expr}
        return self
    
    # ---- Result Shaping Methods ----
    
    def include_fields(self: T, *fields: str) -> T:
        """
        Include only specified fields in results.
        
        Args:
            *fields: Fields to include.
            
        Returns:
            MongoQueryBuilder: Self reference for method chaining.
        """
        for field in fields:
            self.projection[field] = 1
        return self
    
    def exclude_fields(self: T, *fields: str) -> T:
        """
        Exclude specified fields from results.
        
        Args:
            *fields: Fields to exclude.
            
        Returns:
            MongoQueryBuilder: Self reference for method chaining.
        """
        for field in fields:
            self.projection[field] = 0
        return self
    
    def sort(self: T, field: str, ascending: bool = True) -> T:
        """
        Add a sort criterion.
        
        Args:
            field: Field to sort by.
            ascending: Sort direction. Defaults to True.
            
        Returns:
            MongoQueryBuilder: Self reference for method chaining.
        """
        self.sort_criteria[field] = 1 if ascending else -1
        return self
    
    def skip(self: T, count: int) -> T:
        """
        Set number of documents to skip.
        
        Args:
            count: Number of documents to skip.
            
        Returns:
            MongoQueryBuilder: Self reference for method chaining.
        """
        self.skip_value = count
        return self
    
    def limit(self: T, count: int) -> T:
        """
        Set maximum number of documents to return.
        
        Args:
            count: Maximum number of documents.
            
        Returns:
            MongoQueryBuilder: Self reference for method chaining.
        """
        self.limit_value = count
        return self
    
    # ---- Query Building Method ----
    
    def build(self) -> Dict[str, Any]:
        """
        Build the final query parameters.
        
        Returns:
            Dict[str, Any]: Dictionary with query filter, projection, and options.
        """
        result: Dict[str, Any] = {
            'filter': self.query
        }
        
        if self.projection:
            result['projection'] = self.projection
            
        if self.sort_criteria:
            result['sort'] = self.sort_criteria
            
        if self.skip_value is not None:
            result['skip'] = self.skip_value
            
        if self.limit_value is not None:
            result['limit'] = self.limit_value
            
        return result
