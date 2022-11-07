# Recursive Delimited Array 
[![Awesome](https://cdn.jsdelivr.net/gh/sindresorhus/awesome@d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome#readme)

<img src="docs/image/rda_logo.png" align="right" height="128">

Recursive Delimited Array, or RDA, is a text-encoding format for a string-based data container.

Unlike XML and JSON, RDA container is **schema-less** and **application-independent**. The same container can be used for storing any structured data, and for serializing and transporting the data cross-language and cross-platform.

> *An RDA container is like a plain box that has an unlimited number of pockets for freely storing "any stuff", whereas an XML or JSON container is like a wallet, which has specific places for storing coins, notes, and cards.* 

## A Schema-less Data Container

With XML or JSON, schemas are used for specifying the data types and the data structure, meaning XML/JSON containers are application specific, as only data with the specified types and structure can fit into a container. If an application changes its data format and requires changing the schema, all other connected applications will need to change their container-parsing logic to remain compatible, and this can be especially difficult if the other applications are developed and maintained by different parties.

RDA is also a container format for structured data, but is specifically designed to be application independent[^1]:

[^1]: Full details of the encoding rules can be found [here](https://foldda.github.io/rda/rda-encoding-rule).

* Instead of using tags or markups, RDA uses delimited encoding for separating and structuring data elements; 
* Instead of using named paths for navigating a data elements "tree", RDA uses integer-based indexes for addressing data elements in its multi-dimensional array storage space; 
* RDA encoding supports only two **generic** data types[^2]: type _RDA_ is for storing "composite" data values, and type _string_ is for storing "scalar/primitive" data values.   
[^2]:RDA data types and data structure are [discussed here](https://foldda.github.io/rda/data-type-and-data-structure). 

Because an RDA container is schema-less and application independent, it allows "decoupling" the data-transport function from the business-related functions in applications' design. Using RDA can provide easy-to-manage flexibility and compatibility to connected but independent applications.

## Benefits Of Using RDA
 
One use of RDA is for implementing cross-language and cross-application object-serialization. For example, you can send [a "Person" object as a serialized RDA container](https://foldda.github.io/rda/2022/10/03/obj-serialization-pattern.html) from your Java program to a Python program, and in the Python program, you can de-serialize a "User" object using the received RDA container, because unlike using XML/JSON, the "Person" object and the "User" object aren't necessarily "sharing the same schema" during serialization and de-serialization. 

Another use of RDA is maintaining versioning compatibility between a sender and a receiver. Because of RDA's recursive nature, each "pocket" in an RDA container is itself an RDA container. Multiple "children" RDAs can be placed inside a "parent" RDA, which means you can transfer data of multiple versions and multiple formats "side-by-side" in a single container. 

Indeed, being able to send multiple pieces of "anything" side-by-side in a container brings many interesting uses: how about sending XML data (which is a string) together with its DTD (another string), or sending an encrypted document together with the associated digital signature and public key, or sending a computing "workload" that has some data together with an executable script to a data-processing unit, etc.

Thanks to its simple and efficient delimiter-based encoding, an RDA container is much more compact than an equivilent XML or JSON container, and it is much easier to develop RDA parsers. RDA encoding is also more robust and resilient to data corruption, as it does not have any reserved keyword or character. For example, it allows native line-breaks in the data, whilst in other formats line-breaks are ignored or will cause parsing errors unless that special replacement strings (e.g. "\\n") are used in the encoding.

## Getting Started

This repo includes the RDA-encoding spec and an RDA encoding API which is implemented in [C#](https://github.com/foldda/rda/tree/main/src/CSharp), [Java](https://github.com/foldda/rda/blob/main/src/Java/), and [Python](https://github.com/foldda/rda/blob/main/src/Python). To start, simply include the provided source files in your project and start using the API methods like in the example below. 

_*** There is no installation or other dependency required. ***_

#### _API Part 1: Class Rda_

The _Rda class_ includes implementation of both RDA encoding and decoding, and is intuitively modeled as a "container". It provides the following methods:

* **Setter-Getter**  methods are for assigning and retrieving the container's content using index-based addresses, 
* **ToString** method is for RDA-encoding, i.e. serializing the container object and its content into a string, and 
* **Parse** method is for RDA-decoding, i.e. converting an RDA-encoded string back to a Rda container object in a program.

The following example (in C#[^3]) gives a glimpse of how (simple) these methods can be used - 

[^3]: Methods of using the Java API and the Python API are very similar.

```c#
using UniversalDataTransport;  //the Rda class is defined in this domain

class RdaDemo
{
    Rda rda1 = new Rda();    //create an RDA container object

    //SetValue(): store a string value at a specific location (by index) in the container
    rda1.SetValue(0, "One");      //store value "One" at index = 0
    rda1.SetValue(1, "Two");
    rda1.SetValue(2, "Three");

    //ToString(): serialize/encode the container and its content to a string
    System.Console.WriteLine(rda1.ToString());   //print the encoded container string, eg "|\|One|Two|Three"

    //Parse(): de-serialize an RDA-encoded string to an RDA container object 
    Rda rda2 = Rda.Parse(rda1.ToString());   //Parse() method does the reverse of the ToString() method.

    //GetValue(): retrieve a value from a given (index) location in an RDA container   
    System.Console.WriteLine(rda2.GetValue(2));   //print "Three", the value stored at index=2 in the container.
}
```

#### _API Part 2: Interface IRdaSerializable_

The _IRdaSerializable interface_ is for applications implementing object serialization using RDA. It defines two methods:

* **ToRda()**: produces an RDA container that contains specific properties of the object, for serialization. 

* **FromRda(rda)**: restores the object's specific properties from values in a given RDA container, for de-serialization.

Object serialization using RDA container is explained in-details in [this article](https://foldda.github.io/rda/object-serialization-pattern).

#### _Test Cases_

The unit tests [[C#](https://github.com/foldda/rda/tree/main/src/CSharp/UnitTests), [Java](https://github.com/foldda/rda/blob/main/src/Java/src/test/java/UniversalDataTransport/UniversalDataFrameworkTests.java), [Python](https://github.com/foldda/rda/blob/main/src/Python/test_rda.py)] from this repo are good places to find further examples of how to use the RDA API.

## More Details 

Here are some articles and thoughts about RDA. (Warning: some of these are currently roughly drafted and begging for improvement. )

- [RDA encoding rules](https://foldda.github.io/rda/rda-encoding-rule)
- [Data type and data structure in RDA](https://foldda.github.io/rda/data-type-and-data-structure)
- [RDA terms and definitions, and more API methods examples](https://foldda.github.io/rda/api-terms-and-definitions)
- [Generic and universal object-serialization](https://foldda.github.io/rda/object-serialization-pattern)
- [RDA tooling and "version-2" formatting](https://foldda.github.io/rda/rda-tooling-and-formatting)
- [Managing data exchange without using schema](https://foldda.github.io/rda/metadata-vs-schema)
- [Tips for writing a parser/encoder](https://foldda.github.io/rda/parser-development-tips)

## Contributing

We are excited about what can be achieved using RDA, and can't wait to see if this brand-new data format can be used in your project and meet your data-exchange needs. 

You can also help us in this project by - 

- Giving us feedback on how you use the API in your project.
- Improving existing code, test cases, and documentation.
- Writing a new RDA encoder/parser (e.g. in a new language) for your project, and share!
- Participating in discussions and giving your insight.

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

