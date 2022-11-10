# Recursive Delimited Array 
[![Awesome](https://cdn.jsdelivr.net/gh/sindresorhus/awesome@d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome#readme)

<img src="docs/image/rda_logo.png" align="right" height="128">

Recursive Delimited Array, or RDA, is an encoding format for storing and transporting structured data in a text string.

Unlike XML and JSON that have their data restricted by a schema that's specific to an application, the RDA format is **schema-less** and for **generic data**. An RDA-encoded string, also known as an "RDA container", can store any data from any application. 

## A Schema-less Data Container

> *An RDA container is like a expandable shelf that provides unlimited space, where you can store "anything", whereas an XML or JSON container is like a wallet, where there are specific places for coins, notes, and cards.* 

When use XML/JSON containers in data exchange between applications, the applications' data must comply with the specified types and structure so it can be stored in the container. If an application requires changing its data format and the schema, all other connected applications will need to change their container-parsing logic to remain compatible, and this can be difficult if the other applications are developed and maintained by different parties.

While RDA is also a text-encoded data format for storing structured data[^1], it is designed to be generic and **application independent**:

[^1]: Full details of the encoding rules can be found [here](https://foldda.github.io/rda/rda-encoding-rule).

* Instead of using tags or markups, RDA uses delimited encoding for separating and structuring data elements; 
* Instead of using named paths, RDA uses integer-based indexes for addressing data elements inside a container; 
* Instead of having multiple, specific data types, RDA has only two generalized data types[^2]: _RDA_ and _string_, for "composite" and "primitive" data values repectively.
 
[^2]:RDA data types and data structure are [discussed here](https://foldda.github.io/rda/data-type-and-data-structure). 

## Benefits Of Using RDA

> *RDA allows implementing a generic and unified data transport layer that applications can utilize for consistently sending and receiving data, so they are "loosely coupled" when require data exchange, and can be separately and flexibly maintained for compatibility.*
 
One powerful feature of RDA is for implementing cross-language and cross-application object-serialization. For example, you can send [a "Person" object as a serialized RDA container](https://foldda.github.io/rda/2022/10/03/obj-serialization-pattern.html) from your Java program to many receivers, and in a Python program, you can de-serialize a "User" object using the received RDA container. Unlike using XML/JSON, the "Person" object and the "User" object are not bound to a schema, so they can be programmed and maintained separately. 

Another use of RDA is maintaining versioning compatibility between a sender and a receiver. Because RDA has a recursive storage structure, you can have "children" RDAs as data elements in a "parent" RDA. It means you can transfer multiple versions and multiple formats of your data (as child RDAs) "side-by-side" in an RDA container, and the receiver can pick the right version and the right format to use. 

Indeed, being able to send multiple pieces of "anything" side-by-side in a container can have many interesting uses: how about sending XML data (which is a string) together with its DTD (another string), or sending an encrypted document together with the associated digital signature and public key, or sending a computing "workload" that has some data together with an executable script to a data-processing unit, etc.

Also, thanks to its simple and efficient delimiter-based encoding, an RDA container is much more compact than a XML or JSON container with the same content, and it is much easier to develop a parser. RDA encoding is also more robust and resilient to data corruption, as it does not have any reserved keyword or character. For example, it allows the data to contain native line-breaks as part of the value, whilst in XML/JSON line-breaks must be replaced with a reserved string (eg "&#xA;") or they will be ignored by the parser.

## Getting Started

> *The RDA API contains only two "pieces" of code, and it has no 3rd party dependency and requires no installation.*

This repo includes the RDA Encoding spec and an RDA-encoding API implemented in [C#](https://github.com/foldda/rda/tree/main/src/CSharp), [Java](https://github.com/foldda/rda/blob/main/src/Java/), and [Python](https://github.com/foldda/rda/blob/main/src/Python). To start, simply include the provided source files in your project and start using the API objects and methods in your program, as explained below.

#### _API "Piece #1": the Rda class_

The _Rda class_ implements both RDA encoding and decoding. It's modeled as a "container" object which provides these methods:

* **Setter-Getter** methods are for assigning and retrieving the container's content using index-based addresses, 
* **ToString** method is for RDA-encoding, i.e. serializing the container object and its content into a string, and 
* **Parse** method is for RDA-decoding, i.e. de-serializing an RDA-encoded string to an RDA container object in a program.

The following code example (in C#[^3]) demonstrates how to use these methods - 

[^3]: Methods of using the Java API and the Python API are very similar.

```c#
using UniversalDataTransport;  //the Rda class is defined in this domain

class RdaDemo
{
    //create an RDA container
    Rda rda1 = new Rda();    

    //SetValue(): store some values into the container
    rda1.SetValue(0, "One");      //store value "One" at index = 0
    rda1.SetValue(1, "Two");
    rda1.SetValue(2, "Three");

    //ToString(): serialize (encode) the container and its content to an RDA formatted string
    System.Console.WriteLine(rda1.ToString());   //print the encoded container string, eg "|\|One|Two|Three"

    //Parse(): de-serialize an RDA formatted string back to an RDA container object 
    Rda rda2 = Rda.Parse(rda1.ToString());   //Parse() method does the reverse of the ToString() method.

    //GetValue(): retrieve a value from in an RDA container at an index location    
    System.Console.WriteLine(rda2.GetValue(2));   //print "Three", the value stored at index=2 in the container.
}
```

#### _API "Piece #2": the IRdaSerializable interface_

The _IRdaSerializable interface_ is for applications to implement object serialization using RDA. It defines two methods:

* **ToRda()**: produces an RDA container that contains specific properties of the object, for serialization. 

* **FromRda(rda)**: restores the object's specific properties from values in a given RDA container, for de-serialization.

The "RDA Method" of object-serialization is discussed in [this article](https://foldda.github.io/rda/object-serialization-pattern).

#### _Test Cases_

The unit tests [[C#](https://github.com/foldda/rda/tree/main/src/CSharp/UnitTests), [Java](https://github.com/foldda/rda/blob/main/src/Java/src/test/java/UniversalDataTransport/UniversalDataFrameworkTests.java), [Python](https://github.com/foldda/rda/blob/main/src/Python/test_rda.py)] from this repo are good places to find further examples of how to use the RDA API.

## More Details 

The following links contain more details and thoughts about RDA. (Warning: some of these are only drafts and due for improvement. )

- [RDA encoding rules](https://foldda.github.io/rda/rda-encoding-rule)
- [Data type and data structure in RDA](https://foldda.github.io/rda/data-type-and-data-structure)
- [RDA terms and definitions, and more API methods examples](https://foldda.github.io/rda/api-terms-and-definitions)
- [Generic and universal object-serialization](https://foldda.github.io/rda/object-serialization-pattern)
- [RDA tooling and "version-2" formatting](https://foldda.github.io/rda/rda-tooling-and-formatting)
- [Managing data exchange without using schema](https://foldda.github.io/rda/metadata-vs-schema)
- [Tips for writing a parser/encoder](https://foldda.github.io/rda/parser-development-tips)

## Contributing

You can help this project by - 

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

"Recursive Delimited Array" and "RDA" are trademarks of [Foldda Pty Ltd](https://foldda.com) - an Australia software company.

