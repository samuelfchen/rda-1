---
layout: page
title: RDA Tooling and Formatting
permalink: /rda-tooling-and-formatting
---

To improve viewing and assist debugging, the RDA API provides a formatted version of the encoded container, call “V2-Formatting”. An RDA container can be alternatively encoded in V2-format which uses line-breaks and indents to display RDA data elements values in a nicer format. The provided API also supports parsing RDA encoded in V2-format.

## An V2-format RDA example

Let's say we have the following data in the following table - 

| Name | Sex | Age | 
|------|-----|-----|
| Mary | F   | 52  | 
| John | M  | 70  |
| Kate | F   | 63  | 

Encoding the above data in “traditional” RDA encoding would produce the following string - 

```
|,\|Name,Sex,Age|Mary,F,52|John,M,70|Kate,F,63
```

Serializing the same container to a v2-formatted string will be like -

```
|,\|
  "Name"
  ,"Sex"
  ,"Age"
|  "Mary"
   ,"F"
   ,"52"
 |  "John"
    ,"M"
    ,"70"
 |   "Kate"
    ,"F"
    ,"63"
```

To print or serialize an RDA container int v2-format, use the API's **ToStringFormatted()** method.

## Tooling

It is almost certain that when manually working on text-based data containers, even with XML/JSON, it would require dedicated tools (Viewer or Editor software). There is an RDA Viewer program in the making and will be available in the future.  
