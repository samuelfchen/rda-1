---
layout: page
title: A Contender to XML and JSON
permalink: /
---

# Recursive Delimited Array 
[![Awesome](https://cdn.jsdelivr.net/gh/sindresorhus/awesome@d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome#readme)

<img src="docs/image/rda_logo.png" align="right" height="128">

Recursive Delimited Array, or RDA, is a text-encoding format for a string-based data container. RDA is used for "serializing" structured data, so the data can be stored or transported cross-language and cross-platform.

## A Problem Of XML/JSON

XML and JSON container uses a schema to specify the data type and data structure of its content, thus data exchange using XML/JSON containers are data-specific and application-dependent. If an application changes the data format and the schema, all its connected applications may need to change their container-parsing logic to remain compatible. This can be especially difficut if the connected applications are developed and maintained by different parties. 

In contrast, RDA is a **schema-less** container format for storing **generic data**[^1]. It is the key of our soltuion for building application-independent data-exchange pipelines that compatibility can be easily mananged and maintained. 

[^1]: RDA container only supports two data types: [RDA or string](https://sierrathedog.github.io/rda/data-type-and-data-structure). Composite data must implement a "ToRda" method to convert itself into an RDA, and scalar data must be first converted to a string value, which then is wrapped and stored as a 0-dimension RDA.

> *An RDA container is like a plain box that has an unlimited number of pockets for freely storing "any stuff", whereas an XML or JSON container is like a wallet, which has specific places for storing coins, notes, and cards.* 

Being schema-less and generic, RDA promotes "decoupling" the data-transport layer from the business applications, and decoupled systems are known for better flexibility and maintainability. RDA can be particularly beneficial for maintaining compatibility if in the system there are one-to-many, or many-to-many data-exchanging pipelines between the programs. 


## RDA Encoding Examples

The following example shows a 1-dimension RDA-encoded string container containing a list of data elements: "One", "Two", and "Three". 

```
|\|One|Two|Three
```
The next example is a 2-dimension RDA container that contains the data equivalent to the content of the following table.
```
|,\|Name,Sex,Age|Mary,F,52|John,M,70|Kate,F,63
```

| Name | Sex | Age | 
|------|-----|-----|
| Mary | F   | 52  | 
| John | M  | 70  |
| Kate | F   | 63  | 


An RDA container provides an expandable multidimensional data storage, but has no application-depending components in the encoding. As in the above examples - 
* Instead of using tags or markups, RDA uses a **simple** and **compact** delimited encoding for separating and structuring data elements; 
* Instead of using named-paths to navigate a storage "tree", RDA's storage is a mutli-dimensional array which can use integer-based indexes for addressing data elements; and 
* The dimensions of an RDA container's storage can be dynamically extended by increasing the number of delimited levels [^2]. 

[^2]: Full details of the encoding rules can be found [here](https://sierrathedog.github.io/rda/rda-encoding-rule).

## Benefits and Use Cases


RDA offers a simple and powerful way for cross-language and cross-application Object Serialization. For example, you can send [a "Person" object as a serialized RDA container](https://sierrathedog.github.io/rda/2022/10/03/obj-serialization-pattern.html) from your Java program to a Python program, and in the Python program, the RDA container can be de-serialized to a "User" object, because contrary to using XML/JSON, the "Person" object and the "User" object can have different "schema". 

Another use of RDA is to maintain versioning compatibility between a sender and a receiver. Because of RDA's recursive nature, each "pocket" in an RDA container is itself another RDA. You can have multiple "children" RDAs inside a "parent" RDA, which means you can transfer data of multiple versions and multiple protocols "side-by-side" in a single container. 

Indeed, being able to send multiple pieces of "anything" side-by-side in a container can have many interesting uses: how about sending XML data (which is a string) together with a DTD (another string) for validation, or sending an encrypted document together with the associated digital signature and public key, or sending a computing "workload" that has some data together with an executable script to a data-processing unit, etc.

An RDA container is much more compact compared to an XML or JSON container with the same content, and it is generally much easier to develop an RDA container parser, thanks to its simple delimiter-based encoding. Also, RDA encoding does not use any reserved keyword or character for its encoding, so it is more robust and resilient to data corruption. For example, it allows native line-break chars in the data content, unlike other formats that must use replacement strings (e.g. "\\n") to avoid parsing errors.

## Getting Started

This GitHub repo provides parser/encoder APIs for using RDA in [C#](https://github.com/sierrathedog/rda/tree/main/src/CSharp), [Java](https://github.com/sierrathedog/rda/blob/main/src/Java/), and [Python](https://github.com/sierrathedog/rda/blob/main/src/Python). These APIs are well-tested and super lightweight. To start, simply drop in the provided source files in your project and start programming. *There is no other dependency or installation required.*

## Using The API

Using the API is super simple - all you need to know are the few methods from a class called "Rda" and an interface called "IRdaSerializable"[^3], as explained below.  
[^3]:Examples of using API are demonstrated in C#. Methods of using the Java API and the Python API are very similar.

### Class *Rda* 

The Rda class implements the RDA encoding and decoding, and is modeled intuitively as a "container" which provides - 

* **Getter-Setter**  methods for accessing the container's content using index-based addresses, 
* **ToString** method for serializing the container object and its content into a string, and 
* **Parse** method for converting an RDA-encoded string back to a Rda container object in the program.

The example below shows using the **SetValue**/**GetValue** methods for storing/retrieving string values, and also the **ToString** and the **Parse** methods for serializing and deserializing.

```c#
using UniversalDataTransport;  //the Rda class is defined in this domain

class RdaDemo
{
    Rda rda1 = new Rda();    //create a new RDA container object

    //store some values at some randomly-chosen locations in the container
    rda1.SetValue(0, "One");  //storing value "One" at index = 0
    rda1.SetValue(1, "Two");
    rda1.SetValue(2, "Three");

    //call ToString() to serialize the container to a string
    System.Console.WriteLine(rda1.ToString());   //prints "|\|One|Two|Three"

    //de-serialize an RDA container from an encoded string
    Rda rda2 = Rda.Parse(rda1.ToString());

    //test the de-serialized container: retrieve a stored value from the container at index = 2 
    System.Console.WriteLine(rda2.GetValue(2));   //prints "Three"
}
```

This next example show using the **SetRda**/**GetRda** methods for storing RDAs inside an RDA, also shows using the Rda container's multi-dimensional storage space.

```c#
class RdaDemo2
{
    //create two RDA containers each containing some data elements
    Rda rda0 = Rda.Parse(@"|\|One|Two|Three");    
    Rda rda1= Rda.Parse(@"|\|A|B|C|D");    

    Rda rdaX = new Rda();    //create a "parent" RDA container

    //SetRda() allows storing "children" Rda objects in the "parent" container
    rdaX.SetRda(0, rda0);  //stores rda0 at index = 0
    rdaX.SetRda(1, rda1);  //stores rda1 at index = 1

    //serialize the "parent" container, which is a 2D data array, to a string
    System.Console.WriteLine(rdaX.ToString());   //prints "|,\|One,Two,Three|A,B,C,D"

    //retrieve a stored value from the 2D data array, using integer-array address [1,2] 
    System.Console.WriteLine(rdaX.GetValue(new int[]{1,2}));   //prints "C"

    //retrieve a stored Rda object from the parent RDA container
    Rda rda1a = rdaX.GetRda(1);     //gets the stored child Rda object
}

```

### Interface *IRdaSerializable* 
The IRdaSerializable interface is for implementing [a consistent and unified object-serialization pattern using RDA](https://sierrathedog.github.io/rda/object-serialization-pattern). It includes the following two methods:

* **ToRda()**: here you specify the data elements and properties of the object that need to be stored in an RDA container for the serialization. It includes the placement of these properties inside the resulted RDA, and any applicable type-conversion and/or data-validation.

* **FromRda(rda)**: here you restore the object's properties from the string values retrieved from a provided RDA container. It includes locating the values inside the received RDA for the properties, and any applicable type-conversion and/or data-validation and error-handling.

 The following example demonstrates how a business object (the "Address") specifies how its properties ("AddressLines" and "ZIP") would be serialized through inplementing the IRdaSerializable interface.

```c#
class Address : IRdaSerializable
{
    // allocate addresses in the RDA for storing/retrieving object properties
    public enum RDA_INDEX : int { LINES = 0, ZIP = 1 }

    // some example properties that require serialization
    public string AddressLines = "Line 1\nLine 2\nLine 3";
    public string ZIP = "NY 21540";

    // define how the properties are stored in an RDA for serialization
    public Rda ToRda()
    {
        //create an RDA container for holding the result
        var rda = new Rda();  
        
        // storing the properties to the designated places
        // note: type-conversion would be required here if the data's type is not string
        rda[(int)RDA_INDEX.LINES].ScalarValue = this.AddressLines;
        rda[(int)RDA_INDEX.ZIP].ScalarValue = this.ZIP;

        return rda;
    }

    // define how the properties are restored from an RDA during de-serialization
    public IRdaSerializable FromRda(Rda rda)
    {
        // implement value parsing and type-conversion if required (none in this example)
        this.AddressLines = rda[(int)RDA_INDEX.LINES].ScalarValue;
        this.ZIP = rda[(int)RDA_INDEX.ZIP].ScalarValue;
        return this;
    }
}
```

### Test Cases

The unit tests [[C#](https://github.com/sierrathedog/rda/tree/main/src/CSharp/UnitTests), [Java](https://github.com/sierrathedog/rda/blob/main/src/Java/src/test/java/UniversalDataTransport/UniversalDataFrameworkTests.java), [Python](https://github.com/sierrathedog/rda/blob/main/src/Python/test_rda.py)] from this repo are good places to find further examples of how to use the RDA API.

## More Details 

Here are some articals and thoughts about RDA. (Warning: some of these are currently roughly drafted and begging for improvement. )

- [RDA encoding rules](https://sierrathedog.github.io/rda/rda-encoding-rule)
- [Data type and data structure in RDA](https://sierrathedog.github.io/rda/data-type-and-data-structure)
- [RDA terms and definitions, and more API methods examples](https://sierrathedog.github.io/rda/api-terms-and-definitions)
- [Generic and universal object-serialization](https://sierrathedog.github.io/rda/object-serialization-pattern)
- [RDA tooling and "version-2" formatting](https://sierrathedog.github.io/rda/rda-tooling-and-formatting)
- [Managing data-exchange without using schema](https://sierrathedog.github.io/rda/metadata-vs-schema)
- [Tips for writing a parser/encoder](https://sierrathedog.github.io/rda/parser-development-tips)

## Contributing

We are excited about what can be achieved with RDA, and can't wait to see if this brand new data format can be used in your project and meet your data-exchange needs. 

You can also help us in this project by - 

- Giving us feedback on how you use the API in your project.
- Improving existing code, test cases, and documentation.
- Writing new RDA encoder/parser (e.g. in new languages) for your project, and share!
- Participating in discussions and give your insight.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, please take a look at the [tags on this repository](https://github.com/sierrathedog/rda/tags).

## Authors

* **Michael Chen** - Designing RDA, and the reference parser (in C#) - [sierrathedog](https://github.com/sierrathedog)

* **Samuel Chen** - The Java parser and the Python parser - [samuelfchen](https://github.com/samuelfchen)

You can be a contributor and help this project! Please contact us.

## License 

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 

"Recursive Delimited Array" and "RDA" are trademarks of [Foldda Pty Ltd](https://foldda.com) of Australia.

