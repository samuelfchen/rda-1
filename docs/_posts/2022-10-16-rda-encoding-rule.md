---
layout: page
title: RDA Encoding Rule With Examples
permalink: /rda-encoding-rule
---

RDA is called a "delimited array" because the stored data elements are in a listing order (an "array") and are delimited by one or more selected characters ("delimiters"). In the below example, the delimiter is character '|'. Below is an encoded text string of an RDA container, which contains three data elements "One", "Two", and "Three" : 
```
|\|One|Two|Three
```

An RDA container is an encoded string (a serial of utf-8 characters) comprises two substring sections: a "header" section which contains the definition of the container's encoding parameters, followed by a "payload" section which contains the data content encoded using the defined encoding parameters.[^1] 

[^1]: A zero-dimension RDA container only has the payload but no header, in which case the container is the payload which is the data content.

> Encoding Rule #1:
> The header section starts from the container string's first character and to the first repeat of the first character, inclusive; the payload section is the rest of the container string.

In the above example, the 3rd character of the container string is the first repeat of the 1st character of the string (char '\|'), so the header of the RDA is the substring "\|\\\|", and the payload section is the rest of the string which is "One\|Two\|Three".

> Encoding Rule #2:
> In a header section, the second-last character is the escape character; the characters before the escape char are the delimiters. Collectively in a header section, the delimiters and the escape char must be distinct to each other - i.e. cannot contain duplicate.

RDA encoding parameters in the header are defined per container, and any characters can be chosen to be the encoding characters - there are no "reserved" characters or keywords. A parser can be automatically configured by reading and parsing the header section, before proceeding to parse the payload, i.e. the encoded data content. For example, the following RDA string contains identical content to the previous RDA, but it chooses to use character 'w' as the delimiter -

```
w\wOnewT\wowThree
```

In this example, because the chosen delimiter is an alpha-numeric letter (not recommended), the container string appears to be scrambled. However a correctly implemented parser would be able to decode the container string with no difference from decoding other RDA containers. Also, note the escaping applied to encoding the second value "Two" in the array, resulting the encoded data content as "T\\wo". The escape character skips the decoding interpretation to its following character (the 'w') and makes it retain its literal value, rather than being interpreted by the parser as a delimiter.

> Encoding Rule #3:
> In decoding an encoded RDA string, an 'escape' character and its next character shall be parsed together, and the output shall be the literal (non-encoded) value of the next character. When there is no furter character after an 'escape' character, the parsed output shall be empty.

When multiple delimiters are defined in the header and used for encoding the payload's data content, an RDA becomes a container that can store multi-dimensional or hierarchical data. The number of dimensions of an RDA container is the same as the number of the delimiters defined in its header, where the first delimiter in order is used for delimiting the payload data into data elements in the first dimension, and the second defined delimiter is used for delimiting the second dimension data elements inside each of the first dimension data elements, and so on.

> Encoding Rule #4:
> The order of the delimiters defined in the header determines at which dimension level each or the delimiter is used for the payload data elements encoding. I.e. the first delimiter is used for delimiting values at the 1st dimension, the second delimiter is used for delimiting values at the 2nd dimension within the parsed values from the 2nd dimension, etc. The payload string is recursively concatenated by joining the data element sub-string at each dimension level with the corresponding delimiter defined in the header for the dimension.

In the next example, the RDA has two defined delimiters '|' and ',' in its header, and is used to store a set of 2-dimensional data.
```
|,\|Name,Sex,Age|Mary,F,52|John,M,70|Kate,F,63
```
In the example, the first defined delimiter character '|' separates the payload section into substring values of the first dimension, and the second defined delimiter ',' separates substring values of the first dimension into second dimension values. In comparison, an equivalent CSV container containing the same data as the above RDA would be -
```
Name,Sex,Age
Mary,F,52
John,M,70
Kate,F,63
```

Compared to XML and JSON,  because of the removal of the meta data (the "tags") and formatting, RDA encoded container is less "eye-balling" friendly. An RDA encoder/parser program shall be used in practice, and you shouldn't need to dealing with RDA encoding manually. This is true even for working on XML and JSON, when the schema is complex and there are thousands of records, you will need dedicated tools for manually handling the encoded data. For assiatence in viewing and editing RDA manually, please refer to the discussion on [RDA tooling and "version-2" formatting](https://sierrathedog.github.io/rda/rda-tooling-and-formatting).
