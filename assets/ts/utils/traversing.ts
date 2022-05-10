/**
 * Get the `elem`'s closest parent that matches `selector`.
 * Returns `null` if there isn't any.
 */
export function getParentBySelector(elem: Element, selector: string) {
  // eslint-disable-next-line no-param-reassign
  for (; elem && elem as unknown !== document; elem = elem.parentNode as Element) {
    if (elem.matches(selector)) {
      return elem;
    }
  }

  return null;
}
