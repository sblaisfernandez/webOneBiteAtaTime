# Javascript ES6 for Everyone

## Module_1 - New Variables

In JavaScript, variable names (including function names) must be valid identifiers.
An identifier must start with a-z, A-Z, $, or \_. It can then contain any of those characters plus the numerals 0-9.

## Before

var: The scope of var is the enclosing function scope or the global scope.

var: can be update.

```js
var width = 10; // Definition of a variable
var width = 30; // var can be reassign
width = 23; // var can be update

if (true) {
  var result = width * 12; // result will leak out of the {} scope because there is no function
  console.log(`result = ${result}`);
}
```

## New let and const

let and const are block-Scoped, inside the {}

let: can be update, mutable

const: can not be update, mutable

```js
let width = 12;
let width = 34; // error can't be reassign

const height = 12;
const height = 34; // error can't be reassign
height = 356; // error can't be update

if (true) {
  var result = width * 12; // result will not leak out of the {} scope
  console.log(`result = ${result}`);
}
```

- use `const` by default
- use `let` if rebinding is needed
- don't use var

## Module_2 - Function Improvements

## Arrow functions

Arrow functions are anonymous function that don't have it own this, arguments, super, new.target.

[Arrow functions](https://hacks.mozilla.org/2015/06/es6-in-depth-arrow-functions/)

```js
// Implicit return
const arr2 = numbers.map((number) => `${number} arr2`);
console.log(arr2);

// Explicit return
const arr3 = numbers.map((number) => {
  return `${number} arr3`;
});
console.log(arr3);

// No Argument
const arr4 = numbers.map(() => {
  return ` arr4`;
});
console.log(arr4);

// Implicit Object return
const race = `100m Dash`;
const winners = ["seb", "seb1080", "paco"];
// The () of the return
const win = winners.map((winner, i) => ({
  name: winner,
  race: race,
  place: i,
}));
// so cool
console.table(win);
```

### This, arrow functions

#### bind()

ECMAScript6 introduced Function.prototype.bind. Calling f.bind(someObject) creates a new function with the same body and scope as f, but where this occurs in the original function.

```js
function f() {
  return this.a;
}
const g = f.bind({ a: "azerty" });
console.log(g()); // azerty

const h = g.bind({ a: "yoo" }); // bind only works once!
console.log(h()); // azerty
```

In arrow functions, this retains the value of the enclosing lexical context's this.
Arrow functions inherit the 'this' context from the parent context.

Arrow functions don't access the arguments object.

The arrow functions should not be use for :

```js
// To handle click event
  button.# Templating StringaddEventListener('click', function() {
    console.log(this)
    this.classList.toggle('on')
  })

// Don't use () => {} to bind to an object
  const person = {
    points: 23,
    score() {
      console.log(this) // this don't work because this reference to the window()
      this.points++
    }
  }

  // Don't use () => {} has a constructor
  class Car {
    constructor(make, color) {
      this.make = make
      this.color = color
    }
  }
  // () => {} can be use to add a method to a class
  Car.prototype.summarize = function() {
    return `This car is a ${this.make} in the color ${this.color}`
  }

  // Arrow functions don't access the arguments object.
  const orderChildren = function() {
    const children = Array.from(arguments)
    return children.map((child, i) => {
      return `${child} was child #${i + 1}`
    })
    console.log(arguments)
  }
  // not working
  const orderChildren2 = () => {
    const children = Array.from(arguments)
    return children.map((child, i) => {
      return `${child} was child #${i + 1}`
    })
    console.log(arguments)
  }
```

### Default argument

```js
function calculateBill(total, tax = 0.13, tip = 0.15) {
  return total * tax + total * tip;
}
```

## Module_3 - Templating String

```js
const string = `string`;

const temString = ` template ${string}
                    are awesome`;
// Template string is great for formatting HTML markup
const dogs = [
  { name: "Snickers", age: 2 },
  { name: "Hugo", age: 8 },
  { name: "Croby", age: 6 },
  { name: "Snopy" },
];

const markup = `<ul class="dogs">
    ${dogs
      .map(
        (dog) =>
          `<li>${dog.name}

    ${dog.age ? `is ${dog.name} year old` : "have no age"}
    </li>`
      )
      .join("")}
  </ul>`;
document.body.innerHTML = markup;
```

### Tagging Template string

```js
function tagging(strings, ...values) {
  let str = ``;
  strings.forEach((string, i) => {
    str += `${string} <span contenteditable class="h1">
            ${values[i] || ""}
            </>`;
  });
  return str;
}
const name = `Ludo`,
  age = 8;
const sentence = tagging`My dog's name is ${name} and he is ${age} year old`;
document.body.innerHTML = sentence;
```

## Module_4 - Additional String Improvements

```js
const str = `newString`;

str.startsWith("new"); // true

str.endsWith("ing"); // true

str.includes("Str"); // true

str.repeat(3); // newStringnewStringnewString
```

## Module_5 - Destructuring

Destructuring allow to extract properties, key from a object, map, set into a variable.

## Destructuring Object

```js
const object = {
  prop1: "Seb",
  prop2: "Blais",
};

const { prop1, prop2 } = object; // Deconstruction

const seb = {
  first: "Seb",
  last: "Blais",
  links: {
    social: {
      twitter: "https://twitter.com/seb",
      facebook: "https://facebook.com/seb.developer",
    },
    web: {
      blog: "https://seb.com",
    },
  },
};

// rename facebook for fb
const { twitter, facebook: fb } = seb.links.social;

// Create a object
const settings = {
  width: 300,
  color: "black",
};

// Set default value if the settings object don't have the prop
const { width = 100, height = 100, color = "blue", fontSize = 25 } = settings;

// Object Destructuring with variable renaming & default values
const { w: width = 400, h: height = 500 } = { w: 800 };
```

## Destructuring Array

```js
const arr = ["Seb Blais", 233223, "seb.com"];

const [name, id, website] = arr; // Destructuring Array

const data = "aaaaaaaaaa,bbbbbbbbb,cccccccc,ddd";

const [a, b, c, d] = data.split(","); // Deconstruct string into a Array

const team = ["Seb", "Marco", "Mick", "Gab", "Frank"];

const [captain, assistant, ...marins] = team; // Rest Operator
```

## Swapping variables

```js
let var1 = "variable1",
  var2 = ("variable1"[(var1, var2)] = [var2, var1]); // Swapping variables
```

## Ignoring values

Get the first value and the last value.

```js
function f() {
  return [1, 2, 3];
}
let [a, , b] = f();
```

## Destructuring Functions

```js
function tipCalculator({ total = 100, tip = 0.15, tax = 0.13 } = {}) {
  return total + tip * total + tax * total;
}

// Arguments can be pass in a different order
const bill = tipCalculator({ tip: 0.2, total: 200 });
```

## Module_6 Iterables & Looping

## Existing Looping in js

```js
const cuts = ['Chuck', 'Brisket', 'Shank', 'Short Rib']

// ES5 Confusing syntax
for(let i = 0; i < cuts.length; i++){
  console.log(cuts[i])
}
// Can't be abord the loop, can't use the break keyword
cuts.forEach( cut => console.log(cut))

// loop over the prototype, iterate by the index of the array
for(const cut in cuts) {
  console.log(cuts[cut])
}
// New ES6 for looping, iterate by the value of the array
for(const cut of cuts){
  // can be break
  if(cut === 'Brisket') {
    continue
  }
  console.log(cut)
}

// .entries() return a [key, value]
for(const cut of cuts){
  // cut can be deconstruction into a array
  if(const [i ,cut] of cuts.entries()) {
    console.log(` ${} is the ${i + 1}`)
  }
}
```

## Module_7 - An Array of Array Improvements

```js
// Array.from()
const nodeList = document.querySelectorAll('.items p')
const itemsArray = Array.from(nodeList, item => {
  return item.textContent. // map() can by pass a arg. to .from()
})

//Array.of()
const str = `item1,item2,item3,item4,item5`
const newArr = Array.of(str.split(','))

// Array.find()
const posts = [
  {
    "code":"BAcyDyQwcXX",
    "caption":"Lunch #hamont",
    "likes":56,
    "id":"1161022966406956503"
  },
  {
    "code":"BAcJeJrQca9",
    "caption":"Snow! ⛄️🌨❄️ #lifewithsnickers",
    "likes":59,
    "id":"1160844458347054781",
  },
  {
    "code":"BAF_KY4wcRY",
    "caption":"Cleaned my office and mounted my recording gear overhead. Stoked for 2016!",
    "likes":79,
    "id":"1154606670337393752",
  }
]

const post  = posts.find(p => ( p.code === `BAF_KY4wcRY`))

//Array.findIndex(), return the first index of the element that respect the function condition
const postIndex = posts.findIndex( p => p.likes > 57 )

// Array.some()
const ages = [12,11,13,19]

let major = ages.some(age => (age >= 18) ) // true
let allMajor = ages.every(age => (age >= 18) ) // false
```

## Module_8 - ...Spread Syntax And ...Rest parameters

...Spread syntax allows an iterable to be expendanded where zero or more arguments are expected. It will apply a array as a individual elements.

## ...Spread in Array literal

```js
const featured = ["Deep Dish", "Pepperoni", "Hawaiian"];
const specialty = ["Meatzza", "Spicy Mama", "Margherita"];
const friends = ["friend1", "friend2", "friend3"];

const pizzas = [...featured, "veg", ...specialty];
const fridayPizzas = [...pizzas];

const partyMixt = [...featured, ...firends, ...specialty];

const people = Array.from("nodeList"); // Convert arrayList into array

const deepDish = {
  pizzaName: "Deep Dish",
  size: "Medium",
  ingredients: ["Marinara", "Italian Sausage", "Dough", "Cheese"],
};

const arr = ["Milk", "Flour", ...deepDish.ingredients];
// Create a new Array 'arr' not the reference to deepDish.ingredients
```

## The ...Rest Params

The ...Rest parameter allows us to represent an indefinite number of arguments as an array.

```js
// take amounts has a array
function calCurrency(rate, ...amounts) {
  return amounts.map((amount) => amount * rate);
}
```

## Module_9 Object Literal Upgrades

Object can be initialized using New Object(), Object.create(), or Literal notation.
Objects consist of properties, witch are used to describe an object. Values of object properties can either contain primitive data types or other objects.

```js
const fName = 'Seb', lName = 'Blais', age = 11, job = `Web Dev`

const person = { fName, lName, age, job } // Object Literal,
// don't need to specify the name of the property

const me = Object.create(person)

console.log(person)
const modal = {
  create() {  // same as create: function() {}
  },
  open: function() {}
}

const key = 'superLongPropertyName'
const value = {}
const tShirt = {
  // Computed property names
  [key]: `value`,
  [`${key}constructor`]: function() {},
  [`${key}update`]: value
}
// or bind the key/value pair out side of the Object definition
const pants = {}
pants[key]: value

const keys = ['size', 'color', 'weight']
const values = ['medium', 'grey', 70]

const shirt = {
  [keys.shift()]: values.shift(),
  [keys.shift()]: values.shift(),
  [keys.shift()]: values.shift(),
}
```

## Module_10 - Promises

The Promises object represents the eventual completion (or failure) of an asynchronous operation, and its resulting value.

A Promise will return a value between now and the end of time.

A Promise can have 3 States:

- Pending: Initial state, neither fulfilled or rejected.
- Fulfilled: Operation completed successfully.
- Rejected: Operation failed.

A pending Promise can either be fulfilled with a return value, or rejected with a reason (Error).

JS is a single threaded, bits of scripts can't run at the same time, they have to run one after another. JS share a thread in the browser with the same queue as painting, updating styles and event handling. One of the activities will delay the others one.

Asynchronous: In programming, asynchronous events are those occurring independently of the main program flow.

```js
// Fetching data using fetch that implement a Promise
const MTL_WIFI_URL = `http://donnees.ville.montreal.qc.ca/dataset/08f12925-c6b2-405f-bd01-744674d97bff/resource/11860f23-30c9-4221-ae00-a39af4684210/download/mtlwifi_bornes.geojson`;

const response = fetch(MTL_WIFI_URL)
  .then((data) => data.json()) // convert into desired format
  .then((data) => {
    console.log(data);
  })
  .catch((err) => {
    console.error(err);
  });
```

Build my own Promises

```js
const p = new Promise((resolve, reject) => {
  // resolve(`Seb is Cool`)
  setTimeout(() => {
    reject(Error(`Err Seb is not that Cool`));
  }, 1000);
});

p.then((data) => {
  console.log(data);
}).catch((err) => {
  console.error(err);
});
```

Promise.all(iterable) method returns a single Promise that resolve when all of the promises in the iterable argument have resolved or when the iterable argument contains no promises.

```js
const p1 = new Promise((resolve) => {
  setTimeout(() => {
    resolve({ temp: 20, location: `Montreal` });
  }, 2000);
});
const p2 = new Promise((resolve) => {
  setTimeout(() => {
    resolve({ text: `What a nice day`, location: `Montreal` });
  }, 500);
});

Promise.all([p1, p2]).then((responses) => {
  const [weather, tweet] = responses;
  console.log(`responses : `, weather, responses, tweet);
});
```

## Module_11 - Symbol

Symbol is a built-in object whose constructor returns a symbol primitive — also called a Symbol value or just a Symbol — that's guaranteed to be unique.

A symbol value may be used as an identifier, but symbol are not enumerable it is not possible to loop over them.
Every symbol value returned from Symbol() is unique.

Actual data type: Number, String, Object, boolean, Null, undefined and new ES6 Symbol.

```js
const sym1 = Symbol();
const sym2 = Symbol(2);
const symStr = Symbol("foo"); // the param is a Descriptor

const classRoom = {
  [Symbol(`Frederik`)]: { grade: 100, gender: `male` },
  [Symbol(`Frederik`)]: { grade: 78, gender: `female` },
};

const symbols = Object.getOwnPropertySymbols(classRoom);
console.log(symbols);

// Display the values sof the ClassRoom
const data = symbols.map((sym) => classRoom[sym]);

console.log(data);
```

## Module_12 - Code Quality with EsLint

Use EsLint

## Module_13 - Javascript Modules and using npm

A Javascript code module is simply some JS code located in a registered location.

The export statement allow to export functions, objects, primitive values, from a module.

```js
// file config.js
export const CONSTANT = 234242
export const str = `sfsdfsdfdsfsdf`
export newFunc function() { return true }
```

The import statement allow to import bindings which are exported by another module.

```js
// app.js
import { _ } from "lodash";
import insane from "insane";

import { apiKey as key, old, dog } from "./src/config";
```

# Module_14 - ES6 Tooling

## Webpack

Webpack is a static module bundler for modern JavaScript applications.

[System.js](https://github.com/systemjs/systemjs) is a great lib that allow you
to config module loader dynamicaly ES module worflows in the browsers and NodeJS.
Really handy for prototyping, don't use for production.

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>System JS</title>
  </head>
  <body>
    <h1>Browser-sync is a create Tool</h1>
    <script src="https://jspm.io/system@0.19.js"></script>
    <script>
      System.config({ transpiler: "babel" });
      System.import("./main.js");
    </script>
  </body>
</html>
```

```js
// main.js
import { sum, kebabCase } from "npm:lodash";
import { calculTip } from "./customModule";

console.log(kebabCase("Seb is becoming a better Web Dev"));
const amount = 14;
const taxRate = 0.13;
document.write(calculTip(amount, taxRate));
```

```js
// customModule.js
export function calculTip(amount, taxRate) {
  return amount + amount * taxRate;
}
```

### Babel

Babel is a JS compiler, it has 3 stages that it runs code in: parsing, transforming, and generation.

Babel use JS plugins to convert the latest and greatest version of ES into older browser supported JS. A preset is a collection of plugin.

### Polyfill

## Module_15 - Classes

Review the pre ES2015 syntax for prototype.based Object. The body of a class is executed in strict mode.

Class declaration are not hoisted.

```js
class Rectangle {
  constructor(height, width) {
    this.height = height;
    this.width = width;
  }
}
```

Class expressions are not hoisted, class expressions can be named or unnamed.

```js
// unnamed class
let Rectangle = class {
  constructor(height, width) {
    this.height = height;
    this.width = width;
  }
};
console.log(Rectangle.name); // output: "Rectangle"

// named class
let Rectangle = class Rectangle2 {
  constructor(height, width) {
    this.height = height;
    this.width = width;
  }
};
console.log(Rectangle.name); // output: "Rectangle2"
```

```js
// Building a Dog prototype
function Dog(name, breed) {
  this.name = name;
  this.breed = breed;
}
// Adding methods to Dog
Dog.prototype.bark = function () {
  console.log(`Bark Bark! My name is ${this.name}`);
};
// Declaring a instance of Dog
const snoopy = new Dog("snoopy", "King Charles");
```

ES6 JS Classes are syntactical sugar over prototype-based inheritance.

```js
class Dog {
  constructor(name, breed) {
    this.name = name;
    this.breed = breed;
  }
  bark() {
    console.log(`Bark Bark! My name is ${this.name}`);
  }
  // Static methods calls are made directly on the
  // class and are not callable on instances of the class.
  static info() {
    console.log(`A dog is better than a cat by 10 times`);
  }
  // computed property
  get description() {
    return `${this.name} is a ${this.breed}`;
  }
  set nicknames(value) {
    this.nick = value.trim();
  }
  get nicknames() {
    return this.nick.toUpperCase();
  }
}
```

Static method calls are made directly on the class and not callable on
instance of the class. Static methods are often used to create utilities functions.

Extending a Class into a new Class

```js
class Animal {
  constructor(name) {
    this.name = name;
    this.thirst = 100;
    this.belly = [];
  }
  drink() {
    this.thirst -= 10;
    return this.thirst;
  }
  eat(food) {
    this.belly.push(food);
    return this.belly;
  }
}
class Dog extends Animal {
  constructor(name, breed) {
    super(name); // Call the parent Class first
    this.breed = breed;
  }
  bark() {
    console.log("Bark bark I'm a dog");
  }
}
```

Extending the Array Object

The `arguments` object is a local variable within non-arrow functions.

[Functions arguments](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/arguments)

```js
class MovieCollection extends Array {
  constructor(name, ...items) {
    super(...items); // Same thing as calling new Array(...items)
    this.name = name;
  }
  add(movie) {
    this.push(movie);
  }
  topRated(limit = 10) {
    return this.sort((a, b) => (a.stars > b.stars ? -1 : 1)).slice(0, limit);
  }
}
const movies = new MovieCollection(
  "Wes's Fav Movies",
  { name: "Bee Movie", stars: 10 },
  { name: "Star Wars Trek", stars: 1 },
  { name: "Virgin Suicides", stars: 7 },
  { name: "King of the Road", stars: 8 }
);
```

## Module_16 - Generators

The Generator object is returned by a generator function and it conforms to both the iterable protocol and the iterator protocol.

```js
const inventors = [
  { first: "Albert", last: "Einstein", year: 1879 },
  { first: "Isaac", last: "Newton", year: 1643 },
  { first: "Galileo", last: "Galilei", year: 1564 },
  { first: "Marie", last: "Curie", year: 1867 },
  { first: "Johannes", last: "Kepler", year: 1571 },
  { first: "Nicolaus", last: "Copernicus", year: 1473 },
  { first: "Max", last: "Planck", year: 1858 },
];

function* loop(arr) {
  console.log(inventors);
  for (const item of arr) {
    yield item; // act has a return statement
  }
}
const inventorGen = loop(inventors);
inventorGen.next().value; // to be call
```

Generator can be useful for multi fetching calls.

```js
function ajax(url) {
  fetch(url)
    .then((data) => data.json())
    .then((data) => dataGen.next(data));
}

function* steps() {
  console.log("fetching beers");
  const beers = yield ajax("http://api.react.beer/v2/search?q=hops&type=beer");
  console.log(beers);

  console.log("fetching wes");
  const wes = yield ajax("https://api.github.com/users/wesbos");
  console.log(wes);

  console.log("fetching fat joe");
  const fatJoe = yield ajax("https://api.discogs.com/artists/51988");
  console.log(fatJoe);
}

const dataGen = steps();
dataGen.next(); // kick it off
```

## Module_17 - Proxies

The Proxy object is used to define custom behavior for fundamental operations.
Proxy allow to overwrite default behavior of default Object.

```js
const person = { name: `Seb`, age: 99 };
const personProxy = new Proxy(person, {});
```

## Module_18 - Set and WeakSet

The Set object lets you store unique values of any type, whether primitive values or object references.

In a Set the key and the value are the exact same thing.
All the key-value in a Set are unique.

You can iterate through the elements of a set in insertion order.

```js
const group = new Set();

group.add("Seb");
group.add("Natasha");
group.add("Niki");

group.values(); // will return a SetIterator {}
```

WeakSet is a collection of garbage-collectable values, including objects and non-registered symbols. A value in the WeakSet may only occur once. It is unique in the WeakSet's collection.

The WeakSet contain only Objects, there is not iterable on a WeakSet. The WeakSet don't have a clear() method, because the Weakset clean it self up.

```js
let dog1 = { name: `snoopy`, age: 3 };
let dog2 = { name: `doggy`, age: 1 };

const weakSauce = new WeakSet([dog1, dog2]);
```

## Module_19 - Map and WeakMap

The Map object holds key-value pairs and remembers the original insertion order of the keys. Any JS types (both objects and primitives values) may abe used as either a key of a value.

The advantage of a Map() over a regular Object is that the map key can be all type of data structure.

```js
const dogs = new Map();

dogs.set(`snoopy`, 3);
dogs.set(`Summy`, 2);
dogs.set(`Hugo`, 6);
```

WeakMap object is a collection of key/value pairs in which the keys are weakly referenced.
The keys must be objects or non-reference Symbol and the values can any JS types.

WeakMap do not have a size.

```js
let dog1 = { name: "Snickers", age: 3 };
let dog2 = { name: "sunny", age: 1 };

const weakSauce = new WeakSet([dog1, dog2]);

console.log(weakSauce);
dog1 = null;
console.log(weakSauce);
```

## Module_20 - Async + Await Flow Control

The async function declaration defines an asynchronous function, which returns an AsyncFunction object.

```js
function resolveAfterSec(nbSec) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve("resolved");
    }, nbSec * 1000);
  });
}
async function asyncCall() {
  const nbSec = 10; // sec
  const result = await resolveAfterSec(nbSec);
  console.log(result);
}
asyncCall();
```

Promisify of a Call Back

```js
navigator.geolocation.getCurrentPosition(
  function (pos) {
    console.log("it worked!");
    console.log(pos);
  },
  function (err) {
    console.log("it failed!");
    console.log(err);
  }
);

function getCurrentPosition(...args) {
  return new Promise((resolve, reject) => {
    navigator.geolocation.getCurrentPosition(...args, resolve, reject);
  });
}

async function go() {
  console.log("starting");
  const pos = await getCurrentPosition();
  console.log(pos);
  console.log("finished");
}
go();
```

## Module_21 - ES2016 (ES7), ES2017 (ES8) + Beyond

Class Properties, padStart(), padEnd(), ES7 Exponential Operator,
Function Arguments trailing Comma, Object.entries(), Object.values()

```js
// Class Properties
class Dog() {
  constructor(name, breed) {
    this.name = name
    this.breed = breed
  }
  barks = 0 // new ES7 features
}

// padStart & padEnd
const seb = `Seb`
seb.padStart(12, `**`) // nb of character, padding character

// ES7
Array.includes(`str`)

3 ** 3 = 27 // Exponential Operator
2 ** 2 ** 2 = 16


// Comma trailing
const names = ['seb', 'wes', 'bos',]

const people = {
  seb: 'dev',
  wes: 'Cool',
  poppy: 'doggy', // Comma trailing
}

const inventory = {
  jeans: 23,
  shorts: 56,
  hoodies: 31,
}

// entries() : returns an array of a given object
// own enumerable property[key, value]
Object.entries(inventory)

const nav = Object.keys(inventory).map(item => `<li>${item}</li>`).join('')

// Object.values() : returns an array of a given object's own enumerable property values.
const totalInventory = Object.values(inventory).reduce( (a,b) => a + b)

Object.entries(inventory).forEach( [key, val] => {
  console.log(key, val)
})
```

## Glossary

arguments : Arguments is Array-like object corresponding to the arguments passed to a function.

arrow function : () => {}

Array.from() : The Array.from() method creates a new Array instance from an array-like or iterable object.

Array.find() : The find() method returns the value of the first element in the array that satisfies the provided testing function, otherwise undefined is returned.

Array.findIndex() : The findIndex() method returns the index of the first element in the array that satisfies the provided testing function, otherwise -1 is returned.

Array.of() : The Array.of() method creates a new Array instance with a variable number of arguments, regardless of number or type of the arguments.

asynchronous : In programming, asynchronous events are those occurring independently of the main program flow.
Ex :Ajax call, can retrieve data from server asynchronously in the background without stopping the main thread of the browser.

const : Variables constante

debugger : The debugger statement invokes any available debugging functionality, such
as setting a breakpoint. If no debugging functionality is available, this
statement has no effect.

entries() : Array.prototype.entries() : The entries() method returns a new Array
Iterator object that contains the key/value pairs for each index in the array.

fetch() : This method takes one mandatory argument, the path of the resource to fetch. It returns a Promise that resolve to a Response.

let :
 let dog1 = { name: 'Snickers', age: 3 }
let dog2 = { name: 'sunny', age: 1 }

const weakSauce = new WeakSet([dog1, dog2])

console.log(weakSauce)
dog1 = null
console.log(weakSauce)
