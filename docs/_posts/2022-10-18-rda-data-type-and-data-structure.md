---
layout: page
title: RDA Data Type and Data Structure
permalink: /data-type-and-data-structure
---

RDA container supports storing only two data types - 
* String
* RDA container

It’s the client’s responsibility to convert data from "whatever-data-type" to and from these two types, and these are what the client needs to do - 

## Converting primary data types to and from a string. 
Primary types are types that cannot be divided further in a programming language. These include integers, doubles, decimals, strings, etc. 

> *Values with type string are for storing primary-type data value (require client performing type-conversion).*

## Converting composite data types to and from an RDA. 
Composite types are types that can be divided further into “more basic” composite types or primary types in a programming language. This is more applicable to OOP, where composite types can be structs, classes, interfaces. 

> *Values with type RDA are for storing “the structural information” of a composite-type data object (Hint: via the object and its properties recursively implementing the IRdaSerializable interface). *

What is RDA (data type)? 
In a programming language, an RDA (or RDA Container) data type is a 1-dimension array of data elements, where the length of the array can be infinitely extended, and the data elements stored in the array can be 1) a string, or 2) an RDA container.

Because of the recursive structure of the RDA, any arbitrarily complex composite-type data can be divided into lower-dimension RDAs and eventually be “decomposed” into primary values and stored as string-type data elements inside an RDA container.
