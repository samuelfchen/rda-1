# Recursive Delimited Array 
[![Awesome](https://cdn.jsdelivr.net/gh/sindresorhus/awesome@d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome#readme)

<img src="docs/image/rda_logo.png" align="right" height="128">

Recursive Delimited Array, or RDA, is a text-encoding format for a string-based data container.

Unlike XML and JSON, RDA container is **schema-less** and **application-independent**. The same container can be used for storing any structured data, and for serializing and transporting the data cross-language and cross-platform.

> *An RDA container is like a plain box that has an unlimited number of pockets for freely storing "any stuff", whereas an XML or JSON container is like a wallet, which has specific places for storing coins, notes, and cards.* 

## A Schema-less Data Container

Because schemas are used in XML and JSON to specify the content's data type and data structure, data exchange using XML or JSON containers are therefore restricted to the specified data types and are application-dependent. If an application changes the data format and the schema, all its connected applications need to change their container-parsing logic so the data-exchange remains compatible. This can be especially difficult if the connected applications are developed and maintained by different parties. 

In contrast to XML/JSON, RDA is a container format[^1] designed for building data-exchange pipelines that require both flexibility and easy-to-manage compatibility -

[^1]: Full details of the encoding rules can be found [here](https://sierrathedog.github.io/rda/rda-encoding-rule).

* Instead of using tags or markups, RDA uses a **simple** and **compact** delimited encoding for separating and structuring data elements; 
* Instead of using named paths to navigate a storage "tree", RDA's storage is a multi-dimensional array that uses integer-based indexes for addressing data elements; and 
* RDA container has only two supported data types: RDA or string[^2]. In an RDA container, composite data are converted and stored as RDAs, and scalar data are converted and stored as strings.   
[^2]:RDA data types and data structure are [discussed here](https://sierrathedog.github.io/rda/data-type-and-data-structure). 

Because an RDA container is application independent, it allows "decoupling" the data-transport function from the business-related functions in an application's design, for better flexibility and maintainability. RDA can be particularly beneficial for maintaining compatibility if in a system there are one-to-many, or many-to-many applications connected by data-exchanging pipelines.

## Benefits Of Using RDA
 
One use of RDA is for implementing cross-language and cross-application object-serialization. For example, you can send [a "Person" object as a serialized RDA container](https://sierrathedog.github.io/rda/2022/10/03/obj-serialization-pattern.html) from your Java program to a Python program, and in the Python program, you can de-serialize a "User" object using the received RDA container, because unlike using XML/JSON, the "Person" object and the "User" object aren't necessarily "sharing the same schema" during serialization and de-serialization. 

Another use of RDA is maintaining versioning compatibility between a sender and a receiver. Because of RDA's recursive nature, each "pocket" in an RDA container is itself an RDA container. Multiple "children" RDAs can be placed inside a "parent" RDA, which means you can transfer data of multiple versions and multiple formats "side-by-side" in a single container. 

Indeed, being able to send multiple pieces of "anything" side-by-side in a container brings many interesting uses: how about sending XML data (which is a string) together with its DTD (another string), or sending an encrypted document together with the associated digital signature and public key, or sending a computing "workload" that has some data together with an executable script to a data-processing unit, etc.

Thanks to its simple and efficient delimiter-based encoding, an RDA container is much more compact than an equivilent XML or JSON container, and it is much easier to develop RDA parsers. RDA encoding is also more robust and resilient to data corruption, as it does not have any reserved keyword or character. For example, it allows native line-breaks in the data, whilst in other formats line-breaks are ignored or will cause parsing errors unless that special replacement strings (e.g. "\\n") are used in the encoding.

## Getting Started

This repo provides a simple and super lightweight RDA encoding API. To start, simply include the provided API source code files ([C#](https://github.com/sierrathedog/rda/tree/main/src/CSharp), [Java](https://github.com/sierrathedog/rda/blob/main/src/Java/), and [Python](https://github.com/sierrathedog/rda/blob/main/src/Python)) in your project and start programming using the API methods like in the example below.

* **There is no installation or other dependency required for using the API.** *

### Class *Rda*

All the RDA's encoding and decoding are wrapped in a class called "Rda" in the API. The **Rda class** is intuitively modeled as a "container", which has - 

* **Setter-Getter**  methods are for assigning and retrieving the container's content using index-based addresses, 
* **ToString** method is for RDA-encoding, i.e. serializing the container object and its content into a string, and 
* **Parse** method is for RDA-decoding, i.e. converting an RDA-encoded string back to a Rda container object in a program.

The following example code (in C#[^3]) gives a quick glimpse of how these methods are used - 

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

### Interface *IRdaSerializable*
The **IRdaSerializable interface** from the API is for applications implementing object serialization using RDA, which defines two methods:

* **ToRda()**: produces an RDA container that contains specific properties of the object, for serialization. 

* **FromRda(rda)**: restores the object's specific properties from values in a given RDA container, for de-serialization.

Object serialization using RDA container is explained in-details in [this article](https://sierrathedog.github.io/rda/object-serialization-pattern).

### Test Cases

The unit tests [[C#](https://github.com/sierrathedog/rda/tree/main/src/CSharp/UnitTests), [Java](https://github.com/sierrathedog/rda/blob/main/src/Java/src/test/java/UniversalDataTransport/UniversalDataFrameworkTests.java), [Python](https://github.com/sierrathedog/rda/blob/main/src/Python/test_rda.py)] from this repo are good places to find further examples of how to use the RDA API.

## More Details 

Here are some articles and thoughts about RDA. (Warning: some of these are currently roughly drafted and begging for improvement. )

- [RDA encoding rules](https://sierrathedog.github.io/rda/rda-encoding-rule)
- [Data type and data structure in RDA](https://sierrathedog.github.io/rda/data-type-and-data-structure)
- [RDA terms and definitions, and more API methods examples](https://sierrathedog.github.io/rda/api-terms-and-definitions)
- [Generic and universal object-serialization](https://sierrathedog.github.io/rda/object-serialization-pattern)
- [RDA tooling and "version-2" formatting](https://sierrathedog.github.io/rda/rda-tooling-and-formatting)
- [Managing data exchange without using schema](https://sierrathedog.github.io/rda/metadata-vs-schema)
- [Tips for writing a parser/encoder](https://sierrathedog.github.io/rda/parser-development-tips)

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

