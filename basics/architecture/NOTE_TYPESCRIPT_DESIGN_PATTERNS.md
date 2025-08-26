# Learning JS Design Patterns

Design patterns are reusable solution to commonly occurring problems in software design.
Patterns are about reusable designs and interactions of objects.

The gang of Four (GoF) patterns are generally consider the fondation for all other patterns.
Design Pattern are categorize has: Creational, Structural, Behavioral, Concurrency, Architectural.

- **Design Patterns**: represents good practice.
- **Anti-Patterns**: bad practice. Ex: modify the `Object` class prototype.

Js have multiple design Patterns, they can be Front End, back End or Isomorphic JS (Universal JS).

## Design Pattern

Structural patterns focus on ways to manage relationships between object to make the application architecture scalable.

Behavioral patterns focus on communication between objets.

| Category        | Pattern           | Use Case                                                                 |
|------------------|--------------------|--------------------------------------------------------------------------|
| **Creational**   | Abstract Factory   | Create families of related objects without specifying classes            |
|                  | Builder            | Construct complex objects step-by-step                                   |
|                  | Factory Method     | Create objects without specifying exact class                            |
|                  | Prototype          | Clone objects without coupling to their specific classes                 |
|                  | Singleton          | Ensure a class has only one instance                                     |

| **Structural**   | Adapter            | Convert interface of a class into another expected interface             |
|                  | Composite          | Treat individual and group of objects uniformly                          |
|                  | Decorator          | Add behavior to objects dynamically                                      |
|                  | Facade             | Provide a simplified interface to a subsystem                            |
|                  | Mixins             | Reuse behavior across unrelated classes                                  |
|                  | Module             | Encapsulate code into reusable, self-contained components                |
|                  | Proxy              | Provide surrogate for another object to control access                   |

| **Behavioral**   | Command            | Encapsulate requests as objects                                          |
|                  | Interpreter        | Evaluate language grammar or expression representation                   |
|                  | Iterator           | Access items of a collection sequentially without exposing structure     |
|                  | Mediator           | Centralize communication between objects to reduce direct dependencies   |
|                  | Memento            | Save and restore an object's previous state                              |
|                  | Observer           | Notify multiple objects when state changes                               |
|                  | State              | Alter behavior based on internal state                                   |
|                  | Strategy           | Select algorithm behavior at runtime                                     |
|                  | Template Method    | Define skeleton of an algorithm, defer steps to subclasses               |
|                  | Visitor            | Add new operations without modifying existing structure                  |

| **Publish/Subscribe** | Publish/Subscribe  | Decouple sender and receiver through event broadcasting              |

_Reference_

- [JavaScript Patterns](http://shop.oreilly.com/product/9780596806767.do)
[JavaScript Design Patterns](https://addyosmani.com/resources/essentialjsdesignpatterns/book/)
- [Design Pattern](https://github.com/ankitech/design-pattern)

### Singleton Pattern

**Singleton** is thus know because it restricts instantiation of a class to a single object.
It differ from static classes as we can delay their initialization, because it may require some information that is not available during the initialization time.

In JS, **Singleton** serve as a shared resource _namespacing_ which isolate code from the global namespace, to provide a single point of access for functions.

One characteristic of the **Singleton** is the _immuability_.

**The old way** using closures and IIFE it is possible to write and Store(Redux).
`UserStore` will be set to the result of the IIFE - an object that exposes 2 functions, but that does not grant direct access to the collection of data.

In Typescript Singleton are useful for share resource like database connection, pool, configuration, setting, logger, instance, catching service, external API client.

```ts
class Singleton {
  private static instance: Singleton;

  // Private constructor to prevent instantiation
  private constructor() {}

  // Public method to get the instance of the Singleton
  public static getInstance(): Singleton {
    if (!Singleton.instance) {
      Singleton.instance = new Singleton();
    }
    return Singleton.instance;
  }
}

const singletonInstance1 = Singleton.getInstance();
```

```js
// Basic Singleton
const singleton = {
  attr: 1,
  attr1: 'value'

  method: function() {
    return
  }
}

singleton.attr++;
singleton.method();
```

**JS Namespacing**

Using singleton for namespace/packages allow for better organisation of the code into logical chunks. Using _Namespaces_ moves your code from the global context to the Singleton, leading to fewer accidental overwrites and bugs.

```js
// Object Literal
let Namespace = {
  Util: {
    util_method1: function () {
      return;
    },
    util_method2: function () {
      return;
    },
  },
  Ajax: {
    ajaxCall: function () {
      return data;
    },
  },
  someMethod: function () {},
};
// Referencing the methods
Namespace.Util.util_method1();
Namespace.Ajax.ajaxCall();
Namespace.someMethod();
```

```ts
/* The ES2015+ way */
class Car {
  constructor({ doors, state, color }) {
    this.doors = doors || 4;
    this.state = state || "brand new";
    this.color = color || "silver";
  }
}

class Truck {
  constructor({ state, wheelSize, color }) {
    this.state = state || "used";
    this.wheelSize = wheelSize || "large";
    this.color = color || "blue";
  }
}

class VehicleFactory {
  constructor(vehicleType) {
    this.vehicleClass = Car; // default vehiculeClass
    if (vehicleType === "truck") {
      this.vehicleClass = Truck;
    }
  }

  createVehicle(options) {
    switch (options.vehicleType) {
      case "car":
        this.vehicleClass = Car;
        break;
      case "truck":
        this.vehicleClass = Truck;
        break;
    }
    return new this.vehicleClass(options);
  }
}
// Instantiation
const carFactory = new VehicleFactory();
const car = carFactory.createVehicle({
  vehicleType: "car",
  color: "red",
  doors: 4,
});

console.log(car instanceof Car); // true
```

### Constructor Design Pattern

Object Constructors are used to create specific types of objects.

**The old way**

```ts
var newObject = {};

var newObj = Object.create(Object.prototype);

var newObj = new Object();

// 4 ways to assign keys and values to an object.
// Set properties
newObj.somekey = "Hello World";
// Get properties
var value = newObj.someKey;

// Square Bracket Syntax
newObj["someKey"] = "Hello World";
var val = newObj["someKey"];

// Object.defineProterty
object.defineProterty(newObj, "someKey", {
  value: "someVal",
  writable: true,
  enumerable: true,
  configurable: true,
});
// Or
var defineProp = function (obj, key, value) {
  var config = {
    value: value,
    writable: true,
    enumerable: true,
    configurable: true,
  };
  Object.defineProterty(obj, key, config);
};
// To use,  create a new empty "person" object
var person = Object.create(Object.prototype);

defineProp(perosn, "car", "Delorean");
defineProp(perosn, "dateOfBirth", "1981");

// Object.defineProperties
Object.defineProperties(newObj, {
  someKey: {
    val: "Hello",
    writable: true,
  },
  secondKey: {
    val: "World",
    writable: false,
  },
});

// By prefixing a function with "new" a function can behave like a constructor
function Car(model, year, miles) {
  this.model = model;
  this.year = year;
  this.miles = miles;

  this.toString = function () {
    return this.model + " has done " + this.miles + "miles";
  };
}
var civic = new Car("Honda Civic", 2009, 20000);
console.log(civic.toString());
```

**The ES6+ way**

```ts
class Car {
  constructor({ model, year, miles }) {
    (this.model = model), (this.year = year), (this.miles = miles);
  }
  toString() {
    return `${this.model} has done ${this.miles} miles.`;
  }
}

const jeep = new Car("Jeep", 2009, 20000);
console.log(jeep.toString());
```

### Abstract Factories Pattern

### Prototype Pattern

```ts
interface Prototype<T> {
  clone(): T;
}

abstract class Shape implements Prototype<Shape> {
  constructor(public color: string) {}

  abstract clone(): Shape;
  abstract draw(): void;
}

class Circle extends Shape {
  constructor(public color: string, public radius: number) {
    super(color);
  }

  clone(): Circle {
    return new Circle(this.radius, this.color);
  }

  draw() {
    console.log(`🟠 Circle - Radius: ${this.radius}, Color: ${this.color}`);
  }
}

class Rectangle extends Shape {
  constructor(public color: string, public width: number, public height: number) {
    super(color);
  }

  clone(): Rectangle {
    return new Rectangle(this.width, this.height, this.color);
  }

  draw() {
    console.log(`🟥 Rectangle - Width: ${this.width}, Height: ${this.height}, Color: ${this.color}`);
  }
}

// Client Code
const originalCircle = new Circle(10, "blue");
const clonedCircle = originalCircle.clone();

const originalRect = new Rectangle(20, 15, "red");
const clonedRect = originalRect.clone();

// Usage
originalCircle.draw();  // 🟠 Circle - Radius: 10, Color: blue
clonedCircle.draw();    // 🟠 Circle - Radius: 10, Color: blue

originalRect.draw();    // 🟥 Rectangle - Width: 20, Height: 15, Color: red
clonedRect.draw();      // 🟥 Rectangle - Width: 20, Height: 15, Color: red

console.log(originalCircle === clonedCircle); // false (they're different instances)
```

### Mixins Pattern

### Observer Pattern

### Factory Method Pattern

The **Factory** pattern concerned wit the notion of creating objects. it doesn't explicitly require us to use a constructor. The **Factory** pattern provide a generic interface for creating objects, where we can specify the type of factory object we wish to be created.

**When to use**

- when a object involve a high level of complexity.
- When working with high number of object sharing the same properties
- This is useful for decoupling.

```ts
interface Shape {
  draw(): void;
}

class Circle implements Shape {
  draw(): void {
    console.log("Drawing a Circle 🟠");
  }
}

class Square implements Shape {
  draw(): void {
    console.log("Drawing a Square ⏹️");
  }
}

class Triangle implements Shape {
  draw(): void {
    console.log("Drawing a Triangle 🔺");
  }
}

interface ShapeFactory {
  createShape(): Shape;
}

class CircleFactory implements ShapeFactory {
  createShape(): Shape {
    return new Circle();
  }
}

class SquareFactory implements ShapeFactory {
  createShape(): Shape {
    return new Square();
  }
}

class TriangleFactory implements ShapeFactory {
  createShape(): Shape {
    return new Triangle();
  }
}

function renderShape(factory: ShapeFactory) {
  const shape = factory.createShape();
  shape.draw();
}

renderShape(new CircleFactory());   // Drawing a Circle 🟠
renderShape(new SquareFactory());   // Drawing a Square ⏹️
renderShape(new TriangleFactory()); // Drawing a Triangle 🔺
```

```js
// A constructor to create new Car
function Car( options ){
  this.doors = options.doors || 4;
  this.state = options.state || 'new';
  this.color = options.color || "silver";
}
// A constructor to create new Truck
function Truck( options ){
  this.state = options.state || 'used';
  this.wheelSize = options.wheelSize || 'large';
  this.color = options.color || "blue";
}

function VehicleFactory() {
  VehicleFactory.prototype.vehicleClass = Car;

  VehicleFactory.prototype.createVehicle = function( options ) {
      switch(options.vehicleType) {
        case "car":
          this.vehiculeClass = Car;
          break;
        case "truck":
          this.vehiculeClass = Truck;
          break;
      }
      return new this.vehiculeClass(options)
  }
};
const canFactory = new VehiculeFactory()
const var = carFactory.createVehicule({
  vehiculeType: 'car',
  color: 'red',
  doors: 6
})
// We expect that car is a instance of the vehiculeClass/prototype Car
console.log( car instanceof Car);
```

- Interpreter
- Iterator
- Mediator
- Memento

- Publish/Subscribe
- State
- Strategy
- Template Method
- Visitor

### Concurrency Design Pattern

These Design Pattern deal with multi-threaded programming paradigms.

### Architectural Design Pattern

An **Architectural Pattern** is a general, reusable solution to a commonly occuring problem in software architecture within a given context. Achitectural patterns are similar to software design pattern but have a broader scope.

- Model-View-Controller Pattern
- Model-View-ViewModel Pattern
- Model-View-Presenter Pattern
- Layered Pattern
- Client-Server Pattern
- Master-Slave Pattern
- Pipe-filter Pattern
- Broker Pattern
- Peer-to-peer Pattern
- Event-bus Pattern
- Blackboard Pattern
- Interpreter Pattern

#### Model-View-Controller Pattern (MVC)

Divide the application in 3 parts:

- **Model**: contain the core fonctionality and data
- **View**: display the information to the user
- **Controller**: handle the input from the user

#### Model-View-ViewModel Pattern (MVVM)

Divide the application in 3 parts:

- **Model**: Represents the actual State of the application.
- **View**: Represent the layout and apperance of what a user interact with.
- **ViewModel**: It is a abstraction of the **View** exposing public proterties and commands. MVVM have a binder, which automates communication between the view and its bound properties in the view model.

**MVVM** vs. **MVP** A view directly binds to properties on the viewModel to send and receive updates.

![Vue.js Design Pattern](./img/MVVMPattern.png)

    **View**               **ViewModel**           **Model**        **Lib**
        DOM       <--->         Vue       <---       Vuex   <---     DAL     <---  API
                                          --->              --->             --->

|---------------| App.js Store
| | -Page(Vue-Router)
| | -Layout(mobile,
| | table, desktop)
| | -Smart Comp.
| | -Dumb Comp.
|---------------|

[Architectural pattern](https://towardsdatascience.com/10-common-software-architectural-patterns-in-a-nutshell-a0b47a1e9013)

# Vocabulary

_Namespacing_: is a commonly structured as hierachies to allow reuse of name in different contexts. Ex: naming the file system, organizing variables or functions.

_Duck typing_: The duck test —"If it walks like a duck and it quacks like a duck, then it must be a duck"— to determine if an object can be used for a particular purpose, an object's suitability is determined by the presence of certain methods and properties, rather the type of the object itself.

# References

[pluralsight](https://www.pluralsight.com/courses/javascript-practical-design-patterns)

[joezimjs](https://www.joezimjs.com/javascript/javascript-design-patterns-singleton/)

[blog post](https://itnext.io/anyway-heres-how-to-do-ajax-api-calls-with-vue-js-e71e57d5cf12)

[doFactory](https://www.dofactory.com/javascript/design-patterns)

[Tut plus](https://code.tutsplus.com/tutorials/understanding-design-patterns-in-javascript--net-25930)

[Scotch.io](https://scotch.io/bar-talk/4-javascript-design-patterns-you-should-know)

[JS Design Patterns](https://addyosmani.com/resources/essentialjsdesignpatterns/book/)

[nodeJistsu](https://blog.nodejitsu.com/scaling-isomorphic-javascript-code/)

[Node.js Design Patterns](https://blog.risingstack.com/fundamental-node-js-design-patterns/)

[Architecture Patterns](http://pubs.opengroup.org/architecture/togaf8-doc/arch/chap28.html)
