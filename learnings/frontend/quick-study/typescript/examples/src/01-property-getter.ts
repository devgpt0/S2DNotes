function getProperty<T extends object, K extends keyof T>(object: T, key: K): T[K] {
  return object[key];
}

const user = { id: "u1", age: 28 };
const id = getProperty(user, "id");
const age = getProperty(user, "age");

console.log({ id, age });
