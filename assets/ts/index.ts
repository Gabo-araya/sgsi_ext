// https://github.com/MrBin99/django-vite#assets
// Should not be required in other entrypoints like `status.ts`
// as long as `base.pug` loads this asset.
// The polyfill applies to `window.document` so importing it only here is enough.
import 'vite/modulepreload-polyfill';

// Importing Bootstrap forces the load of the type definition for the window.bootstrap global.
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import Bootstrap from 'bootstrap';

// Styles
import '../scss/main.scss';

// Vendors
import './vendors/choices';

// Behaviors
import './behaviors/input-rut';
import './behaviors/regions';

// Utils
import { App } from './utils/app';

// Load React components that can be auto-loaded on DOMContentLoaded
import { ComponentLoader } from './component-loader';
import { ExampleComponent } from './components/example-component';

ComponentLoader.registerComponent('#react-example-component', ExampleComponent);

/**
 * This runs on 'DOMContentLoaded', that means it waits for every javascript to be parsed and
 * executed and waits for stylesheets and defered external scripts. This may take a long time
 * if an external resource loads too slow (should we change this to <script defer src="...">?)
 */
window.addEventListener('DOMContentLoaded', () => {
  // Load the registered react components:
  ComponentLoader.start();

  const alerts = document.querySelectorAll('.alert');
  alerts.forEach((alert) => {
    App.Utils.highlight(alert);
  });

  setTimeout(() => {
    const mainAlerts = document.querySelectorAll('.main-alert .alert');
    mainAlerts.forEach((alert) => {
      window.bootstrap.Alert.getInstance(alert)?.close();
    });
  }, 10000);

  document.querySelectorAll('form')
    .forEach((form) => {
      form.addEventListener('submit', () => {
        const submitButtons = [...form.elements].filter((element) => (
          element.matches('[type="submit"]:not(.js-do-not-disable-on-submit)')
        ));

        // Disable buttons after submit to prevent disabling submit inputs
        // with values
        submitButtons.forEach((submitButton) => {
          // eslint-disable-next-line no-param-reassign
          (submitButton as HTMLButtonElement).disabled = true;
          App.Utils.showLoading(submitButton);
        });

        return true;
      });
    });
});
