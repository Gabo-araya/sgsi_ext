/**
 * Converts a string in snake_case or kebab-case to camelCase.
 * @param input A string in snake_case or kebab-case.
 * @returns The camel cased string.
 */
export function camelize(input: string) {
  return input.replace(
    /([-_\s].)/ig,
    ($1) => $1.toUpperCase()
      .replace(/[-_\s]/g, '')
  );
}

/**
 * Returns an object with its keys recursively replaced to camel case.
 * If it's an array, the contents of the array are recursively replaced too.
 * Returns the input for other primitives.
 */
export function camelizeObject(input: unknown): unknown {
  if (Array.isArray(input)) {
    // eslint-disable-next-line @typescript-eslint/no-unsafe-return
    return input.map((el) => camelizeObject(el));
  }

  const type = typeof input;
  if (type === 'object' || type === 'function') {
    // typeof null is object too:
    if (input) {
      const obj = input as { [key: string]: unknown };
      const newObj: { [key: string]: unknown } = {};
      Object.keys(obj).forEach((key) => {
        newObj[camelize(key)] = camelizeObject(obj[key]);
      });
      return newObj;
    }
    return input;
  }

  // string, number, boolean. symbol, bigint, udefined:
  return input;
}
