# Learning Design Patterns

Design patterns are reusable solution to commonly occurring problems in software design.

Patterns are about reusable designs and interactions of objects.

The gang of Four(GoF) popularize 23 Design Patterns consider the fondation for all other patterns.

Design patterns are categorize has: Creational, Structural, Behavioral, Concurrency, Architectural.

- Design Patterns: represents good practice.
- Anti-Patterns: bad practice. Ex: modify the `Object` class prototype.

Js have multiple Design patterns, they can be Front End, back End or Isomorphic JS (Universal JS).

- [Real World Design Patterns](https://github.com/vahidvdn/realworld-design-patterns/tree/master)

## Creational Design patterns

Creational patterns focus on ways to create objects and instanciate classes.

- Singleton
- Factory Method
- Abstract Factory/Factories
- Builder
- Prototype
- Mixins
- Module

_Reference_

[JavaScript Patterns](http://shop.oreilly.com/product/9780596806767.do)
[JavaScript Design Patterns](https://addyosmani.com/resources/essentialjsdesignpatterns/book/)

### Singleton Pattern

A singleton is an object that can only be instantiated once, while providing a global access point to this instance. It is useful for implementing a global object that can be accessed from anywhere in the application. Example: configuration, database connection.

#### Singleton Pattern in TS

```ts
class Configs {
  static instance: Configs;
  public readonly theme = 'dark';

  // prevent new with private constructor
  private constructor() {}

  static getInstance(): Configs {
    if (!Configs.instance) {
      Configs.instance = new Configs();
    }

    return Configs.instance;
  }
}

const configs = new Configs() // throws error
const configs = Configs.getInstance();
```

#### Singleton Pattern in JS

It differ from static classes as we can delay their initialization, because it may require some information that is not available during the initialization time.

In JS, **Singleton** serve as a shared resource _namespacing_ which isolate code from the global namespace, to provide a single point of access for functions.

One characteristic of the **Singleton** is the _immuability_.

**The old way** using closures and IIFE it is possible to write and Store(Redux).
`UserStore` will be set to the result of the IIFE - an object that exposes 2 functions, but that does not grant direct access to the collection of data.

```js
var UserStore = (function () {
  var _data = [];

  function add(item) {
    _data.push(item);
  }
  function get(id) {
    return _data.find((d) => {
      return d.id === id;
    });
  }
  return {
    add: add,
    get: get,
  };
})();
```

**The ES2015+ way**

```js
const _data = [];

const UserStore = {
  add: item => _data.push(item),
  get: id => _data.find(d => d.id === id)
}

Object.freeze(UserStore)
export default UserStore.
// OR
class UserStoreB {
  constructor(){
    this._data = [];
  }
  add(item) {
    this._data.push(item)
  }
  get(id){
    return this._data.find(d => d.id === id)
  }
}
const instance = new UserStoreB();
Object.freeze(instance);
export default instance;
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

### Factory Method

The **Factory** pattern provide a generic interface for creating objects, where we can specify the type of factory object we wish to be created.

The **Factory** pattern concerned with the notion of creating objects. it doesn't explicitly require us to use a constructor.

**When to use**

- Use the Factory Method when you don’t know beforehand the exact types and dependencies of the objects your code should work with.
- When working with high number of object sharing the same properties.
- Use the Factory Method when you want to save system resources by reusing existing objects instead of rebuilding them each time.

#### Factory Design Pattern in TS

```ts
class IOSButton { }

class AndroidButton { }

// Without Factory
const button1 = os === 'ios' ? new IOSButton() : new AndroidButton()
const button2 = os === 'ios' ? new IOSButton() : new AndroidButton()

// With Factory
class ButtonFactory {
  createButton(os: string): IOSButton | AndroidButton {
    if (os === 'ios') {
      return new IOSButton();
    } else {
      return new AndroidButton();
    }
  }
}

const factory = new ButtonFactory();
const btn1 = factory.createButton(os);
const btn2 = factory.createButton(os);

```

#### Factory Design Pattern in JS

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

```js
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

#### Constructor Design Pattern

Object Constructors are used to create specific types of objects.

**The old way**

```js
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

```js
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

### Abstract Factories

Abstract Factory is a creational design pattern that lets you produce families of related objects without specifying their concrete classes.

```ts
// 1. Define Abstract Product Interfaces
interface Button {
  render(): void;
}

interface Input {
  render(): void;
}

// 2. Create Concrete Products (e.g., Light and Dark theme components)
// Light Theme Products
class LightButton implements Button {
  render() {
    console.log("Rendering a Light Theme Button.");
  }
}

class LightInput implements Input {
  render() {
    console.log("Rendering a Light Theme Input.");
  }
}

// Dark Theme Products
class DarkButton implements Button {
  render() {
    console.log("Rendering a Dark Theme Button.");
  }
}

class DarkInput implements Input {
  render() {
    console.log("Rendering a Dark Theme Input.");
  }
}

// 3. Define the Abstract Factory Interface
interface UIComponentFactory {
  createButton(): Button;
  createInput(): Input;
}

// 4. Implement Concrete Factories
class LightThemeFactory implements UIComponentFactory {
  createButton(): Button {
    return new LightButton();
  }

  createInput(): Input {
    return new LightInput();
  }
}

class DarkThemeFactory implements UIComponentFactory {
  createButton(): Button {
    return new DarkButton();
  }

  createInput(): Input {
    return new DarkInput();
  }
}

// 5. Client Code (uses the factory to create UI components)
function createUI(factory: UIComponentFactory) {
  const button = factory.createButton();
  const input = factory.createInput();

  button.render();
  input.render();
}

// Usage
console.log("Creating Light Theme UI:");
const lightThemeFactory = new LightThemeFactory();
createUI(lightThemeFactory);

console.log("\nCreating Dark Theme UI:");
const darkThemeFactory = new DarkThemeFactory();
createUI(darkThemeFactory);
```

### Builder Design Patterns

Builder Design Pattern lets you construct complex objects step by step. The pattern allows you to produce different types and representations of an object using the same construction code.

```ts
// Product class (the complex object to be built)
class Product {
    private partA: string;
    private partB: string;
    private partC: string;

    constructor() {
        this.partA = '';
        this.partB = '';
        this.partC = '';
    }

    public setPartA(partA: string): void {
        this.partA = partA;
    }

    public setPartB(partB: string): void {
        this.partB = partB;
    }

    public setPartC(partC: string): void {
        this.partC = partC;
    }

    public display(): void {
        console.log(`Product parts: A=${this.partA}, B=${this.partB}, C=${this.partC}`);
    }
}

// Builder interface
interface IProductBuilder {
    buildPartA(value: string): this;
    buildPartB(value: string): this;
    buildPartC(value: string): this;
    getProduct(): Product;
}

// Concrete Builder
class ConcreteProductBuilder implements IProductBuilder {
    private product: Product;

    constructor() {
        this.product = new Product();
    }

    public buildPartA(value: string): this {
        this.product.setPartA(value);
        return this; // Return 'this' for method chaining
    }

    public buildPartB(value: string): this {
        this.product.setPartB(value);
        return this;
    }

    public buildPartC(value: string): this {
        this.product.setPartC(value);
        return this;
    }

    public getProduct(): Product {
        const result = this.product;
        // Reset the builder for future use if needed
        this.product = new Product();
        return result;
    }
}

// Director (optional, for common construction processes)
class Director {
    private builder: IProductBuilder;

    constructor(builder: IProductBuilder) {
        this.builder = builder;
    }

    public constructFullFeaturedProduct(): void {
        this.builder.buildPartA('Feature A')
                    .buildPartB('Feature B')
                    .buildPartC('Feature C');
    }

    public constructSimpleProduct(): void {
        this.builder.buildPartA('Simple A');
    }
}

// Client code
const builder = new ConcreteProductBuilder();

// Using the builder directly
const product1 = builder.buildPartA('Value 1A')
                        .buildPartB('Value 1B')
                        .getProduct();
product1.display(); // Output: Product parts: A=Value 1A, B=Value 1B, C=

// Using the Director
const director = new Director(builder);

director.constructFullFeaturedProduct();
const product2 = builder.getProduct();
product2.display(); // Output: Product parts: A=Feature A, B=Feature B, C=Feature C

director.constructSimpleProduct();
const product3 = builder.getProduct();
product3.display(); // Output: Product parts: A=Simple A, B=, C=
```

### Prototype Pattern

Prototype design pattern lets you copy existing objects without making your code dependent on their classes.

- Use the Prototype pattern when your code shouldn’t depend on the concrete classes of objects that you need to copy.
- Use the pattern when you want to reduce the number of subclasses that only differ in the way they initialize their respective objects.

```ts
// 1. Define the Prototype interface
interface Clonable<T> {
    clone(): T;
}

// 2. Create a Concrete Prototype class
class Document implements Clonable<Document> {
    constructor(public title: string, public content: string[], public version: number) {}

    clone(): Document {
        // Perform a deep copy for mutable properties like arrays
        const clonedContent = this.content.map(item => item);
        return new Document(this.title, clonedContent, this.version);
    }

    display(): void {
        console.log(`Title: ${this.title}`);
        console.log(`Content: ${this.content.join('\n')}`);
        console.log(`Version: ${this.version}`);
    }
}

// 3. Client code using the Prototype
class DocumentManager {
    private prototypes: { [key: string]: Document } = {};

    addPrototype(key: string, document: Document): void {
        this.prototypes[key] = document;
    }

    createDocument(key: string): Document | null {
        const prototype = this.prototypes[key];
        if (prototype) {
            return prototype.clone(); // Clone the prototype to create a new object
        }
        return null;
    }
}

// Usage example
const manager = new DocumentManager();

// Create a template document (prototype)
const contractTemplate = new Document(
    "Contract Template",
    ["Clause 1: Agreement details.", "Clause 2: Terms and conditions."],
    1.0
);
manager.addPrototype("contract", contractTemplate);

// Create a new document by cloning the template
const newContract = manager.createDocument("contract");
if (newContract) {
    newContract.title = "Specific Project Contract";
    newContract.content.push("Clause 3: Specific project requirements."); // Modify the cloned object
    newContract.version = 1.1;
    newContract.display();
}

console.log("\nOriginal Template:");
contractTemplate.display(); // The original prototype remains unchanged
```

### Mixins Pattern

The Mixin design pattern in TypeScript allows for sharing functionality between classes without using traditional inheritance, which can lead to a "diamond problem" or deep inheritance hierarchies. Instead, mixins enable a form of "composition over inheritance."

```ts
// Define a type for a constructor, which is essential for mixins
type Constructor<T = {}> = new (...args: any[]) => T;

// Mixin 1: Adds a 'Loggable' capability
function Loggable<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    log(message: string) {
      console.log(`Log: ${message}`);
    }
  };
}

// Mixin 2: Adds a 'Timestampable' capability
function Timestampable<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    getTimestamp(): string {
      return new Date().toISOString();
    }
  };
}

// Base class
class User {
  constructor(public name: string) {}
}

// Combine the base class with mixins
// The order matters for type inference if methods/properties overlap
class EnhancedUser extends Loggable(Timestampable(User)) {
  constructor(name: string, public email: string) {
    super(name);
  }

  greet() {
    this.log(`Hello, ${this.name}!`);
    console.log(`Current time: ${this.getTimestamp()}`);
  }
}

// Create an instance of the enhanced class
const user = new EnhancedUser("Alice", "alice@example.com");

// Use the mixed-in functionalities
user.greet();
user.log("User created successfully.");
console.log(`Timestamp of creation: ${user.getTimestamp()}`);
```

### Module Pattern

The Module Design Pattern in TypeScript primarily leverages the built-in module system (ES Modules) to encapsulate related code, manage dependencies, and control visibility.

```ts
// mathUtils.ts
export const PI = 3.14159;

export function add(a: number, b: number): number {
    return a + b;
}

export function subtract(a: number, b: number): number {
    return a - b;
}

// Internal helper function, not exported
function multiplyInternal(a: number, b: number): number {
    return a * b;
}

// main.ts
import { PI, add, subtract } from './mathUtils'; // Import specific exports
// import * as MathUtils from './mathUtils'; // Alternative: import all exports as a namespace

console.log(`Value of PI: ${PI}`);

const sum = add(5, 3);
console.log(`Sum: ${sum}`);

const difference = subtract(10, 4);
console.log(`Difference: ${difference}`);

// Attempting to access multiplyInternal will result in a compilation error
// console.log(MathUtils.multiplyInternal(2, 3)); // Error: Property 'multiplyInternal' does not exist
```

## Structural Design Patterns

The structural pattern is concerned with how our classes and objects are composed to form a larger structure in our application.

Structural Design Patterns focus on ways to manage relationships between object to make the application architecture scalable.

- Adapter
- Bridge
- Composite
- Decorator
- Facade
- Flyweight
- Proxy

### Adapter Design Pattern

Adapter is a structural design pattern that allows objects with incompatible interfaces to collaborate.

```ts
// Target Interface: The interface our client code expects
interface PaymentProcessor {
    pay(amount: number): void;
}

// Adaptee: An existing class with an incompatible interface
class PayPalPaymentGateway {
    makePayment(amount: number): void {
        console.log(`Processing payment of $${amount} through PayPal.`);
    }
}

// Adaptee: Another existing class with a different incompatible interface
class StripePaymentService {
    charge(amount: number): void {
        console.log(`Charging $${amount} using Stripe.`);
    }
}

// Adapter: Adapts PayPalPaymentGateway to the PaymentProcessor interface
class PayPalAdapter implements PaymentProcessor {
    private paypalGateway: PayPalPaymentGateway;

    constructor(paypalGateway: PayPalPaymentGateway) {
        this.paypalGateway = paypalGateway;
    }

    pay(amount: number): void {
        this.paypalGateway.makePayment(amount);
    }
}

// Adapter: Adapts StripePaymentService to the PaymentProcessor interface
class StripeAdapter implements PaymentProcessor {
    private stripeService: StripePaymentService;

    constructor(stripeService: StripePaymentService) {
        this.stripeService = stripeService;
    }

    pay(amount: number): void {
        this.stripeService.charge(amount);
    }
}

// Client Code: Uses the Target interface
function processOrder(processor: PaymentProcessor, amount: number): void {
    console.log("Initiating order processing...");
    processor.pay(amount);
    console.log("Order processed successfully.");
}

// Usage
const paypalGateway = new PayPalPaymentGateway();
const paypalAdapter = new PayPalAdapter(paypalGateway);

const stripeService = new StripePaymentService();
const stripeAdapter = new StripeAdapter(stripeService);

console.log("--- Processing with PayPal ---");
processOrder(paypalAdapter, 150);

console.log("\n--- Processing with Stripe ---");
processOrder(stripeAdapter, 200);
```

### Bridge Design Pattern

The Bridge Design Pattern in TypeScript separates an abstraction from its implementation, allowing both to vary independently. This is achieved by creating two distinct hierarchies: Abstraction and Implementation, with a "bridge" connecting them.

```ts
// 1. Implementor Interface: Defines the interface for implementation classes.
interface Color {
  fill(): string;
}

// 2. Concrete Implementations: Implement the Implementor interface.
class Red implements Color {
  fill(): string {
    return "Red";
  }
}

class Blue implements Color {
  fill(): string {
    return "Blue";
  }
}

// 3. Abstraction: Defines the abstract interface for the abstraction classes.
//    It holds a reference to the Implementor.
abstract class Shape {
  protected color: Color;

  constructor(color: Color) {
    this.color = color;
  }

  abstract draw(): string;
}

// 4. Refined Abstractions: Extend the Abstraction and use the Implementor.
class Circle extends Shape {
  constructor(color: Color) {
    super(color);
  }

  draw(): string {
    return `Drawing a Circle in ${this.color.fill()}`;
  }
}

class Square extends Shape {
  constructor(color: Color) {
    super(color);
  }

  draw(): string {
    return `Drawing a Square in ${this.color.fill()}`;
  }
}

// Client Code
const redColor = new Red();
const blueColor = new Blue();

const redCircle = new Circle(redColor);
const blueSquare = new Square(blueColor);

console.log(redCircle.draw()); // Output: Drawing a Circle in Red
console.log(blueSquare.draw()); // Output: Drawing a Square in Blue

const blueCircle = new Circle(blueColor);
console.log(blueCircle.draw()); // Output: Drawing a Circle in Blue
```

### Composite Design Pattern

Composite is a structural design pattern that lets you compose objects into tree structures and then work with these structures as if they were individual objects.

```ts
// Component interface
interface Graphic {
  draw(): void;
}

// Leaf class
class Circle implements Graphic {
  private radius: number;

  constructor(radius: number) {
    this.radius = radius;
  }

  draw(): void {
    console.log(`Drawing a Circle with radius ${this.radius}`);
  }
}

// Leaf class
class Rectangle implements Graphic {
  private width: number;
  private height: number;

  constructor(width: number, height: number) {
    this.width = width;
    this.height = height;
  }

  draw(): void {
    console.log(`Drawing a Rectangle with width ${this.width} and height ${this.height}`);
  }
}

// Composite class
class CompositeGraphic implements Graphic {
  private graphics: Graphic[] = [];
  private name: string;

  constructor(name: string) {
    this.name = name;
  }

  add(graphic: Graphic): void {
    this.graphics.push(graphic);
  }

  remove(graphic: Graphic): void {
    const index = this.graphics.indexOf(graphic);
    if (index > -1) {
      this.graphics.splice(index, 1);
    }
  }

  draw(): void {
    console.log(`Drawing Composite Graphic: ${this.name}`);
    this.graphics.forEach((graphic) => graphic.draw());
  }
}

// Example Usage
const circle1 = new Circle(10);
const rectangle1 = new Rectangle(5, 8);
const circle2 = new Circle(7);

const group1 = new CompositeGraphic("Group 1");
group1.add(circle1);
group1.add(rectangle1);

const mainDrawing = new CompositeGraphic("Main Drawing");
mainDrawing.add(group1);
mainDrawing.add(circle2);

mainDrawing.draw();
```

### Decorator Design Pattern

The Decorator Design Pattern in TypeScript enables the dynamic addition of new behaviors or responsibilities to an object without modifying its core structure. This is achieved by wrapping the original object within a "decorator" object that adds the desired functionality while maintaining the original object's interface.

```ts

// 1. Component Interface
interface Logger {
  log(message: string): void;
}

// 2. Concrete Component
class BasicLogger implements Logger {
  log(message: string): void {
    console.log(message);
  }
}

// 3. Abstract Decorator
abstract class LoggerDecorator implements Logger {
  protected logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  abstract log(message: string): void;
}

// 4. Concrete Decorators
class TimestampLoggerDecorator extends LoggerDecorator {
  log(message: string): void {
    const timestamp = new Date().toISOString();
    this.logger.log(`[${timestamp}] ${message}`);
  }
}

class LevelLoggerDecorator extends LoggerDecorator {
  private level: string;

  constructor(logger: Logger, level: string) {
    super(logger);
    this.level = level;
  }

  log(message: string): void {
    this.logger.log(`[${this.level}] ${message}`);
  }
}

// Usage
const basicLogger = new BasicLogger();
const timestampLogger = new TimestampLoggerDecorator(basicLogger);
const levelTimestampLogger = new LevelLoggerDecorator(timestampLogger, "INFO");

levelTimestampLogger.log("This is a log message.");
// Expected Output: [INFO] [YYYY-MM-DDTHH:MM:SS.sssZ] This is a log message.
```

### Facade Design Pattern

Facade is a structural design pattern that provides a simplified interface to a library, a framework, or any other complex set of classes.

A facade is a class that provides a simplified API for larger body of code. It is often to used to hide low-level details of a subsystem.

```ts
// Subsystem components
class DvdPlayer {
  turnOn(): void {
    console.log("DVD Player: Turning on");
  }

  playMovie(movie: string): void {
    console.log(`DVD Player: Playing movie - ${movie}`);
  }

  turnOff(): void {
    console.log("DVD Player: Turning off");
  }
}

class Projector {
  turnOn(): void {
    console.log("Projector: Turning on");
  }

  setInput(input: string): void {
    console.log(`Projector: Setting input to ${input}`);
  }

  turnOff(): void {
    console.log("Projector: Turning off");
  }
}

class SoundSystem {
  turnOn(): void {
    console.log("Sound System: Turning on");
  }

  setVolume(volume: number): void {
    console.log(`Sound System: Setting volume to ${volume}`);
  }

  turnOff(): void {
    console.log("Sound System: Turning off");
  }
}

// Facade class
class HomeTheaterFacade {
  private dvdPlayer: DvdPlayer;
  private projector: Projector;
  private soundSystem: SoundSystem;

  constructor(dvdPlayer: DvdPlayer, projector: Projector, soundSystem: SoundSystem) {
    this.dvdPlayer = dvdPlayer;
    this.projector = projector;
    this.soundSystem = soundSystem;
  }

  watchMovie(movie: string): void {
    console.log("\nHome Theater: Getting ready to watch a movie...");
    this.dvdPlayer.turnOn();
    this.projector.turnOn();
    this.projector.setInput("DVD");
    this.soundSystem.turnOn();
    this.soundSystem.setVolume(10);
    this.dvdPlayer.playMovie(movie);
  }

  endMovie(): void {
    console.log("\nHome Theater: Shutting down...");
    this.dvdPlayer.turnOff();
    this.projector.turnOff();
    this.soundSystem.turnOff();
  }
}

// Client code
const dvdPlayer = new DvdPlayer();
const projector = new Projector();
const soundSystem = new SoundSystem();

const homeTheater = new HomeTheaterFacade(dvdPlayer, projector, soundSystem);

homeTheater.watchMovie("The Matrix");
homeTheater.endMovie();
```

### Flyweight Design Pattern

Flyweight is a structural design pattern that lets you fit more objects into the available amount of RAM by sharing common parts of state between multiple objects instead of keeping all of the data in each object.

```ts

```

### Proxy Design Pattern

The Proxy Design Pattern provides a surrogate or placeholder for another object to control access to it. This can be used for various purposes, including lazy initialization, access control, logging, or remote object access.

```ts
// Subject interface
interface Image {
    display(): void;
}

// RealSubject: The actual heavy object
class RealImage implements Image {
    private filename: string;

    constructor(filename: string) {
        this.filename = filename;
        this.loadFromDisk(); // Simulate a heavy operation
    }

    private loadFromDisk(): void {
        console.log(`Loading image: ${this.filename}`);
    }

    public display(): void {
        console.log(`Displaying image: ${this.filename}`);
    }
}

// Proxy: The surrogate object
class ProxyImage implements Image {
    private realImage: RealImage | null = null;
    private filename: string;

    constructor(filename: string) {
        this.filename = filename;
    }

    public display(): void {
        if (this.realImage === null) {
            // Lazy initialization: Create RealImage only when needed
            this.realImage = new RealImage(this.filename);
        }
        this.realImage.display();
    }
}

// Client Code
console.log("Creating image objects...");
const image1: Image = new ProxyImage("photo1.jpg");
const image2: Image = new ProxyImage("gallery_pic.png");

console.log("\nFirst display call (image1):");
image1.display(); // RealImage for photo1.jpg is loaded and displayed

console.log("\nSecond display call (image1):");
image1.display(); // RealImage for photo1.jpg is already loaded, only displayed

console.log("\nFirst display call (image2):");
image2.display(); // RealImage for gallery_pic.png is loaded and displayed
```

## Behavioral Design patterns

The behavioral pattern is concerned about how the objects can interact efficiently without being tightly coupled.

Behavioral patterns focus on communication between objets.

- Chain of Responsibility
- Command
- Interpreter
- Iterator
- Mediator
- Memento
- Observer
- Publish/Subscribe
- State
- Strategy
- Template Method
- Visitor

### Chain of Responsibility Design Pattern

The Chain of Responsibility design pattern in TypeScript allows for decoupling the sender of a request from its receiver by creating a chain of objects, each of which can handle the request or pass it to the next object in the chain.

```ts
// 1. Define the Handler interface
interface DispenserHandler {
    setNext(handler: DispenserHandler): DispenserHandler;
    handle(amount: number): void;
}

// 2. Implement an abstract base handler
abstract class AbstractDispenser implements DispenserHandler {
    private nextHandler: DispenserHandler | null = null;

    public setNext(handler: DispenserHandler): DispenserHandler {
        this.nextHandler = handler;
        return handler;
    }

    public handle(amount: number): void {
        if (this.nextHandler) {
            this.nextHandler.handle(amount);
        } else {
            console.log(`Cannot dispense remaining amount: ${amount}`);
        }
    }
}

// 3. Implement concrete handlers for different denominations
class FiftyPoundDispenser extends AbstractDispenser {
    public handle(amount: number): void {
        if (amount >= 50) {
            const numNotes = Math.floor(amount / 50);
            console.log(`Dispensing ${numNotes} x £50 notes.`);
            const remainingAmount = amount % 50;
            if (remainingAmount > 0) {
                super.handle(remainingAmount);
            }
        } else {
            super.handle(amount);
        }
    }
}

class TwentyPoundDispenser extends AbstractDispenser {
    public handle(amount: number): void {
        if (amount >= 20) {
            const numNotes = Math.floor(amount / 20);
            console.log(`Dispensing ${numNotes} x £20 notes.`);
            const remainingAmount = amount % 20;
            if (remainingAmount > 0) {
                super.handle(remainingAmount);
            }
        } else {
            super.handle(amount);
        }
    }
}

class TenPoundDispenser extends AbstractDispenser {
    public handle(amount: number): void {
        if (amount >= 10) {
            const numNotes = Math.floor(amount / 10);
            console.log(`Dispensing ${numNotes} x £10 notes.`);
            const remainingAmount = amount % 10;
            if (remainingAmount > 0) {
                super.handle(remainingAmount);
            }
        } else {
            super.handle(amount);
        }
    }
}

// 4. Client Code
const fiftyPoundDispenser = new FiftyPoundDispenser();
const twentyPoundDispenser = new TwentyPoundDispenser();
const tenPoundDispenser = new TenPoundDispenser();

fiftyPoundDispenser.setNext(twentyPoundDispenser).setNext(tenPoundDispenser);

console.log('Attempting to withdraw £180:');
fiftyPoundDispenser.handle(180); // Should dispense 3x£50, 1x£20, 1x£10

console.log('\nAttempting to withdraw £75:');
fiftyPoundDispenser.handle(75); // Should dispense 1x£50, 1x£20, cannot dispense £5

console.log('\nAttempting to withdraw £5:');
fiftyPoundDispenser.handle(5); // Cannot dispense remaining amount

```

### Command Design Pattern

The Command Design Pattern encapsulates a request as an object, thereby allowing for parameterization of clients with different requests, queuing of requests, and logging of requests. It also supports undoable operations.

```ts
// 1. Command Interface
interface Command {
    execute(): void;
    undo(): void; // Optional: for undoable operations
}

// 2. Receiver: The object that performs the actual actions
class Light {
    turnOn(): void {
        console.log("Light is ON.");
    }

    turnOff(): void {
        console.log("Light is OFF.");
    }
}

// 3. Concrete Commands: Implement the Command interface and bind a Receiver to an action
class LightOnCommand implements Command {
    private light: Light;

    constructor(light: Light) {
        this.light = light;
    }

    execute(): void {
        this.light.turnOn();
    }

    undo(): void {
        this.light.turnOff();
    }
}

class LightOffCommand implements Command {
    private light: Light;

    constructor(light: Light) {
        this.light = light;
    }

    execute(): void {
        this.light.turnOff();
    }

    undo(): void {
        this.light.turnOn();
    }
}

// 4. Invoker: Holds a Command and can execute it
class RemoteControl {
    private command: Command | null = null;
    private history: Command[] = []; // Optional: for undo/redo functionality

    setCommand(command: Command): void {
        this.command = command;
    }

    pressButton(): void {
        if (this.command) {
            this.command.execute();
            this.history.push(this.command); // Add to history for undo
        }
    }

    pressUndo(): void {
        if (this.history.length > 0) {
            const lastCommand = this.history.pop();
            if (lastCommand) {
                lastCommand.undo();
            }
        }
    }
}

// Client Code
const livingRoomLight = new Light();
const remote = new RemoteControl();

// Turn on the light
const lightOn = new LightOnCommand(livingRoomLight);
remote.setCommand(lightOn);
remote.pressButton(); // Output: Light is ON.

// Turn off the light
const lightOff = new LightOffCommand(livingRoomLight);
remote.setCommand(lightOff);
remote.pressButton(); // Output: Light is OFF.

// Undo the last action
remote.pressUndo(); // Output: Light is ON.
```

### Interpreter Design Pattern

The Interpreter design pattern in TypeScript allows for defining a grammatical representation for a language and providing an interpreter to handle that grammar. This pattern is particularly useful for evaluating expressions or commands within a specific domain.

```ts
// 1. Abstract Expression Interface
interface Expression {
    interpret(): number;
}

// 2. Terminal Expressions (Concrete Expressions)
class NumberExpression implements Expression {
    private value: number;

    constructor(value: number) {
        this.value = value;
    }

    interpret(): number {
        return this.value;
    }
}

// 3. Non-Terminal Expressions (Concrete Expressions)
class AddExpression implements Expression {
    private left: Expression;
    private right: Expression;

    constructor(left: Expression, right: Expression) {
        this.left = left;
        this.right = right;
    }

    interpret(): number {
        return this.left.interpret() + this.right.interpret();
    }
}

class SubtractExpression implements Expression {
    private left: Expression;
    private right: Expression;

    constructor(left: Expression, right: Expression) {
        this.left = left;
        this.right = right;
    }

    interpret(): number {
        return this.left.interpret() - this.right.interpret();
    }
}

// 4. Client Usage
const five = new NumberExpression(5);
const ten = new NumberExpression(10);
const two = new NumberExpression(2);

// Build the expression tree: (5 + 10) - 2
const addOperation = new AddExpression(five, ten);
const finalExpression = new SubtractExpression(addOperation, two);

// Interpret the expression
const result = finalExpression.interpret();
console.log(`Result: ${result}`); // Output: Result: 13
```

### Iterator Design Pattern

The Iterator Design Pattern provides a way to access the elements of an aggregate object sequentially without exposing its underlying representation. In TypeScript, this is often achieved by implementing the built-in Iterable and Iterator interfaces.

```ts
// Book class representing an individual item in the collection
class Book {
    constructor(public title: string, public author: string) {}
}

// Bookshelf class implementing the Iterable interface
class Bookshelf implements Iterable<Book> {
    private books: Book[] = [];

    addBook(book: Book): void {
        this.books.push(book);
    }

    // Implementing the Symbol.iterator method to make Bookshelf iterable
    [Symbol.iterator](): Iterator<Book> {
        let index = 0;
        const books = this.books; // Capture 'this.books' for the closure

        return {
            next(): IteratorResult<Book> {
                if (index < books.length) {
                    return { value: books[index++], done: false };
                } else {
                    return { value: undefined, done: true };
                }
            }
        };
    }
}

// Usage of the Bookshelf and its iterator
const myBookshelf = new Bookshelf();
myBookshelf.addBook(new Book("The Lord of the Rings", "J.R.R. Tolkien"));
myBookshelf.addBook(new Book("Pride and Prejudice", "Jane Austen"));
myBookshelf.addBook(new Book("1984", "George Orwell"));

// Using the for...of loop, which leverages the Symbol.iterator
console.log("Books on the shelf:");
for (const book of myBookshelf) {
    console.log(`- ${book.title} by ${book.author}`);
}
```

### Mediator Design Pattern

The Mediator design pattern is a behavioral pattern that reduces coupling between objects by centralizing their communication through a mediator object. This prevents objects from having to directly interact with each other, leading to a more maintainable and flexible system.

```ts
// 1. Mediator Interface
interface ChatMediator {
    registerUser(user: User): void;
    sendMessage(message: string, sender: User): void;
}

// 2. Concrete Mediator
class ChatRoom implements ChatMediator {
    private users: User[] = [];

    registerUser(user: User): void {
        this.users.push(user);
    }

    sendMessage(message: string, sender: User): void {
        this.users.forEach((user) => {
            if (user !== sender) {
                user.receiveMessage(message);
            }
        });
    }
}

// 3. Colleague Interface
interface User {
    name: string;
    mediator: ChatMediator;
    sendMessage(message: string): void;
    receiveMessage(message: string): void;
}

// 4. Concrete Colleague
class ChatUser implements User {
    constructor(public name: string, public mediator: ChatMediator) {
        mediator.registerUser(this); // Register the user with the mediator
    }

    sendMessage(message: string): void {
        console.log(`${this.name} sends: ${message}`);
        this.mediator.sendMessage(message, this);
    }

    receiveMessage(message: string): void {
        console.log(`${this.name} receives: ${message}`);
    }
}

// Client Code
const chatRoom = new ChatRoom();

const user1 = new ChatUser("Alice", chatRoom);
const user2 = new ChatUser("Bob", chatRoom);
const user3 = new ChatUser("Charlie", chatRoom);

user1.sendMessage("Hello everyone!");
user2.sendMessage("Hi Alice!");
user3.sendMessage("Good morning!");
```

### Memento Design Pattern

The Memento design pattern allows capturing and externalizing an object's internal state so that it can be restored later without violating encapsulation.

```ts
// Memento: Stores the internal state of the Originator.
class TextMemento {
    constructor(public readonly text: string) {}
}

// Originator: The object whose state needs to be saved and restored.
class TextEditor {
    private content: string = "";

    public appendText(newText: string): void {
        this.content += newText;
        console.log(`Current content: "${this.content}"`);
    }

    public createMemento(): TextMemento {
        return new TextMemento(this.content);
    }

    public restoreFromMemento(memento: TextMemento): void {
        this.content = memento.text;
        console.log(`Restored content: "${this.content}"`);
    }

    public getCurrentContent(): string {
        return this.content;
    }
}

// Caretaker: Manages the Mementos.
class History {
    private mementos: TextMemento[] = [];

    public save(memento: TextMemento): void {
        this.mementos.push(memento);
    }

    public undo(): TextMemento | undefined {
        if (this.mementos.length > 0) {
            return this.mementos.pop();
        }
        return undefined;
    }

    public getMemento(index: number): TextMemento | undefined {
        if (index >= 0 && index < this.mementos.length) {
            return this.mementos[index];
        }
        return undefined;
    }
}

// Client Code
const editor = new TextEditor();
const history = new History();

editor.appendText("Hello, ");
history.save(editor.createMemento()); // Save "Hello, "

editor.appendText("World!");
history.save(editor.createMemento()); // Save "Hello, World!"

console.log(`Final content: "${editor.getCurrentContent()}"`);

// Undo to previous state
const previousMemento = history.undo();
if (previousMemento) {
    editor.restoreFromMemento(previousMemento); // Restores "Hello, "
}

// Demonstrate restoring to a specific point (e.g., the very first state)
const firstStateMemento = history.getMemento(0);
if (firstStateMemento) {
    editor.restoreFromMemento(firstStateMemento); // Restores "Hello, "
}
```

### Observer Design Pattern

The Observer Design Pattern is a behavioral pattern where a subject maintains a list of its dependents, called observers, and notifies them of any state changes, typically by calling one of their methods. This pattern promotes loose coupling between the subject and its observers.

```ts
// Observer Interface
interface Observer {
  update(productName: string): void;
}

// Subject Interface
interface Subject {
  addObserver(observer: Observer): void;
  removeObserver(observer: Observer): void;
  notifyObservers(): void;
}

// Concrete Subject: Product
class Product implements Subject {
  private observers: Observer[] = [];
  private name: string;
  private inStock: boolean;

  constructor(name: string, inStock: boolean) {
    this.name = name;
    this.inStock = inStock;
  }

  addObserver(observer: Observer): void {
    this.observers.push(observer);
  }

  removeObserver(observer: Observer): void {
    const index = this.observers.indexOf(observer);
    if (index !== -1) {
      this.observers.splice(index, 1);
    }
  }

  notifyObservers(): void {
    for (const observer of this.observers) {
      observer.update(this.name);
    }
  }

  // Method to simulate a state change
  restock(): void {
    this.inStock = true;
    console.log(`${this.name} is now back in stock!`);
    this.notifyObservers(); // Notify all subscribed observers
  }

  getProductName(): string {
    return this.name;
  }
}

// Concrete Observer: Customer
class Customer implements Observer {
  private name: string;

  constructor(name: string) {
    this.name = name;
  }

  update(productName: string): void {
    console.log(`${this.name}: The product "${productName}" you wanted is back in stock!`);
  }
}

// Usage Example
const laptop = new Product("Gaming Laptop", false);

const alice = new Customer("Alice");
const bob = new Customer("Bob");
const charlie = new Customer("Charlie");

// Alice and Bob subscribe to updates for the Gaming Laptop
laptop.addObserver(alice);
laptop.addObserver(bob);

// Simulate the product being restocked
laptop.restock();

// Charlie is not interested in this product, so he doesn't subscribe
// Or, if Bob decides he no longer wants notifications:
laptop.removeObserver(bob);

// Simulate another restock (only Alice will be notified)
console.log("\nSimulating another restock after Bob unsubscribed:");
laptop.restock();
```

### Publish/Subscribe Design Pattern

A common TypeScript example of the Publish/Subscribe (Pub/Sub) design pattern involves creating an EventEmitter class that manages event subscriptions and emissions.

```ts
// Define a type for event callback functions
type EventCallback = (...args: any[]) => void;

class EventEmitter {
  // A record to store event names and their associated callbacks
  private events: Record<string, EventCallback[]>;

  constructor() {
    this.events = {};
  }

  /**
   * Subscribes a callback function to a specific event.
   * @param eventName The name of the event to subscribe to.
   * @param callback The function to be called when the event is emitted.
   */
  public subscribe(eventName: string, callback: EventCallback): void {
    if (!this.events[eventName]) {
      this.events[eventName] = [];
    }
    this.events[eventName].push(callback);
  }

  /**
   * Unsubscribes a specific callback function from an event.
   * @param eventName The name of the event to unsubscribe from.
   * @param callback The specific callback function to remove.
   */
  public unsubscribe(eventName: string, callback: EventCallback): void {
    const eventCallbacks = this.events[eventName];
    if (eventCallbacks) {
      this.events[eventName] = eventCallbacks.filter((cb) => cb !== callback);
    }
  }

  /**
   * Emits an event, triggering all subscribed callbacks for that event.
   * @param eventName The name of the event to emit.
   * @param args Any arguments to pass to the subscribed callbacks.
   */
  public emit(eventName: string, ...args: any[]): void {
    const eventCallbacks = this.events[eventName];
    if (eventCallbacks) {
      eventCallbacks.forEach((callback) => {
        callback(...args);
      });
    }
  }
}

// Example Usage:
const eventEmitter = new EventEmitter();

// Define event handlers (subscribers)
const handler1: EventCallback = (message: string) => {
  console.log(`Handler 1 received: ${message}`);
};

const handler2: EventCallback = (data: number, name: string) => {
  console.log(`Handler 2 received: Data - ${data}, Name - ${name}`);
};

// Subscribe handlers to events
eventEmitter.subscribe('messageReceived', handler1);
eventEmitter.subscribe('dataUpdated', handler2);
eventEmitter.subscribe('messageReceived', (msg: string) => {
  console.log(`Anonymous handler received: ${msg}`);
});

// Emit events (publishers)
console.log("Emitting 'messageReceived' event:");
eventEmitter.emit('messageReceived', 'Hello from the publisher!');

console.log("\nEmitting 'dataUpdated' event:");
eventEmitter.emit('dataUpdated', 123, 'Alice');

// Unsubscribe a handler
eventEmitter.unsubscribe('messageReceived', handler1);

console.log("\nEmitting 'messageReceived' event after unsubscribe:");
eventEmitter.emit('messageReceived', 'Another message!');
```

### State Design Pattern

The State Design Pattern allows an object to alter its behavior when its internal state changes. It appears as if the object has changed its class. This pattern is particularly useful for managing complex state-dependent logic, preventing large conditional statements.

```ts
// 1. State Interface
interface TrafficLightState {
    transitionToGreen(light: TrafficLight): void;
    transitionToYellow(light: TrafficLight): void;
    transitionToRed(light: TrafficLight): void;
    displayState(): void;
}

// 2. Concrete States
class RedLightState implements TrafficLightState {
    transitionToGreen(light: TrafficLight): void {
        console.log("Red Light: Transitioning to Green.");
        light.setState(new GreenLightState());
    }
    transitionToYellow(light: TrafficLight): void {
        console.log("Red Light: Cannot transition directly to Yellow from Red.");
    }
    transitionToRed(light: TrafficLight): void {
        console.log("Red Light: Already in Red state.");
    }
    displayState(): void {
        console.log("Traffic Light is RED.");
    }
}

class GreenLightState implements TrafficLightState {
    transitionToGreen(light: TrafficLight): void {
        console.log("Green Light: Already in Green state.");
    }
    transitionToYellow(light: TrafficLight): void {
        console.log("Green Light: Transitioning to Yellow.");
        light.setState(new YellowLightState());
    }
    transitionToRed(light: TrafficLight): void {
        console.log("Green Light: Cannot transition directly to Red from Green.");
    }
    displayState(): void {
        console.log("Traffic Light is GREEN.");
    }
}

class YellowLightState implements TrafficLightState {
    transitionToGreen(light: TrafficLight): void {
        console.log("Yellow Light: Transitioning to Green.");
        light.setState(new GreenLightState());
    }
    transitionToYellow(light: TrafficLight): void {
        console.log("Yellow Light: Already in Yellow state.");
    }
    transitionToRed(light: TrafficLight): void {
        console.log("Yellow Light: Cannot transition directly to Red from Yellow.");
    }
    displayState(): void {
        console.log("Traffic Light is YELLOW.");
    }
}

// 3. Context
class TrafficLight {
    private currentState: TrafficLightState;

    constructor(initialState: TrafficLightState) {
        this.currentState = initialState;
    }

    public setState(state: TrafficLightState): void {
        this.currentState = state;
    }

    public get currentStateName(): string {
        return this.currentState.constructor.name;
    }

    public goGreen(): void {
        this.currentState.transitionToGreen(this);
    }

    public goYellow(): void {
        this.currentState.transitionToYellow(this);
    }

    public goRed(): void {
        this.currentState.transitionToRed(this);
    }

    public display(): void {
        this.currentState.displayState();
    }
}

// Client Code
const trafficLight = new TrafficLight(new RedLightState());

trafficLight.display();
trafficLight.goGreen();
trafficLight.display();
trafficLight.goYellow();
trafficLight.display();
trafficLight.goRed(); // This will show an invalid transition message as per YellowLightState logic
trafficLight.goGreen(); // This will transition from Yellow to Green
trafficLight.display();
```

### Strategy Design Pattern

The Strategy design pattern in TypeScript allows defining a family of algorithms, encapsulating each one, and making them interchangeable. This pattern enables the algorithm to vary independently from the clients that use it.

```ts
// 1. Define the Strategy Interface
interface PaymentStrategy {
    processPayment(amount: number): void;
}

// 2. Implement Concrete Strategy Classes
class CreditCardStrategy implements PaymentStrategy {
    processPayment(amount: number): void {
        console.log(`Processing credit card payment of $${amount}.`);
        // Add specific credit card payment logic here
    }
}

class PayPalStrategy implements PaymentStrategy {
    processPayment(amount: number): void {
        console.log(`Processing PayPal payment of $${amount}.`);
        // Add specific PayPal payment logic here
    }
}

class BitcoinStrategy implements PaymentStrategy {
    processPayment(amount: number): void {
        console.log(`Processing Bitcoin payment of $${amount}.`);
        // Add specific Bitcoin payment logic here
    }
}

// 3. Create the Context Class
class OnlineStore {
    private paymentStrategy: PaymentStrategy;

    constructor(strategy: PaymentStrategy) {
        this.paymentStrategy = strategy;
    }

    setPaymentStrategy(strategy: PaymentStrategy): void {
        this.paymentStrategy = strategy;
    }

    checkout(amount: number): void {
        console.log("Starting checkout process...");
        this.paymentStrategy.processPayment(amount);
        console.log("Checkout complete.");
    }
}

// 4. Client Usage
const store = new OnlineStore(new CreditCardStrategy());
store.checkout(100); // Uses CreditCardStrategy

store.setPaymentStrategy(new PayPalStrategy());
store.checkout(50); // Switches to PayPalStrategy

store.setPaymentStrategy(new BitcoinStrategy());
store.checkout(200); // Switches to BitcoinStrategy
```

### Template Method Design Pattern

The Template Method design pattern defines the skeleton of an algorithm in a base class, deferring some steps to subclasses. This allows subclasses to redefine certain steps of an algorithm without changing the algorithm's structure.

```ts
// Abstract base class defining the template method
abstract class DataProcessor {
    // The template method that defines the algorithm's skeleton
    public processData(): void {
        this.fetchData();
        this.processFetchedData();
        this.saveData();
    }

    // Abstract methods to be implemented by subclasses
    protected abstract fetchData(): void;
    protected abstract processFetchedData(): void;
    protected abstract saveData(): void;

    // Hook methods (optional, can be overridden by subclasses)
    protected hookBeforeFetch(): void {
        // Default empty implementation
    }

    protected hookAfterSave(): void {
        // Default empty implementation
    }
}

// Concrete subclass for processing CSV data
class CsvDataProcessor extends DataProcessor {
    protected fetchData(): void {
        console.log("Fetching data from CSV file...");
        // Simulate data fetching
    }

    protected processFetchedData(): void {
        console.log("Processing CSV data (e.g., parsing rows and columns)...");
        // Simulate data processing
    }

    protected saveData(): void {
        console.log("Saving processed CSV data to database...");
        // Simulate data saving
    }

    // Optionally override hook method
    protected hookAfterSave(): void {
        console.log("CSV data processing complete and saved.");
    }
}

// Concrete subclass for processing JSON data
class JsonDataProcessor extends DataProcessor {
    protected fetchData(): void {
        console.log("Fetching data from JSON API...");
        // Simulate data fetching
    }

    protected processFetchedData(): void {
        console.log("Processing JSON data (e.g., deserializing objects)...");
        // Simulate data processing
    }

    protected saveData(): void {
        console.log("Saving processed JSON data to cloud storage...");
        // Simulate data saving
    }
}

// Usage
console.log("--- Processing CSV Data ---");
const csvProcessor = new CsvDataProcessor();
csvProcessor.processData();

console.log("\n--- Processing JSON Data ---");
const jsonProcessor = new JsonDataProcessor();
jsonProcessor.processData();
```

### Visitor Design Pattern

The Visitor Design Pattern allows for the separation of algorithms from the objects on which they operate. It enables adding new operations to existing object structures without modifying those structures.

```ts
// 1. Element Interface (Visitable)
interface Shape {
    accept(visitor: ShapeVisitor): void;
}

// 2. Concrete Elements
class Circle implements Shape {
    constructor(public radius: number) {}

    accept(visitor: ShapeVisitor): void {
        visitor.visitCircle(this);
    }
}

class Square implements Shape {
    constructor(public side: number) {}

    accept(visitor: ShapeVisitor): void {
        visitor.visitSquare(this);
    }
}

class Triangle implements Shape {
    constructor(public base: number, public height: number) {}

    accept(visitor: ShapeVisitor): void {
        visitor.visitTriangle(this);
    }
}

// 3. Visitor Interface
interface ShapeVisitor {
    visitCircle(circle: Circle): void;
    visitSquare(square: Square): void;
    visitTriangle(triangle: Triangle): void;
}

// 4. Concrete Visitors
class AreaCalculator implements ShapeVisitor {
    visitCircle(circle: Circle): void {
        const area = Math.PI * circle.radius * circle.radius;
        console.log(`Area of Circle (radius ${circle.radius}): ${area.toFixed(2)}`);
    }

    visitSquare(square: Square): void {
        const area = square.side * square.side;
        console.log(`Area of Square (side ${square.side}): ${area.toFixed(2)}`);
    }

    visitTriangle(triangle: Triangle): void {
        const area = 0.5 * triangle.base * triangle.height;
        console.log(`Area of Triangle (base ${triangle.base}, height ${triangle.height}): ${area.toFixed(2)}`);
    }
}

class PerimeterCalculator implements ShapeVisitor {
    visitCircle(circle: Circle): void {
        const perimeter = 2 * Math.PI * circle.radius;
        console.log(`Perimeter of Circle (radius ${circle.radius}): ${perimeter.toFixed(2)}`);
    }

    visitSquare(square: Square): void {
        const perimeter = 4 * square.side;
        console.log(`Perimeter of Square (side ${square.side}): ${perimeter.toFixed(2)}`);
    }

    visitTriangle(triangle: Triangle): void {
        // For a general triangle, perimeter requires more info (e.g., all sides)
        // This example assumes a simplified case or would need more properties in Triangle
        console.log(`Perimeter of Triangle: Not directly calculable with base/height only.`);
    }
}

// Client Code
const shapes: Shape[] = [
    new Circle(5),
    new Square(4),
    new Triangle(6, 8)
];

const areaCalculator = new AreaCalculator();
const perimeterCalculator = new PerimeterCalculator();

console.log("--- Calculating Areas ---");
shapes.forEach(shape => shape.accept(areaCalculator));

console.log("\n--- Calculating Perimeters ---");
shapes.forEach(shape => shape.accept(perimeterCalculator));
```

### Concurrency Design patterns

These Design patterns deal with multi-threaded programming paradigms.

### Architectural Design patterns

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

- [Design Patterns](https://refactoring.guru/design-patterns/typescript)

- [Design Pattern](https://github.com/ankitech/design-pattern)

- [pluralsight](https://www.pluralsight.com/courses/javascript-practical-design-patterns)

- [joezimjs](https://www.joezimjs.com/javascript/javascript-design-patterns-singleton/)

- [blog post](https://itnext.io/anyway-heres-how-to-do-ajax-api-calls-with-vue-js-e71e57d5cf12)

- [doFactory](https://www.dofactory.com/javascript/design-patterns)

- [Tut plus](https://code.tutsplus.com/tutorials/understanding-design-patterns-in-javascript--net-25930)

- [Scotch.io](https://scotch.io/bar-talk/4-javascript-design-patterns-you-should-know)

- [JS Design Patterns](https://addyosmani.com/resources/essentialjsdesignpatterns/book/)

- [nodeJistsu](https://blog.nodejitsu.com/scaling-isomorphic-javascript-code/)

- [Node.js Design Patterns](https://blog.risingstack.com/fundamental-node-js-design-patterns/)

- [Architecture Patterns](http://pubs.opengroup.org/architecture/togaf8-doc/arch/chap28.html)
