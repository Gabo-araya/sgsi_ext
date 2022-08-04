import React, { ReactElement } from 'react';
import ReactDOM from 'react-dom/client';
import { camelizeObject } from './utils/casing';

export type JsonPropsType = { jsonObject: unknown };

/**
 * We can automatically load any component that accepts a deserialized json
 * from backend as a prop, or components that take no parameters.
 */
export type AutoLoadableComponentType = (
  ((props: JsonPropsType) => ReactElement) | (() => ReactElement)
);

/**
 * This class will mount a list of React components to their parent
 * containers when the DOM content is loaded.
 */
export class ComponentLoader {
  static components = new Map<string, AutoLoadableComponentType>();

  /**
   * Registers a React component to be automatically mounted when a given selector for its
   * container is found on the html after the page loads.
   * The selector can be used only once (a single component per container), but a component
   * can be mounted on multiple selectors or in containers with multiple matches.
   * @param selector A css-style selector for the component's container. If there are
   *                 multiple matches the component will be instantiated for every container.
   * @param component The React component to mount on the container. If the container
   *                  defines a data-props-source-id attribute, JsonPropsType will be passed.
   */
  static registerComponent(selector: string, component: AutoLoadableComponentType) {
    this.components.set(selector, component);
  }

  /**
   * This method should be called only when the DOM content has fineshed loading.
   * It will create and mount every registered container to their parent container.
   * When the parent container defines a data-props-source-id attribute, a json with
   * the same id will be deserialized, converted to camel case and passed as the
   * props to the component.
   */
  static start() {
    this.components.forEach((component, selector) => {
      document.querySelectorAll(selector).forEach((container) => {
        const root = ReactDOM.createRoot(container);
        const containerDataset = (container as HTMLElement).dataset;
        let jsonObject: unknown;
        if (containerDataset.propsSourceId) {
          const json: string | undefined = document.querySelector(`#${containerDataset.propsSourceId}`)?.innerHTML;
          if (json) {
            // eslint-disable-next-line @typescript-eslint/no-unsafe-call
            jsonObject = camelizeObject(JSON.parse(json));
          }
        }
        root.render(
          jsonObject
            ? React.createElement<JsonPropsType>(component, { jsonObject })
            : React.createElement(component as () => ReactElement)
        );
      });
    });
  }
}
