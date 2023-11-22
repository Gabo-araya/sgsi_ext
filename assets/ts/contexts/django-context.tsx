import React, { ReactNode, createContext } from 'react';
import { camelizeObject } from '../utils/casing';

/** Id used in the json_script template tag in django. */
const djangoContextSelector = '#django-context-data';

/**
 * Backend data as received from the backend.
 */
type DjangoSerializedContextType = {
  static_path: string,
  user: {
    id: number,
    email: string,
    first_name: string,
    last_name: string
  } | null
} | undefined;

/**
 * Backend data as exposed to the components.
 */
type DjangoContextType = {
  staticPath: string,
  user: {
    id: number,
    email: string,
    firstName: string,
    lastName: string
  } | null
} | undefined;

/**
 * This context provides data serialized from the backend, such as the current user.
 * Use this context only to provide global data available for all pages.
 * To load data for a specific component use another json_script for that component.
 * See the DjangoContextProvider for more info about how this data is loaded globally.
 * See the components/example-component to learn how to pass data for a single component.
 */
export const DjangoContext = createContext<DjangoContextType>(undefined);

/**
 * Loads the django context from a json serialized in the page body.
 * This context is rendered in /base/templates/base.html and is provided
 * by the ReactContextMixin in /base/views/mixins.py.
 * To use this context provider, a view using that mixin is required.
 */
export function DjangoContextProvider(props: { children: ReactNode }) {
  const contextJson: string | undefined = document.querySelector(djangoContextSelector)?.innerHTML;
  if (!contextJson) {
    throw new Error('Missing django context when django context is required');
  }

  const contextObject = JSON.parse(contextJson) as DjangoSerializedContextType;
  if (!contextObject) {
    throw new Error('Missing django context when django context is required');
  }

  if (!contextObject.static_path) {
    throw new Error('Missing static path in django context');
  }

  const context = camelizeObject(contextObject) as DjangoContextType;

  return (
    <DjangoContext.Provider value={context}>
      {props.children}
    </DjangoContext.Provider>
  );
}
