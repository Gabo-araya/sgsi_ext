import React, { useState } from 'react';
import { JsonPropsType } from '../../component-loader';

/**
 * See /base/views/misc.py and /base/templates/index.html
 * to learn where this come from!
 */
interface ExampleComponentProps {
  backendParameter1: string,
  backendParameter2: string
}

/**
 * This is an example React component that accepts a json from the backend and
 * can be automatically loaded when the container is present in the html.
 * A component with no props can be used too.
 * See '/assets/ts/component-loader.ts' to learn more about the loading process.
 * Additional components can be registered in '/assets/ts/index.ts'.
 */
export function ExampleComponent(props: JsonPropsType) {
  const { backendParameter1, backendParameter2 } = props.jsonObject as ExampleComponentProps;
  const [count, setCount] = useState(0);

  return (
    <div className="example-component d-inline-block p-3 shadow-sm border rounded">
      <p>
        This is a React component that reads
        {' '}
        <span className="badge bg-success">{ backendParameter1 }</span>
      </p>
      <button type="button" className="btn btn-primary" onClick={() => setCount(count + 1)}>
        { backendParameter2 }
        {' '}
        <span className="badge bg-secondary ml-5">{ count }</span>
      </button>
    </div>
  );
}
