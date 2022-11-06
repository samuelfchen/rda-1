---
layout: post
title: "Objects Serialization Using RDA"
permalink: /object-serialization-pattern
author:
- Michael Chen
---

> By implementing the IRdaSerializable interface, a data object provides application-specific instructions about how its properties need to be stored into an RDA container during object serialization; and to be restored from values in an RDA container during de-serialization.


In this article, we demonstrate how to use RDA to simply and easily implement object-serialization using , by using examples in C#, Java and Python. [^1]
[^1]Rda and IRdaSerializable are defined in the provided source files (for C# these are the "Rda.cs" and the "IRdaSerializable.cs") from the RDA GitHub project repo.

In the C# examples below, the Person class has specified its "FirstName" and "LastName" properties values must be stored inside an RDA during serialization, at pre-defined location indexes RDA_INDEX.FIRST_NAME = 0 and RDA_INDEX.LAST_NAME =1; and during de-serialization, these two properties can be restored at the same locations from an incoming RDA container.

It also demonstrates how to "save and retrieve a person object, to and from a file", using RDA container serialization.

```c#
using UniversalDataTransport;

public class Person : IRdaSerializable
{
    public string FirstName = "John";
    public string LastName = "Smith";

    public enum RDA_INDEX : int 
    { 
        FIRST_NAME = 0, 
        LAST_NAME = 1, 
        RES_ADDRESS = 2, 
        POST_ADDRESS = 3 
    }

    //store the properties of this object into an RDA
    public virtual Rda ToRda()
    {
        var rda = new Rda();  //create an RDA container

        //stores the properties' value, in C# syntax. 
        //It's the same as calling rda.SetValue(index, value)
        rda[(int) RDA_INDEX.FIRST_NAME].ScalarValue = this.FirstName;
        rda[(int)RDA_INDEX.LAST_NAME].ScalarValue = this.LastName;
        return rda;
    }

    //restore the object's properties from an RDA
    public virtual IRdaSerializable FromRda(Rda rda)
    {
        this.FirstName = rda[(int) RDA_INDEX.FIRST_NAME].ScalarValue;
        this.LastName = rda[(int)RDA_INDEX.LAST_NAME].ScalarValue;
        return this;
    }

    //serialize and save this Person object to a file
    public void SaveToFile(string filePath)
    {
        string encodedRdaString = this.ToRda().ToString(); //serialize
        File.WriteAllText(filePath, encodedRdaString);
    }

    //restore a Person object from an RDA string that is stored in a file
    public static Person ReadFromFile(string filePath)
    {
        string encodedRdaString = File.ReadAllText(filePath);
        Rda rda = Rda.Parse(encodedRdaString);
        Person person = new Person();
        person.FromRda(rda);
        return person;
    }
}

```

In the examples below, the Address class has two properties "AddressLines" and "ZIP" need to be serialized using RDA. This is done very similarily as the previous Person class example.

```c#
class Address : IRdaSerializable
{
    public enum RDA_INDEX : int { LINES = 0, ZIP = 1 }

    public string AddressLines = "Line 1\nLine 2\nLine 3";
    public string ZIP = "NY 21540";

    //store the properties into an RDA
    public Rda ToRda()
    {
        var rda = new Rda();  //create an RDA container
         //serialize the properties
        rda[(int)RDA_INDEX.LINES].ScalarValue = this.AddressLines;
        rda[(int)RDA_INDEX.ZIP].ScalarValue = this.ZIP;
        return rda;
    }

    //restore the properties from an RDA
    public IRdaSerializable FromRda(Rda rda)
    {
        this.AddressLines = rda[(int)RDA_INDEX.LINES].ScalarValue;
        this.ZIP = rda[(int)RDA_INDEX.ZIP].ScalarValue;
        return this;
    }
}

```

In the example below, serializing this ComplexPerson class is more interesting. Firstly ComplexPerson class is extended from the Person class, thus inherites the FirstName and the LastName properties that require serialization; secondly it has two non-primary-type Address proterties "ResidentialAddress" and "PostalAddress" which also require serialization. Because both the Person class and the Address class have implemented the IRdaSerializable interface, serializing and deserializing a ComplexPerson object are simple and easy to manage.

```c#
class ComplexPerson : Person
{
    public Address ResidentialAddress = new Address() { AddressLines = "1, 2, 3", ZIP = "12345" };
    public Address PostalAddress = new Address() { AddressLines = "a, b, c", ZIP = "23456" };

    public override Rda ToRda()
    {
        Rda personRda = base.ToRda(); // the result rda contains FirstName and LastName

        //adding the extra "residential address" property (as a child rda) to a new location in the "person" RDA
        //note the ResidentialAddress object specifies how itself can be serialized by implementing the ToRda()
        personRda[(int) RDA_INDEX.RES_ADDRESS] = this.ResidentialAddress.ToRda();

        //now personRda is 2-dimensional
        //Console.Println(personRda[2][1].ScalarValue);   //prints ResidentialAddress.ZIP

        //You can continue to grow the complexity of the Person object.
        //eg storing a further "postal address" RDA to the person RDA, and so on ..
        personRda[(int) RDA_INDEX.POST_ADDRESS] = this.PostalAddress.ToRda();

        return personRda;
    }

    public override IRdaSerializable FromRda(Rda rda)
    {
        //restore the base Person properties
        base.FromRda(rda);  //restores FirstName and LastName

        //sub-RDA structure is passed on to recursively de-serialize sub objects
        this.ResidentialAddress.FromRda(rda[(int) RDA_INDEX.RES_ADDRESS]);
        this.PostalAddress.FromRda(rda[(int) RDA_INDEX.POST_ADDRESS]);
        return this;
    }

    //deserialize a ComplexPerson object 
    public new static ComplexPerson ReadFromFile(string filePath)
    {
        string encodedRdaString = File.ReadAllText(filePath);
        Rda rda = Rda.Parse(encodedRdaString);
        ComplexPerson person = new ComplexPerson();
        person.FromRda(rda);
        return person;
    }
}

```
Note the RDA container serialized from a ComplexPerson object is "compatible" if it is de-serialized into a Person object. So if there are two programs: one requires using the Person class, and the other requires using the ComplexPerson class, using the same RDA container format will maintain backward compatibility.

The following diagram shows the structure and conent of ComplexPerson serialized container -

<img src="image/ComplexPersonRDA.png" align="right" height="400">

## Java Objects Serialization Example

Here are the same examples as the above, but in Java using the provided Java API.

```
import UniversalDataTransport;

class Person implements IRdaSerializable 
{
    public String FirstName="John";
    public String LastName="Smith";

    //store the properties of this object into an RDA
    public Rda ToRda()
    {	 
        var rda = new Rda();  //create an RDA container
        //stores the properties' value
        rda.SetValue(0, this.FirstName);
        rda.SetValue(1, this.LastName;
        return rda;
    }

    //restore the object's properties from an RDA
    public IRdaSerializable FromRda(Rda rda)
    {	 
        this.FirstName = rda.GetValue(0);
        this.LastName = rda.GetValue(1);
        return this;
    }

    //serialize and save this Person object to a file
    public void SaveToFile(string filePath)
    {
        String encodedRdaString= this.ToRda().ToString(); //serialize
        File.WriteAll(filePath, encodedRdaString);
    }	

    //restore a Person object from an RDA string that is stored in a file
    public static Person ReadFromFile(string filePath)
    {
        String encodedRdaString= File.ReadAll(filePath);
        Rda rda =Rda.Parse(encodedRdaString);
        Person person = new Person();
        person.FromRda(rda);
        return person;
    }
}
```

Serializing a simple "Address" class:

```
import UniversalDataTransport;

class Address implements IRdaSerializable 
{
    String AddressLines="Line 1\nLine 2\nLine 3";
    String ZIP="NY 21540";

    //store the properties into an RDA
    Rda ToRda()
    {	 
        var rda = new Rda();  //create an RDA container
        //serialize the properties
        rda.SetValue(0, this.AddressLines);
        rda.SetValue(1, this.ZIP);
        return rda;
    }

    //restore the properties from an RDA
    IRdaSerializable FromRda(Rda rda)
    {	 
        this.AddressLines = rda.GetValue(0);
        this.ZIP = rda.GetValue(1);
        return this;
    }
}
```

Serializing the ComplexPerson class below requires recursively calling the ToRda() of its parent Person class, and its composite proterties which are the Address class. 

```
class ComplexPerson extends Person
{
    Address ResidentialAddress = new Address() {AddressLines="1,2,3", ZIP="12345"};
    Address PostalAddress = new Address() {AddressLines="a,b,c", ZIP="23456"};

    public Rda ToRda()
    {	 
        Rda personRda= base.ToRda();

        //assign the "residential address" RDA to a location in the "person" RDA
        personRda.SetRda(2, this.ResidentialAddress.ToRda());   

        //now personRda is 2-dimensional
        //Console.Println(personRda.GetRda(2).GetValue(1));   
        //prints ResidentialAddress.ZIP

        //You can continue to grow the complexity of the Person object.
        //eg storing a further "postal address" RDA to the person RDA, and so on ..
        personRda.SetRda(3, this.PostalAddress.ToRda());

        Return personRda;
    }

    IRdaSerializable FromRda(Rda rda)
    {	 
        //restore the base Person properties
        base.FromRda(rda);	//restores FirstName and LastName

        //sub-RDA structure is passed on to recursively de-serialize sub objects
        this.ResidentialAddress.FromRda(rda.GetRda(2));
        this.PostalAddress.FromRda(rda.GetRda(3));
        return this;
    }

    //deserialize a ComplexPerson object 
    static ComplexPerson ReadFromFile(string filePath)
    {
        String encodedRdaString= File.ReadAll(filePath);
        Rda rda =Rda.Parse(encodedRdaString);
        ComplexPerson person = new ComplexPerson ();
        person.FromRda(rda);
        return person;
    }
}
```


## Python Objects Serialization Example

The following examples requires includsion of the source files "rda.py" and "i_rda_serializable.py" from this repo in your project.

```python
from enum import Enum
from rda import Rda
from i_rda_serializable import IRdaSerializable


class Person(IRdaSerializable):
    class RDA_INDEX(Enum):
        FIRST_NAME = 0
        LAST_NAME = 1
        RES_ADDRESS = 2
        POST_ADDRESS = 3

    def __init__(self, first_name: str, last_name: str) -> None:
        self.first_name = first_name
        self.last_name = last_name

    # store the properties of this object into an RDA
    def to_rda(self) -> Rda:
        rda = Rda()  # create a RDA container
        # stores the properties' value
        rda[self.RDA_INDEX.FIRST_NAME].set_scalar_value(self.first_name)
        rda[self.RDA_INDEX.LAST_NAME].set_scalar_value(self.last_name)
        return rda

    # restore the object's properties from and RDA
    def from_rda(self, rda: Rda):
        self.first_name = rda[self.RDA_INDEX.FIRST_NAME].get_scalar_value()
        self.last_name = rda[self.RDA_INDEX.LAST_NAME].get_scalar_value()
        return self

    # serialize and save this Person object to a file
    def save_file_to_string(self, file_path: str):
        with open(file_path, "w") as f:
            f.write(self.to_rda().to_string())

    # restore a Person object from an RDA string that is stored in a file
    def read_from_file(file_path: str):
        with open(file_path, "r") as f:
            encoded_rda_string = f.read()
            rda = Rda.parse(encoded_rda_string)
            person = Person()
            person.from_rda(rda)
            return person
```

This example below demonstrates using RDA to (recursively) serialize a complex object.

```python
class Address(IRdaSerializable):
    class RDA_INDEX(Enum):
        LINES = 0
        ZIP = 1

    def __init__(self, address_lines: str, ZIP: str) -> None:
        self.address_lines = address_lines
        self.ZIP = ZIP

    # store the properties into an RDA
    def to_rda(self) -> Rda:
        rda = Rda()
        rda[self.RDA_INDEX.LINES].set_scalar_value(self.address_lines)
        rda[self.RDA_INDEX.ZIP].set_scalar_value(self.ZIP)
        return rda

    # restore the properties from an RDA
    def from_rda(self, rda: Rda):
        self.address_lines = rda[self.RDA_INDEX.LINES].get_scalar_value()
        self.zip = rda[self.RDA_INDEX.ZIP].get_scalar_value()
        return self


class ComplexPerson(Person):
    def __init__(self, residential_address: Address, postal_address: Address) -> None:
        self.residential_address = residential_address
        self.postal_address = postal_address

    def to_rda(self) -> Rda:
        person_rda = super().to_rda()

        # assign the "residential address" RDA To a locaiton in the "person" RDA
        person_rda[self.RDA_INDEX.RES_ADDRESS] = self.residential_address.to_rda()

        # now personRda is 2-dimensional
        # print(person_rda[2][1].get_scalar_value()) # prints residential_address.ZIP

        # You can continue to grow the complexity of the Person object
        # e.g. storing a further "postal address" RDA To the person RDA, and so on...
        person_rda[self.RDA_INDEX.POST_ADDRESS] = self.postal_address.to_rda()

        return person_rda

    def from_rda(self, rda: Rda):
        # restore the base Person properties
        super().from_rda(rda)   # restores first_name and last_name

        # sub-RDA structure is passed on to recursively de-serialize sub objects
        self.residential_address.from_rda(rda[self.RDA_INDEX.RES_ADDRESS])
        self.postal_address.from_rda(rda[self.RDA_INDEX.POST_ADDRESS])
        return self
    
    # deserialize a ComplexPerson object
    def read_from_file(file_path: str) -> ComplexPerson: 
        with open(file_path, "r") as f:
            encoded_rda_string = f.read(file_path)
            rda = Rda.parse(encoded_rda_string)
            person = ComplexPerson()
            person.from_rda(rda)
            return person
```

## Take Away

The above examples have demonstrated -
* RDA container provides a simple and elegant way for flexibly serializing arbitrarily complex data objects.
* Serialized objects stored in RDA container can be exchanged flexibly cross-language and cross-application.
* RDA container allows serialized objects’ data to be maintained backwards compatible with earlier versions. 

