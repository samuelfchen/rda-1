---
layout: page
title: Metadata Vs Schema
permalink: /metadata-vs-schema
---

Schema in XML and JSON has its uses: it acts as the data contract between two applications that are using the XML or JSON container for exchanging data. Without having the schema, how can RDA provide the same function?

The answer is to use extra "channel" to store the "contract" as metadata.

Let's take a look at some examples. Let's say we need to have a data contract for the following data in the following table - 

| Name | Sex | Age | 
|------|-----|-----|
| Mary | F   | 52  | 
| John | M  | 70  |
| Kate | F   | 63  | 

A JSON container for this data would be something like - 

```
[
 {"Name":"Mary","Sex":"F","Age":52},
 {"Name":"John","Sex":"M","Age":70},
 {"Name":"Kate","Sex":"F","Age":63}
]
```

And an XML container would be something like  -
```
<Group>
  <Person>
   <Name>Mary</Name>
   <Sex>F</Sex>
   <Age>52</Age>
  </Person>
  <Person>
   <Name>John</Name>
   <Sex>M</Sex>
   <Age>70</Age>
  </Person>
  <Person>
   <Name>Kate</Name>
   <Sex>F</Sex>
   <Age>63</Age>
  </Person>
</Group>
```

To just have the data in an RDA container, it could be -
```
|,\|Mary,F,52|John,M,70|Kate,F,63
```
For including the data's header row, which contains the "names" for each column, we can get the applications to agree that the first array element at the RDA's data array is dedicated to metadata, in this case, to store column names. So the RDA container becomes - 

```
|,\|Name,Sex,Age|Mary,F,52|John,M,70|Kate,F,63
```

Note the goal of data transport to to move the data from one application to another application. Where the informtion is placed inside the container, is for the application to decide. In the above case, the column names of each data column are placed in RDA[0], as values in a secondary array. The RDA now carries almost as much as infomation as the JSON container, except for JSON, each data element has a implied "data type", which can be "string", "number", "boolean", depending on the JSON notation. To further capture this information using the RDA, one technique is to fork an extra dimension, like this - 

```
|,:\|Name:string,Sex:string,Age:number|Mary,F,52|John,M,70|Kate,F,63
```

So at the receiving end, if data type validation is required by the "contract", the metadata for enforcing the contract is available in the RDA. 

For using RDA to mimicing the XML schema, once again we want to capture all the essential data elements. Comparing to the JSON container, the XML container has included a value hierarchy, which is: Group>Person>{properties of a Person}. To be able to capture the element hierarchy in an RDA, let's say the applications agree the first element is the root element, and the array elements following the first element are children of the first/root element.
```
|,;:\|Group,Person;Name;Sex;Age|,;Mary;F;52|,;John;M;70|,;Kate;F;63
```
As shown in the above RDA, Rda[0] is the agreed place for metadata, which has "Group,Person;Name;Sex;Age", which demonstrate the following hierarchy.

{Tree drawing here ...}





In practice, text-based data containers such as XML/JSON and RDA are for computer programs to store and exchange data using the purposely built encoding/decoding API. Because of RDA's simplicity, both in its encoding rules and the provided storage structure, the API provided from this repo is inherently simple yet extremely flexible and capable.

