# TypeScript Note

TypeScript is a strongly typed programming language that builds on JavaScript. It was originally designed by Anders Hejlsberg in 2012 and is currently developed and maintained by Microsoft as an open source project.

TypeScript compiles to JavaScript and can be executed in any JavaScript runtime (e.g., a browser or server Node.js).

TypeScript is a language that aims at easing development of large scale applications written in JavaScript. TypeScript is just like ES2015 with type-checking.

- [TS documentation](https://www.typescriptlang.org/docs/)
- [Typescript book](https://gibbok.github.io/typescript-book/book/typescript-introduction/)

## Installation & launch

```ts
npm install -g typescript

// to compile
tsc app.ts
```

The TypeScript compiler has two main responsibilities: checking for type errors and compiling to JavaScript.

## Hello World

```ts
class Student {
  fullName: string;
  constructor(
    public firstName: string,
    public middleInitial: string,
    public lastName: string
  ) {
    this.fullName = `${Person} ${middleInitial} ${lastName}`;
  }
}

interface Person {
  firstName: string;
  lastName: string;
}
// type of the function
function greeter(person: Person): string {
  return `Hello, ${person.firstName} ${person.lastName}`;
}

let user = new Student("Jane", "M.", "User");

document.body.innerHTML = greeter(user);
```

## Primitive Types (Built-in)

| Type      | Code                                                      |
| --------- | --------------------------------------------------------- |
| Any type  | `any` (explicitly untyped)                                |
| String    | `string`                                                  |
| Boolean   | `boolean`                                                 |
| Null      | `null`                                                    |
| Symbol    | `symbol`                                                  |
| Number    | `number`                                                  |
| bigint    | `bigint`                                                  |
| void type | `void` (null or undefined, use for function returns only) |
| Undefined | `undefined`                                               |
| never     | `never`                                                   |
| unknown   | `unknown`                                                 |
| date      | `date`                                                    |
| object    | `object`                                                  |

## Type assertions

Type assertions are a way to tell the compiler “trust me, I know what I’m doing.” A type assertion is like a type cast in other languages, but performs no special checking or restructuring of data.

```ts
let someValue: any = "this is a string";
let strLength: number = (<string>someValue).length;
// OR
let strLength: number = (someValue as string).length;
```

### Type Inference

```ts
var num = 1; // Inference

var num: number = 2; // annotation

function addNumbers(num1: number, num2: number): number {
  return num1 + num2;
}
```

## Ambient Declarations

`declare` is a hint for a compiler that the variable has been created outside the actual file.

`*.d.ts` files include all the types for the corresponding packages.
top of the file // <reference parth ="jquery-1.8.d.ts">

[DefinitelyTyped](https://github.com/DefinitelyTyped/DefinitelyTyped)

```ts
declare var document;

document.title = "Hello";
```

## Function

```ts
const squareItConventional = function (h: number = 10, w: number = 10): number {
  return h * w;
};

const squareItSimplest = (h: number = 10, w: number = 10) => h * w;
```

### Optional parameters

```ts
const squareIt = function (rect: { h: number; w?: number }) {
  if (rect.w === undefined) {
    return rect.h * rect.h;
  }
  return rect.h * rect.w;
};
```

### Defaults parameters

```ts
const squareIt = function (rect: { h: number = 10; w: number = 10 }) {
  return rect.h * rect.w;
};
```

### Functions Overloads

Function overloads in TypeScript allow you to define multiple function signatures for a single function name, enabling you to define functions that can be called in multiple ways.

```ts
// Overloads
function sayHi(name: string): string;
function sayHi(names: string[]): string[];

// Implementation
function sayHi(name: unknown): unknown {
    if (typeof name === 'string') {
        return `Hi, ${name}!`;
    } else if (Array.isArray(name)) {
        return name.map(name => `Hi, ${name}!`);
    }
    throw new Error('Invalid value');
}

sayHi('xx'); // Valid
sayHi(['aa', 'bb']); // Valid
```

### Names types

Interface, Class, Enum

#### Types vs. Interfaces

| Feature                            | `interface`                                   | `type`                                             |
|------------------------------------|-----------------------------------------------|----------------------------------------------------|
| **Basic Syntax**                   | `interface User { name: string }`             | `type User = { name: string }`                     |
| **Extending**                      | `interface A extends B`                       | `type A = B & C`                                   |
| **Implements (Classes)**          | ✅ Yes                                         | ✅ Yes (indirectly, if structurally compatible)     |
| **Declaration Merging**           | ✅ Yes — interfaces can merge                  | ❌ No — duplicate declarations cause errors         |
| **Supports Primitives**           | ❌ No                                          | ✅ Yes (e.g., `type ID = string | number`)          |
| **Supports Tuples / Unions**      | ❌ No                                          | ✅ Yes                                              |
| **Mapped / Conditional Types**    | ❌ Limited support                             | ✅ Full support                                     |
| **Recursive Types**               | ⚠️ Complex                                     | ✅ Supported                                        |
| **Discriminated Unions**          | ⚠️ Verbose and awkward                         | ✅ Natural and expressive                          |
| **Tooling & Intellisense**        | ✅ Better autocomplete in some editors         | ✅ Good, but can be more opaque in complex types    |
| **Preferred For**                 | Objects, Class contracts, public APIs         | Complex types, unions, functional composition      |

## Types

Several built-in utility types can be used to manipulate types.

```ts
type A = Awaited<Promise<string>>; // string

type Person = {
    name: string;
    age: number;
};

type A = Partial<Person>; // { name?: string | undefined; age?: number | undefined; }

type Person = {
    name?: string;
    age?: number;
};

type A = Required<Person>; // { name: string; age: number; }

type Person = {
    name: string;
    age: number;
};

type A = Readonly<Person>;

const a: A = { name: 'Simon', age: 17 };
a.name = 'John'; // Invalid

type Product = {
    name: string;
    price: number;
};

const products: Record<string, Product> = {
    apple: { name: 'Apple', price: 0.5 },
    banana: { name: 'Banana', price: 0.25 },
};

console.log(products.apple); // { name: 'Apple', price: 0.5 }

type MyType = Uppercase<'abc'>; // "ABC"

type MyType = Capitalize<'abc'>; // "Abc"
```

## Types Utilities

In TypeScript, types are used to define the shape of data and enforce type checking.

Type do not support type merging.

```ts
type TypeName = {
    property1: Type1;
    // ...
    method1(arg1: ArgType1, arg2: ArgType2): ReturnType;
    // ...
};
```

### Type intersection

For types, you use the & operator to combine multiple types into a single type (intersection).

```ts
interface A {
    x: string;
    y: number;
}

type B = A & {
    j: string;
};

const c: B = {
    x: 'x',
    y: 123,
    j: 'j',
};

type Department = 'dep-x' | 'dep-y'; // Union

type Person = {
    name: string;
    age: number;
};

type Employee = {
    id: number;
    department: Department;
};

type EmployeeInfo = Person & Employee; // Intersection
```

## Interfaces

Interfaces are used to type-check whether an object fits a certain structure.

Interfaces provide code contract to ensure consistency across objects. The compiler will enforce the contract.

In TypeScript, interfaces define the structure of objects, specifying the names and types of properties or methods that an object must have.

```ts
interface Person {
  firstName: string;
  lastName: string;
}

function greeter(person: Person): void {
  console.log(`Hello, ${person.firstName} ${person.lastName}`);
}

let user = { firstName: "Jane", lastName: "User" };
document.body.innerHTML = greeter(user);
```

### Optional Members

```ts
interface IAutoOptions {
  engine: IEngine;
  basePrice: number;
  make?: string; // ? Optional Member
}
```

## Interface Merging and Extension

`Careful` Merging allows you to combine multiple declarations of the same name into a single definition

```ts
interface X {
    a: string;
}

interface X {
    b: number;
}

const person: X = {
    a: 'a',
    b: 7,
};
```

## Interface Union

```ts
interface A {
    x: 'x';
}
interface B {
    y: 'y';
}

type C = A | B; // Union of interfaces
```

## Class

```ts
class Menu {
  // Our properties:
  // By default they are public, but can also be private or protected.
  items: Array<string>; // The items in the menu, an array of strings.
  private _pages: number; // How many pages will the menu be, a number.

  // A straightforward constructor.
  constructor(item_list: Array<string>, pages: number) {
    // The this keyword is mandatory.
    this.items = item_list;
    this.pages = pages;
  }

  // Methods || Functions
  list(): void {
    console.log("Our menu for today:");
    for (var i = 0; i < this.items.length; i++) {
      console.log(this.items[i]);
    }
  }
  // Properties
  get pages(): number {
    return this._pages;
  }

  set pages(value: number) {
    if (value == undefined) throw `Pages number most be define`;
    this._pages = value;
  }
}

// Create a new instance of the Menu class.
var newMenu = new Menu(["pancakes", "waffles", "orange juice"], 1);

// Call the list method.
newMenu.list();
```

### Class Constructor

Constructors can be marked as private or protected.

Private Constructors: Can be called only within the class itself. Private constructors are often used in scenarios where you want to enforce a singleton pattern or restrict the creation of instances to a factory method within the class.

Protected Constructors: Protected constructors are useful when you want to create a base class that should not be instantiated directly but can be extended by subclasses.

```ts
class BaseClass {
    protected constructor() {}
}

class DerivedClass extends BaseClass {
    private value: number;

    constructor(value: number) {
        super();
        this.value = value;
    }
}

// Attempting to instantiate the base class directly will result in an error
// const baseObj = new BaseClass(); // Error: Constructor of class 'BaseClass' is protected.

// Create an instance of the derived class
const derivedObj = new DerivedClass(10);
```

### Access Modifiers

The private modifier restricts access to the class member only within the containing class.

The protected modifier allows access to the class member within the containing class and its derived classes.

The public modifier provides unrestricted access to the class member, allowing it to be accessed from anywhere.”

### This

In TypeScript, the this keyword refers to the current instance of a class within its methods or constructors. It allows you to access and modify the properties and methods of the class from within its own scope. It provides a way to access and manipulate the internal state of an object within its own methods.

## Classes abstracts

An `abstract` method or `abstract` field is one that hasn't had an implementation provided. There members must exist inside an `abstract` class, which cannot be directly instantiated.

The role of `abstract` classes is to serve as a base class for subclasses which do implement all the `abstract` members. When a class doesn't have any `abstract` members, it is said to be concrete.

### Extending Type

```ts
class ChildClass extends ParentClass {
  constructor() {
    super();
  }
}
```

### Casting Types

```ts
var table: HTMLTableElement = document.createElement(`table`); // failed

var table: HTMLTableElement = <HTMLTableElement>document.createElement(`table`); // Success
```

## Enum, Array, Tuples

```ts
enum Category { Biography, Poetry, Fiction } // 0, 1, 2

enum Category { Biography = 2, Poetry = 0, Fiction = 1 } // 2, 0, 1

const favoriteCategory: Category = Category.Biography;

let strArray1 = string[] = ["here", "are", "strings"];
let strArray2 = Array<string> = ["here", "are", "strings"];
let tuple = any[] = [42, true, "strings"];
```

## Modules

Modules allow for better `Separation` of concerns, `maintainability`, `testing`, `reusable`, they can be implicite or explicite.

Modules are `flexible`, Modules can be extend and Modules are `Open` you can import and export from Modules.

```ts
// explicit module
module dataService {}
// implicit module
class TestClass implements ITest {
  private a = 2;
  b = 4;
}
const testClass = new TestClass();
```

### Asynchronous Module Definition (AMD)

- Manage Dependencies
- Loads them asynchronously

### Namespaces

Namespaces are simply named javaScript object in the global namespace.

## Generics

```ts
interface Box<Type> {
  contents: Type;
}

let box: Box<string>;

// OR
type Box<Type> = {
  contents: Type;
};
```

### Generic functions

```ts
function setContents<Type>(box: Box<Type>, newContents: Type) {
  box.contents = newContents;
}

function firstElement<Type>(arr: Type[]): Type | undefined {
  return arr[0];
}

// s is of type 'string'
const s = firstElement(["a", "b", "c"]);
// n is of type 'number'
const n = firstElement([1, 2, 3]);
// u is of type undefined
const u = firstElement([]);
```

### Generic Classes

```ts
class Container<T> {
    private item: T;

    constructor(item: T) {
        this.item = item;
    }

    getItem(): T {
        return this.item;
    }
}

const numberContainer = new Container<number>(123);
console.log(numberContainer.getItem()); // 123

const stringContainer = new Container<string>('hello');
console.log(stringContainer.getItem()); // hello
```

## declare keyword

The TypeScript `declare` keyword is used to declare variables that may not have originated from a TypeScript file.

## Type Predicates

```ts

const isString = (value: unknown): value is string => typeof value === 'string';

const foo = (bar: unknown) => {
    if (isString(bar)) {
        console.log(bar.toUpperCase());
    } else {
        console.log('not a string');
    }
};
```

## Type Indexing

Type indexing refers to the ability to define types that can be indexed by a key that is not known in advance, using an index signature to specify the type for properties that are not explicitly declared.

```ts
type Dictionary<T> = {
    [key: string]: T;
};
const myDict: Dictionary<string> = { a: 'a', b: 'b' };
console.log(myDict['a']); // Returns a
```

## Predefined Conditional Types

In TypeScript, Predefined Conditional Types are built-in conditional types provided by the language.

```ts
Required<Type>: This type makes all properties in Type required.

Partial<Type>: This type makes all properties in Type optional.

Readonly<Type>: This type makes all properties in Type readonly.
```

## template

```ts

```

## References

[Handbook](https://www.typescriptlang.org/docs/handbook/basic-types.html)

[Reference](https://tutorialzine.com/2016/07/learn-typescript-in-30-minutes)

[Devhints Cheatsheet](https://devhints.io/typescript)
